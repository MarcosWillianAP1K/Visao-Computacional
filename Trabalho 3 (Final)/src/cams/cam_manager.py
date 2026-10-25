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
    import torch.nn.functional as F
except ImportError:
    torch = None
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


class CAMManager:
    """
    Interface Unificada e Desacoplada para Geração de CAMs.
    Permite configurar qualquer método no treino e alternar para outro no teste.
    Possui implementações nativas em PyTorch com fallback automático.
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
        if PYTORCH_GRAD_CAM_AVAILABLE and self.method_name != 'cam':
            method_map = {
                'gradcam': GradCAM,
                'gradcam++': GradCAMPlusPlus,
                'xgradcam': XGradCAM,
                'layercam': LayerCAM
            }
            cam_class = method_map.get(self.method_name)
            if cam_class:
                try:
                    self.cam_obj = cam_class(
                        model=self.model,
                        target_layers=[self.target_layer],
                        use_cuda=self.use_cuda
                    )
                except Exception:
                    self.cam_obj = None

    def __call__(self, input_tensor, feat_map=None):
        """
        Gera mapa de ativação 2D normalizado [B, 1, Hg, Wg].
        """
        if self.method_name == 'cam' or self.cam_obj is None:
            return self._generate_native(input_tensor, feat_map)
        else:
            try:
                # pytorch-grad-cam espera targets=None para máxima classe ativada
                grayscale_cam = self.cam_obj(input_tensor=input_tensor, targets=None)
                # Converte numpy [B, H, W] para torch tensor [B, 1, H, W]
                cam_tensor = torch.from_numpy(grayscale_cam).unsqueeze(1).float()
                if self.use_cuda and torch.cuda.is_available():
                    cam_tensor = cam_tensor.to(input_tensor.device)
                return cam_tensor
            except Exception:
                # Fallback para o motor nativo em caso de erro
                return self._generate_native(input_tensor, feat_map)

    def _generate_native(self, x, feat_map=None):
        """
        Motor nativo em PyTorch puro para os 5 métodos de saliência.
        Garante funcionamento imediato e reprodutível independente de bibliotecas externas.
        """
        if torch is None:
            raise ImportError("PyTorch necessário para gerar mapas de ativação.")

        # Se feature map não foi passado, obtém da rede global
        if feat_map is None:
            feat_map, h_global = self.model.global_net(x)
        else:
            h_global = self.model.global_net.gap(feat_map)
            h_global = torch.flatten(h_global, 1)

        B, C, H, W = feat_map.shape

        # 1. CAM Clássico (Zhou et al., 2016)
        if self.method_name == 'cam':
            w = self.model.fc_global.weight # [1, C]
            cam = F.relu(torch.einsum('kc, bchw -> bkhw', w, feat_map))
            return self._normalize_cam(cam)

        # Para métodos baseados em gradientes:
        feat_map_grad = feat_map.clone().detach().requires_grad_(True)
        h_g = self.model.global_net.gap(feat_map_grad)
        h_g = torch.flatten(h_g, 1)
        score = self.model.fc_global(h_g) # [B, 1]

        # Gradientes do score em relação às ativações
        grads = torch.autograd.grad(
            outputs=score.sum(),
            inputs=feat_map_grad,
            retain_graph=True,
            create_graph=False
        )[0] # [B, C, H, W]

        # 2. Grad-CAM (Selvaraju et al., 2017): Média espacial de gradientes
        if self.method_name == 'gradcam':
            alpha = torch.mean(grads, dim=[-2, -1], keepdim=True) # [B, C, 1, 1]
            cam = F.relu(torch.sum(alpha * feat_map, dim=1, keepdim=True))
            return self._normalize_cam(cam)

        # 3. Grad-CAM++ (Chattopadhay et al., 2018): Derivadas de ordens superiores
        elif self.method_name == 'gradcam++':
            grads_power_2 = grads ** 2
            grads_power_3 = grads ** 3
            # Coeficientes alfa analíticos
            sum_activations = torch.sum(feat_map, dim=[-2, -1], keepdim=True)
            eps = 1e-7
            aij = grads_power_2 / (2.0 * grads_power_2 + sum_activations * grads_power_3 + eps)
            aij = torch.where(grads != 0, aij, torch.zeros_like(aij))
            
            # Ponderação positiva dos gradientes
            weights = torch.sum(aij * F.relu(grads), dim=[-2, -1], keepdim=True) # [B, C, 1, 1]
            cam = F.relu(torch.sum(weights * feat_map, dim=1, keepdim=True))
            return self._normalize_cam(cam)

        # 4. XGrad-CAM (Fu et al., 2020): Axiomas de Sensibilidade e Conservação
        elif self.method_name == 'xgradcam':
            # Soma das ativações por canal
            sum_act = torch.sum(feat_map, dim=[-2, -1], keepdim=True) + 1e-7
            normalized_act = feat_map / sum_act # [B, C, H, W]
            alpha = torch.sum(normalized_act * grads, dim=[-2, -1], keepdim=True) # [B, C, 1, 1]
            cam = F.relu(torch.sum(alpha * feat_map, dim=1, keepdim=True))
            return self._normalize_cam(cam)

        # 5. Layer-CAM (Jiang et al., 2021): Ponderação elemento a elemento
        elif self.method_name == 'layercam':
            weights = F.relu(grads) # [B, C, H, W]
            cam = F.relu(torch.sum(weights * feat_map, dim=1, keepdim=True))
            return self._normalize_cam(cam)

        return self._normalize_cam(feat_map[:, :1])

    def _normalize_cam(self, cam_tensor):
        """Normalização Min-Max para escala [0, 1] com proteção contra divisão por zero"""
        min_v = torch.amin(cam_tensor, dim=[-2, -1], keepdim=True)
        max_v = torch.amax(cam_tensor, dim=[-2, -1], keepdim=True)
        return (cam_tensor - min_v) / (max_v - min_v + 1e-8)


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
