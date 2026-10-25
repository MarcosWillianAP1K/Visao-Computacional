"""
Configurações Globais e Hiperparâmetros do Projeto GMIC - WSOD
Disciplina: Tópicos Especiais em Visão Computacional - UFPI
Artigo Base: Sampaio & Cordeiro (UFRPE, SBC 2022)
"""

import os
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class ModelConfig:
    # Dimensões da imagem mamográfica de alta resolução (H, W)
    input_resolution: Tuple[int, int] = (2944, 1920)
    
    # Extração de patches locais
    num_patches: int = 6
    patch_size: int = 256
    
    # Dimensões latentes dos backbones
    dim_global: int = 512
    dim_local: int = 512
    dim_fusion: int = 256
    dropout_rate: float = 0.3

    # Função de perda: peso de esparsidade L1 sobre o mapa de ativação da classe
    beta_sparsity: float = 3.26

@dataclass
class TrainingConfig:
    # Treinamento com Acumulação de Gradientes
    batch_size: int = 2               # Batch físico na GPU
    gradient_accumulation_steps: int = 3  # Batch virtual = 2 * 3 = 6
    num_epochs: int = 50
    learning_rate: float = 1e-4
    weight_decay: float = 1e-5
    
    # Otimização e precisão mista
    use_amp: bool = True              # torch.cuda.amp FP16
    seed: int = 42
    num_workers: int = 4
    
    # Método padrão de CAM durante o treino
    train_cam: str = 'xgradcam'       # 'cam', 'gradcam', 'gradcam++', 'xgradcam', 'layercam'

@dataclass
class EvalConfig:
    # Critério de detecção WSOD
    iou_threshold: float = 0.3
    cam_thresholds: List[float] = field(default_factory=lambda: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    
    # Método padrão de CAM durante a inferência / teste
    test_cam: str = 'gradcam++'       # 'cam', 'gradcam', 'gradcam++', 'xgradcam', 'layercam'

@dataclass
class PathConfig:
    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    data_dir: str = os.path.join(base_dir, '..', 'data', 'vindr-mammo')
    metadata_train_csv: str = os.path.join(data_dir, 'train_metadata.csv')
    metadata_test_csv: str = os.path.join(data_dir, 'test_metadata.csv')
    images_dir: str = os.path.join(data_dir, 'images')
    checkpoints_dir: str = os.path.join(base_dir, 'checkpoints')
    results_dir: str = os.path.join(base_dir, 'results')

@dataclass
class Config:
    model: ModelConfig = field(default_factory=ModelConfig)
    train: TrainingConfig = field(default_factory=TrainingConfig)
    eval: EvalConfig = field(default_factory=EvalConfig)
    paths: PathConfig = field(default_factory=PathConfig)

# Instância padrão para importação direta
DEFAULT_CONFIG = Config()
