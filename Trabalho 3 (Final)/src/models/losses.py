"""
Função de Perda Multi-Ramo com Regularização de Esparsidade L1 (GMICLoss)
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


class GMICLoss(nn.Module if torch else object):
    """
    Função de Perda do GMIC:
    L = BCE(y, y_local) + BCE(y, y_global) + BCE(y, y_fusao) + beta * L_reg(A^c)
    Onde beta = 3.26 penaliza a área ativada no mapa de ativação A^c,
    forçando concentração espacial e esparsidade sobre a massa neoplásica.
    Compatível com Automatic Mixed Precision (AMP FP16).
    """
    def __init__(self, beta: float = 3.26):
        super().__init__()
        self.beta = beta
        if torch is not None:
            self.bce_logits = nn.BCEWithLogitsLoss()
            self.bce_prob = nn.BCELoss()

    def forward(self, outputs: dict, target):
        """
        outputs: dicionário retornado pelo GMIC com chaves:
                 'y_local', 'y_global', 'y_fusion', 'cam_map'
                 (e opcionalmente 'logits_local', 'logits_global', 'logits_fusion')
        target: tensor [B] contendo o rótulo de imagem (0 = normal, 1 = massa)
        """
        target = target.float()

        # 1. Perdas de Entropia Cruzada Binária para cada ramo
        # Utiliza BCEWithLogitsLoss quando logits estão disponíveis (seguro para AMP FP16)
        if 'logits_local' in outputs and 'logits_global' in outputs and 'logits_fusion' in outputs:
            loss_local = self.bce_logits(outputs['logits_local'].float(), target)
            loss_global = self.bce_logits(outputs['logits_global'].float(), target)
            loss_fusion = self.bce_logits(outputs['logits_fusion'].float(), target)
        else:
            eps = 1e-7
            with torch.amp.autocast('cuda', enabled=False) if hasattr(torch, 'amp') else torch.cuda.amp.autocast(enabled=False):
                y_loc = torch.clamp(outputs['y_local'].float(), eps, 1.0 - eps)
                y_glo = torch.clamp(outputs['y_global'].float(), eps, 1.0 - eps)
                y_fus = torch.clamp(outputs['y_fusion'].float(), eps, 1.0 - eps)
                loss_local = self.bce_prob(y_loc, target)
                loss_global = self.bce_prob(y_glo, target)
                loss_fusion = self.bce_prob(y_fus, target)

        # 2. Termo de Regularização L1 de Esparsidade sobre o Mapa de Ativação
        cam_map = outputs['cam_map'].float()  # [B, 1, Hg, Wg]

        # Norma L1 espacial somada sobre altura e largura, normalizada pela área espacial
        Hg, Wg = cam_map.shape[-2], cam_map.shape[-1]
        l1_reg_sum = torch.mean(torch.sum(torch.abs(cam_map), dim=[-2, -1]))
        l1_reg_normalized = l1_reg_sum / max(1, (Hg * Wg))

        # 3. Perda Total Ponderada (Equação 2 do artigo: beta = 3.26)
        total_loss = loss_local + loss_global + loss_fusion + (self.beta * l1_reg_normalized)

        return total_loss, {
            'loss_total': total_loss.item(),
            'loss_local': loss_local.item(),
            'loss_global': loss_global.item(),
            'loss_fusion': loss_fusion.item(),
            'l1_reg': l1_reg_normalized.item(),
            'l1_reg_raw_sum': l1_reg_sum.item(),
            'weighted_reg': (self.beta * l1_reg_normalized).item()
        }
