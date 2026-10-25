"""
Modelo GMIC (Globally-Aware Multiple Instance Classifier)
Artigo Base: Sampaio & Cordeiro (UFRPE, SBC 2022) / Shen et al. (MedIA 2021)
"""

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:
    torch = None
    nn = object
    F = None

from .backbones import ResNet22Global, ResNet18Local


class GreedyPatchExtractor(nn.Module if torch else object):
    """
    Extrator Guloso de Patches Locais:
    Localiza os K picos máximos no mapa de calor A^c,
    aplica supressão de vizinhança espacial para evitar sobreposição,
    e recorta patches da imagem original na resolução nativa.
    """
    def __init__(self, patch_size: int = 256, num_patches: int = 6):
        super().__init__()
        self.patch_size = patch_size
        self.num_patches = num_patches

    def forward(self, high_res_img, cam_map):
        """
        high_res_img: [Batch, 1, H_img, W_img]
        cam_map: [Batch, 1, H_cam, W_cam]
        Retorna:
          patches: [Batch, K, 1, patch_size, patch_size]
          coords: Lista de coordenadas dos centros [cy, cx] por amostra
        """
        batch_size, _, H_img, W_img = high_res_img.shape
        _, _, H_cam, W_cam = cam_map.shape

        patches_batch = []
        coords_batch = []

        for b in range(batch_size):
            cur_cam = cam_map[b, 0].clone()
            cur_img = high_res_img[b]
            sample_patches = []
            sample_coords = []

            for _ in range(self.num_patches):
                # 1. Encontra a coordenada espacial do pico máximo de ativação
                max_val = torch.max(cur_cam)
                if max_val <= -100.0 or torch.isnan(max_val):
                    # Se todos os pixels foram suprimidos, usa o centro da imagem
                    cy_cam, cx_cam = H_cam // 2, W_cam // 2
                else:
                    max_idx = torch.argmax(cur_cam)
                    cy_cam = (max_idx // W_cam).item()
                    cx_cam = (max_idx % W_cam).item()

                sample_coords.append((cy_cam, cx_cam))

                # 2. Mapeamento de proporção do CAM para a resolução da imagem original
                cy_img = int((cy_cam / max(1, H_cam)) * H_img)
                cx_img = int((cx_cam / max(1, W_cam)) * W_img)

                # 3. Delimita limites do recorte com proteção de bordas
                half = self.patch_size // 2
                ymin = max(0, cy_img - half)
                ymax = min(H_img, cy_img + half)
                xmin = max(0, cx_img - half)
                xmax = min(W_img, cx_img + half)

                patch = cur_img[:, ymin:ymax, xmin:xmax]

                # 4. Zero-padding caso o recorte encoste nas extremidades da imagem
                ph, pw = patch.shape[1], patch.shape[2]
                if ph != self.patch_size or pw != self.patch_size:
                    pad_bottom = self.patch_size - ph
                    pad_right = self.patch_size - pw
                    patch = F.pad(patch, (0, pad_right, 0, pad_bottom), mode='constant', value=0.0)

                sample_patches.append(patch)

                # 5. Supressão de vizinhança espacial no CAM (zera região ao redor do pico)
                rad_y = max(1, int(H_cam * (self.patch_size / H_img) / 2))
                rad_x = max(1, int(W_cam * (self.patch_size / W_img) / 2))

                y0 = max(0, cy_cam - rad_y)
                y1 = min(H_cam, cy_cam + rad_y + 1)
                x0 = max(0, cx_cam - rad_x)
                x1 = min(W_cam, cx_cam + rad_x + 1)

                cur_cam[y0:y1, x0:x1] = -999.0

            patches_batch.append(torch.stack(sample_patches)) # [K, 1, P, P]
            coords_batch.append(sample_coords)

        return torch.stack(patches_batch), coords_batch


class GMIC(nn.Module if torch else object):
    """
    Globally-Aware Multiple Instance Classifier (GMIC).
    Integração dos três ramos:
    1. Ramo Global (ResNet-22)
    2. Ramo Local (ResNet-18 com agregação MIL por Max-Pooling)
    3. Módulo de Fusão Linear Multiescala
    """
    def __init__(
        self,
        global_backbone=None,
        local_backbone=None,
        num_patches: int = 6,
        patch_size: int = 256,
        dim_global: int = 512,
        dim_local: int = 512,
        dim_fusion: int = 256,
        dropout_rate: float = 0.3
    ):
        super().__init__()
        self.global_net = global_backbone if global_backbone is not None else ResNet22Global(in_channels=1, out_features=dim_global)
        self.local_net = local_backbone if local_backbone is not None else ResNet18Local(in_channels=1, out_features=dim_local)
        self.patch_extractor = GreedyPatchExtractor(patch_size=patch_size, num_patches=num_patches)

        self.dim_global = dim_global
        self.dim_local = dim_local

        # Classificadores lineares independentes para cada ramo
        self.fc_global = nn.Linear(dim_global, 1)
        self.fc_local = nn.Linear(dim_local, 1)

        # Módulo de Fusão
        self.fc_fusion = nn.Sequential(
            nn.Linear(dim_global + dim_local, dim_fusion),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout_rate),
            nn.Linear(dim_fusion, 1)
        )

    def forward(self, x, cam_generator=None):
        """
        x: [Batch, 1, H, W]
        cam_generator: Função ou objeto gerador de CAM desacoplado
        """
        # ==========================================
        # 1. Ramo Global
        # ==========================================
        feat_map, h_global = self.global_net(x) # feat_map: [B, 512, Hg, Wg], h_global: [B, 512]
        logits_global = self.fc_global(h_global) # [B, 1]
        y_global = torch.sigmoid(logits_global).squeeze(-1) # [B]

        # ==========================================
        # 2. Geração do Mapa de Ativação (CAM)
        # ==========================================
        if cam_generator is not None:
            # Invoca o método de CAM desacoplado (XGradCAM, GradCAM++, etc.)
            cam_map = cam_generator(x, feat_map)
        else:
            # CAM clássico nativo via projeção linear dos pesos de fc_global
            # w: [1, 512], feat_map: [B, 512, Hg, Wg]
            w = self.fc_global.weight # [1, dim_global]
            cam_map = F.relu(torch.einsum('kc, bchw -> bkhw', w, feat_map)) # [B, 1, Hg, Wg]
            
            # Normalização min-max por amostra
            max_vals = torch.amax(cam_map, dim=[-2, -1], keepdim=True)
            min_vals = torch.amin(cam_map, dim=[-2, -1], keepdim=True)
            cam_map = (cam_map - min_vals) / (max_vals - min_vals + 1e-8)

        # ==========================================
        # 3. Ramo Local
        # ==========================================
        patches, patch_coords = self.patch_extractor(x, cam_map) # [B, K, 1, P, P]
        B, K, C, Hp, Wp = patches.shape
        patches_flattened = patches.view(B * K, C, Hp, Wp)

        h_patches = self.local_net(patches_flattened) # [B * K, dim_local]
        h_patches = h_patches.view(B, K, self.dim_local) # [B, K, dim_local]

        # Agregação MIL via Max-Pooling sobre as K instâncias locais
        h_local, _ = torch.max(h_patches, dim=1) # [B, dim_local]
        logits_local = self.fc_local(h_local) # [B, 1]
        y_local = torch.sigmoid(logits_local).squeeze(-1) # [B]

        # ==========================================
        # 4. Módulo de Fusão
        # ==========================================
        h_fused = torch.cat([h_global, h_local], dim=-1) # [B, dim_global + dim_local]
        logits_fusion = self.fc_fusion(h_fused) # [B, 1]
        y_fusion = torch.sigmoid(logits_fusion).squeeze(-1) # [B]

        return {
            'y_global': y_global,
            'y_local': y_local,
            'y_fusion': y_fusion,
            'logits_global': logits_global.squeeze(-1),
            'logits_local': logits_local.squeeze(-1),
            'logits_fusion': logits_fusion.squeeze(-1),
            'cam_map': cam_map,
            'patches': patches,
            'patch_coords': patch_coords,
            'h_global': h_global,
            'h_local': h_local
        }
