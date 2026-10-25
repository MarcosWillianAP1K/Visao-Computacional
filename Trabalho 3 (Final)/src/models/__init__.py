"""
Módulo de Modelos e Redes Neurais para GMIC
"""

from .backbones import ResNet22Global, ResNet18Local, BasicBlock
from .gmic import GMIC, GreedyPatchExtractor
from .losses import GMICLoss

__all__ = [
    'ResNet22Global',
    'ResNet18Local',
    'BasicBlock',
    'GMIC',
    'GreedyPatchExtractor',
    'GMICLoss'
]
