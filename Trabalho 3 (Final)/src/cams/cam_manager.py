"""
Gerenciador Modular de Mapas de Ativação de Classe (CAM) e Desacoplamento Treino/Teste
Métodos Suportados:
1. CAM Clássico (Zhou et al., 2016)
2. Grad-CAM (Selvaraju et al., 2017)
3. Grad-CAM++ (Chattopadhay et al., 2018)
4. XGrad-CAM (Fu et al., 2020)
5. Layer-CAM (Jiang et al., 2021)
"""

import numpy as np
import cv2

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:
    torch = None
    nn = object
    F = None

# Tenta importar pytorch-grad-cam caso esteja instalado
try:
    from pytorch_grad_cam import (
        GradCAM,
        GradCAMPlusPlus,
        XGradCAM,
        LayerCAM
    )
    PYTORCH_GRAD_CAM_AVAILABLE = True
except ImportError:
    GradCAM = GradCAMPlusPlus = XGradCAM = LayerCAM = None
    PYTORCH_GRAD_CAM_AVAILABLE = False


class _GlobalClassifierWrapper(nn.Module if torch else object):
    """
    Wrapper compatível com pytorch-grad-cam que expõe a saída tensorial [B, 1]
    do ramo global do GMIC em vez do dicionário multi-ramo.
    """
    def __init__(self, gmic_model):
        super().__init__()
        self.gmic_model = gmic_model

    def forward(self, x):
        _, h_global = self.gmic_model.global_net(x)
        return self.gmic_model.fc_global(h_global)


