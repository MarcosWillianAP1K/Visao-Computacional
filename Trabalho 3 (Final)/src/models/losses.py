"""
Função de Perda Multi-Ramo com Regularização de Esparsidade L1 (GMICLoss)
Artigo Base: Sampaio & Cordeiro (UFRPE, SBC 2022) / Shen et al. (MedIA 2021)
"""

try:
    import torch
    import torch.nn as nn
except ImportError:
    torch = None
    nn = object


class GMICLoss(nn.Module if torch else object):
    """
    Função de Perda do GMIC:
    L = BCE(y, y_local) + BCE(y, y_global) + BCE(y, y_fusao) + beta * L_reg(A^c)
    Onde beta = 3.26 penaliza a área ativada no mapa de ativação A^c,
    forçando concentração espacial e esparsidade sobre a massa neoplásica.
    """
    def __init__(self, beta: float = 3.26):
        super().__init__()
        self.beta = beta
        self.bce_local = nn.BCELoss()
        self.bce_global = nn.BCELoss()
        self.bce_fusion = nn.BCELoss()

    def forward(self, outputs: dict, target):
        """
        outputs: dicionário retornado pelo GMIC com chaves:
                 'y_local', 'y_global', 'y_fusion', 'cam_map'
        target: tensor [B] contendo o rótulo de imagem (0 = normal, 1 = massa)
        """
        # Garante float32 no target
        target = target.float()

        # Evita extremos numéricos de log(0) via clamping
        eps = 1e-7
        y_loc = torch.clamp(outputs['y_local'], eps, 1.0 - eps)
        y_glo = torch.clamp(outputs['y_global'], eps, 1.0 - eps)
        y_fus = torch.clamp(outputs['y_fusion'], eps, 1.0 - eps)

        # 1. Perdas de Entropia Cruzada Binária para cada ramo
        loss_local = self.bce_local(y_loc, target)
        loss_global = self.bce_global(y_glo, target)
        loss_fusion = self.bce_fusion(y_fus, target)

        # 2. Termo de Regularização L1 de Esparsidade sobre o Mapa de Ativação
        # Aplicado preferencialmente sobre imagens da classe positiva (massa),
        # ou sobre todo o lote com média por imagem: L_reg = mean(sum(|A^c_{i,j}|))
        cam_map = outputs['cam_map'] # [B, 1, Hg, Wg]
        
        # Norma L1 espacial somada sobre altura e largura, com média sobre o batch
        l1_reg = torch.mean(torch.sum(torch.abs(cam_map), dim=[-2, -1]))
        
        # Normalização relativa para escala [0, 1] do mapa espacial se necessário
        Hg, Wg = cam_map.shape[-2], cam_map.shape[-1]
        l1_reg_normalized = l1_reg / (Hg * Wg)

        # 3. Perda Total Ponderada
        total_loss = loss_local + loss_global + loss_fusion + (self.beta * l1_reg_normalized)

        return total_loss, {
            'loss_total': total_loss.item(),
            'loss_local': loss_local.item(),
            'loss_global': loss_global.item(),
            'loss_fusion': loss_fusion.item(),
            'l1_reg': l1_reg_normalized.item(),
            'weighted_reg': (self.beta * l1_reg_normalized).item()
        }
