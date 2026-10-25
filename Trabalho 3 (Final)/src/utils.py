"""
Funções Utilitárias para Reprodutibilidade, Logging e Visualização
Disciplina: Tópicos Especiais em Visão Computacional - UFPI
"""

import os
import random
import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

try:
    import torch
except ImportError:
    torch = None


def seed_everything(seed: int = 42) -> None:
    """
    Fixa todas as sementes pseudo-aleatórias para garantir máxima reprodutibilidade.
    """
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    if torch is not None:
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def setup_logger(name: str = "GMIC_WSOD", log_file: str = None) -> logging.Logger:
    """
    Configura logger formatado para console e arquivo.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt='[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File handler (opcional)
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            
    return logger


def save_checkpoint(state: dict, is_best: bool, checkpoint_dir: str, filename: str = "checkpoint.pth") -> str:
    """
    Salva estado dos pesos da rede e metadados de treinamento.
    """
    if torch is None:
        raise ImportError("PyTorch não encontrado para salvar checkpoint.")
        
    os.makedirs(checkpoint_dir, exist_ok=True)
    filepath = os.path.join(checkpoint_dir, filename)
    torch.save(state, filepath)
    
    if is_best:
        best_filepath = os.path.join(checkpoint_dir, "best_model.pth")
        torch.save(state, best_filepath)
        return best_filepath
        
    return filepath


def load_checkpoint(checkpoint_path: str, model, optimizer=None, device="cpu"):
    """
    Restaura pesos de modelo e estado de otimizador a partir de um checkpoint.
    """
    if torch is None:
        raise ImportError("PyTorch não encontrado para carregar checkpoint.")
        
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint não encontrado em: {checkpoint_path}")
        
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    
    if optimizer and 'optimizer_state_dict' in checkpoint:
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        
    return checkpoint


def plot_wsod_detection(
    image: np.ndarray,
    cam_map: np.ndarray,
    pred_boxes: list,
    gt_boxes: list,
    save_path: str,
    title: str = "WSOD Detecção de Massa em Mamografia"
):
    """
    Gera imagem lado a lado:
    1. Mamografia com Ground Truth (Verde) e Bounding Boxes preditas (Vermelho).
    2. Mapa de Ativação de Classe (CAM) sobreposto termicamente.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    # 1. Imagem e Caixas Delimitadoras
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title("Exame Original com Detecções", fontsize=12)
    axes[0].axis('off')
    
    # Desenha Ground Truth (Verde)
    for box in gt_boxes:
        # box: [xmin, ymin, xmax, ymax]
        xmin, ymin, xmax, ymax = box
        rect = patches.Rectangle(
            (xmin, ymin), xmax - xmin, ymax - ymin,
            linewidth=2.5, edgecolor='#10b981', facecolor='none',
            label='Ground Truth (Especialista)'
        )
        axes[0].add_patch(rect)
        
    # Desenha Predições WSOD (Vermelho)
    for box in pred_boxes:
        xmin, ymin, xmax, ymax = box
        rect = patches.Rectangle(
            (xmin, ymin), xmax - xmin, ymax - ymin,
            linewidth=2, edgecolor='#f43f5e', facecolor='none',
            linestyle='--', label='Predição WSOD (CAM)'
        )
        axes[0].add_patch(rect)
        
    # Legenda única
    handles, labels = axes[0].get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    if by_label:
        axes[0].legend(by_label.values(), by_label.keys(), loc='upper right')

    # 2. Heatmap Sobreposto
    axes[1].imshow(image, cmap='gray')
    im = axes[1].imshow(cam_map, cmap='jet', alpha=0.45)
    axes[1].set_title("Mapa de Ativação Térmica (CAM)", fontsize=12)
    axes[1].axis('off')
    fig.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)

    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=200, bbox_inches='tight')
    plt.close(fig)
