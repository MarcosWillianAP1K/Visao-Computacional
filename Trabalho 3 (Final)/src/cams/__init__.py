"""
Módulo de Mapas de Ativação de Classe (CAM) e Desacoplamento
"""

from .cam_manager import CAMManager, extract_bounding_boxes_from_cam

__all__ = ['CAMManager', 'extract_bounding_boxes_from_cam']