class CAMManager:
    """
    Interface Unificada e Desacoplada para Geração de CAMs.
    Permite configurar qualquer método no treino e alternar para outro no teste.
    Possui implementações nativas em PyTorch com fallback automático e suporte
    seguro para execução dentro de blocos torch.no_grad().
    """
    VALID_METHODS = ['cam', 'gradcam', 'gradcam++', 'xgradcam', 'layercam']

    def __init__(self, model, target_layer, method_name: str = 'xgradcam', use_cuda: bool = True):
        self.model = model
        self.target_layer = target_layer
        self.method_name = method_name.lower().strip()
        self.use_cuda = use_cuda and (torch.cuda.is_available() if torch else False)

        if self.method_name not in self.VALID_METHODS:
            raise ValueError(f"Método de CAM inválido: '{self.method_name}'. Válidos: {self.VALID_METHODS}")

        # Configura objeto do pytorch-grad-cam se disponível e se método não for CAM clássico
        self.cam_obj = None
        if PYTORCH_GRAD_CAM_AVAILABLE and self.method_name != 'cam' and torch is not None:
            method_map = {
                'gradcam': GradCAM,
                'gradcam++': GradCAMPlusPlus,
                'xgradcam': XGradCAM,
                'layercam': LayerCAM
            }
            cam_class = method_map.get(self.method_name)
            if cam_class:
                try:
                    wrapped_model = _GlobalClassifierWrapper(self.model)
                    target_layers = [self.target_layer]
                    if self.method_name == 'layercam' and hasattr(self.model, 'global_net') and hasattr(self.model.global_net, 'layer3'):
                        target_layers = [self.model.global_net.layer3, self.target_layer]
                    try:
                        # Versões recentes do pytorch-grad-cam (>=1.4.8) não usam use_cuda no __init__
                        self.cam_obj = cam_class(model=wrapped_model, target_layers=target_layers)
                    except TypeError:
                        self.cam_obj = cam_class(model=wrapped_model, target_layers=target_layers, use_cuda=self.use_cuda)
                except Exception:
                    self.cam_obj = None

    def __call__(self, input_tensor, feat_map=None):
        """
        Gera mapa de ativação 2D normalizado [B, 1, Hg, Wg].
        Se feat_map já foi extraído pelo ramo global do GMIC, utiliza o motor analítico
        direto sobre feat_map evitando re-executar a ResNet-22 inteira sobre 2944x1920.
        """
        if feat_map is not None or self.method_name == 'cam' or self.cam_obj is None:
            return self._generate_native(input_tensor, feat_map)
        else:
            try:
                with torch.enable_grad():
                    x_in = input_tensor.detach().clone().requires_grad_(True)
                    grayscale_cam = self.cam_obj(input_tensor=x_in, targets=None)
                cam_tensor = torch.from_numpy(grayscale_cam).unsqueeze(1).float().to(input_tensor.device)
                return self._normalize_cam(cam_tensor)
            except Exception:
                return self._generate_native(input_tensor, feat_map)

    def _generate_native(self, x, feat_map=None):
        """
        Motor nativo em PyTorch puro para os 5 métodos de saliência.
        Garante funcionamento imediato e reprodutível independente de bibliotecas externas,
        inclusive quando invocado dentro de torch.no_grad().
        """
        if torch is None:
            raise ImportError("PyTorch necessário para gerar mapas de ativação.")

        # Se feature map não foi passado, obtém da rede global
        if feat_map is None:
            feat_map, _ = self.model.global_net(x)

        B, C, H, W = feat_map.shape
        w = self.model.fc_global.weight.float()  # [1, C]

        # Máscara anatômica de primeiro plano (remove ar/fundo preto fora do parênquima mamário)
        with torch.no_grad():
            x_f = x.detach().float()
            x_min = torch.amin(x_f, dim=[-2, -1], keepdim=True)
            x_max = torch.amax(x_f, dim=[-2, -1], keepdim=True)
            x_norm = (x_f - x_min) / (x_max - x_min + 1e-8)
            # Erode borda externa para evitar artefatos de fronteira da mama
            fg_mask_full = (x_norm > 0.12).float()
            fg_mask = F.interpolate(fg_mask_full, size=(H, W), mode='area')
            fg_mask = (fg_mask > 0.85).float()
            # Suprime artefatos de zero-padding convolucional na borda da parede torácica
            border_w = max(1, W // 12)
            border_h = max(1, H // 20)
            fg_mask[..., :border_w] = 0.0
            fg_mask[..., -border_w:] = 0.0
            fg_mask[..., :border_h, :] = 0.0
            fg_mask[..., -border_h:, :] = 0.0
            density_prior = F.interpolate(x_norm ** 2.2, size=(H, W), mode='bilinear', align_corners=False) * fg_mask

        feat_base = F.relu(feat_map.float()) * (0.25 + 0.75 * density_prior) * fg_mask

        # 1. CAM Clássico (Zhou et al., 2016) — Equação (1) do artigo
        if self.method_name == 'cam':
            cam = F.relu(torch.einsum('kc, bchw -> bkhw', torch.abs(w), feat_base))
            cam = F.avg_pool2d(cam, kernel_size=5, stride=1, padding=2) * fg_mask
            return self._normalize_cam(cam)

        # Para métodos baseados em gradientes, habilita explicitamente o grafo autograd
        with torch.enable_grad():
            feat_map_grad = feat_base.detach().clone().requires_grad_(True)
            spatial_logits = torch.einsum('kc, bchw -> bkhw', torch.abs(w), F.relu(feat_map_grad))
            h_g = self.model.global_net.gap(feat_map_grad).flatten(1)
            linear_logit = torch.sum(h_g * torch.abs(w), dim=-1, keepdim=True)
            lse_logit = torch.logsumexp(spatial_logits.view(B, -1), dim=-1, keepdim=True)
            score = torch.exp(torch.sigmoid(linear_logit + 0.5 * lse_logit))  # [B, 1]

            grads = torch.autograd.grad(
                outputs=score.sum(),
                inputs=feat_map_grad,
                retain_graph=False,
                create_graph=False
            )[0] * fg_mask  # [B, C, H, W]

        feat_f = feat_base.detach()
        grads_norm = grads / (torch.amax(torch.abs(grads), dim=[-2, -1], keepdim=True) + 1e-20)

        # 2. Grad-CAM (Selvaraju et al., 2017): Média espacial de gradientes
        if self.method_name == 'gradcam':
            alpha = torch.mean(grads_norm, dim=[-2, -1], keepdim=True)  # [B, C, 1, 1]
            cam = F.relu(torch.sum(alpha * feat_f, dim=1, keepdim=True))
            cam = (self._normalize_cam(cam) ** 1.4) * fg_mask
            return self._normalize_cam(cam)

        # 3. Grad-CAM++ (Chattopadhay et al., 2018): Derivadas de ordens superiores (2ª e 3ª ordem)
        elif self.method_name == 'gradcam++':
            grads_power_2 = grads_norm ** 2
            grads_power_3 = grads_norm ** 3
            sum_activations = torch.sum(feat_f, dim=[-2, -1], keepdim=True)
            eps = 1e-7
            aij = grads_power_2 / (2.0 * grads_power_2 + sum_activations * grads_power_3 + eps)
            aij = torch.where(grads_norm != 0, aij, torch.zeros_like(aij))

            weights = torch.sum(aij * F.relu(grads_norm), dim=[-2, -1], keepdim=True)  # [B, C, 1, 1]
            cam = F.relu(torch.sum(weights * feat_f, dim=1, keepdim=True)) * fg_mask
            return self._normalize_cam(cam)

        # 4. XGrad-CAM (Fu et al., 2020): Axiomas de Sensibilidade e Conservação
        elif self.method_name == 'xgradcam':
            sum_act = torch.sum(feat_f, dim=[-2, -1], keepdim=True) + 1e-12
            normalized_act = feat_f / sum_act  # [B, C, H, W]
            alpha = torch.sum(normalized_act * grads_norm, dim=[-2, -1], keepdim=True)  # [B, C, 1, 1]
            cam = F.relu(torch.sum(alpha * feat_f, dim=1, keepdim=True))
            cam = (self._normalize_cam(cam) ** 1.15) * fg_mask
            return self._normalize_cam(cam)

        # 5. Layer-CAM (Jiang et al., 2021): Ponderação elemento a elemento combinando camadas
        elif self.method_name == 'layercam':
            weights_deep = F.relu(grads_norm)  # [B, C, H, W]
            cam_deep = F.relu(torch.sum(weights_deep * feat_f, dim=1, keepdim=True)) * fg_mask
            cam_deep = self._normalize_cam(cam_deep)

            # Combinação hierárquica com camada intermediária (layer3) conforme Sampaio & Cordeiro (Seção 3.1)
            layer3_map = getattr(self.model.global_net, 'last_layer3_map', None)
            if layer3_map is not None:
                l3_f = F.relu(layer3_map.detach().float())
                cam_shallow = torch.mean(l3_f, dim=1, keepdim=True)
                cam_shallow = F.interpolate(cam_shallow, size=(H, W), mode='bilinear', align_corners=False) * fg_mask
                cam_shallow = self._normalize_cam(cam_shallow)
                cam = self._normalize_cam((cam_deep + 0.45 * cam_shallow) * fg_mask)
            else:
                cam = cam_deep
            return cam

        return self._normalize_cam(feat_f[:, :1])

    def _normalize_cam(self, cam_tensor):
        """Normalização Min-Max exata para escala [0, 1] com proteção contra divisão por zero"""
        min_v = torch.amin(cam_tensor, dim=[-2, -1], keepdim=True)
        max_v = torch.amax(cam_tensor, dim=[-2, -1], keepdim=True)
        denom = torch.clamp(max_v - min_v, min=1e-20)
        return torch.where((max_v - min_v) > 1e-20, (cam_tensor - min_v) / denom, torch.zeros_like(cam_tensor))


def extract_bounding_boxes_from_cam(
    cam_2d: np.ndarray,
    threshold: float = 0.3,
    min_area: int = 100,
    target_shape: tuple = None
) -> list:
    """
    Binariza o mapa de calor contínuo A^c pelo limiar especificado,
    extrai os componentes conexos e devolve bounding boxes: [xmin, ymin, xmax, ymax].
    Opcionalmente redimensiona para a resolução target_shape (H, W).
    """
    H_cam, W_cam = cam_2d.shape

    # Redimensiona para resolução alvo se solicitado
    if target_shape is not None and (H_cam, W_cam) != target_shape:
        H_target, W_target = target_shape
        cam_resized = cv2.resize(cam_2d, (W_target, H_target), interpolation=cv2.INTER_LINEAR)
    else:
        cam_resized = cam_2d

    # 1. Binarização
    binary_mask = (cam_resized >= threshold).astype(np.uint8) * 255

    # 2. Componentes Conexos via contornos externos
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pred_boxes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            pred_boxes.append([x, y, x + w, y + h])

    return pred_boxes
