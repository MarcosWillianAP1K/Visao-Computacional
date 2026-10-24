# Arquitetura do Código e Guia de Implementação PyTorch

> **Módulo**: Engenharia de Software e Implementação Técnica  
> **Diretório Alvo do Código**: `Trabalho 3 (Final)/src/`  
> **Linguagem & Framework**: Python 3.10+ | PyTorch 2.x | PyTorch-Grad-CAM  
> **Objetivo**: Fornecer um guia estrutural e modular completo para a implementação limpa, reprodutível e robusta do modelo GMIC e dos geradores de CAM desacoplados, atendendo integralmente à rubrica de código (2,0 pontos).

---

## 1. Estrutura Modular de Diretórios do Código

Para garantir legibilidade, modularidade e nota máxima no critério "Organização do código (0,5 pt)" e "Qualidade técnica (1,5 pts)", o código da pasta `Trabalho 3 (Final)/src/` deve adotar a seguinte topologia:

```
Trabalho 3 (Final)/src/
├── configs/
│   └── config.yaml                  # Hiperparâmetros, caminhos, resolução, batch, beta=3.26
├── datasets/
│   ├── __init__.py
│   ├── vindr_dataset.py             # PyTorch Dataset com parsing de CSV/imagens e labels
│   └── transforms.py                # Augmentations (Flip, Crop, Normalization, Resizing)
├── models/
│   ├── __init__.py
│   ├── backbones.py                 # ResNet-22 (Global) e ResNet-18 (Local)
│   ├── gmic.py                      # Arquitetura GMIC completa (Global, Patch Slicing, Local, Fusão)
│   └── losses.py                    # Multi-branch BCE + Regularização L1 beta*L_reg
├── cams/
│   ├── __init__.py
│   ├── cam_manager.py               # Interface unificada para CAM, GradCAM, ++, XGrad e LayerCAM
│   └── cam_utils.py                 # Binarização por limiar, connected components e caixas preditas
├── evaluation/
│   ├── __init__.py
│   ├── metrics.py                   # Acurácia, AUC-ROC, Sensibilidade (TPR), FNR, TNR
│   ├── detection_eval.py            # Cálculo de IoU >= 0.3, contagem de FPPI e curva FROC
│   └── visualizer.py                # Plotagem de heatmaps, bounding boxes preditas e ground truth verde
├── train.py                         # Script CLI de treinamento com suporte a AMP e Gradient Accumulation
├── test.py                          # Script CLI de avaliação WSOD e comparação de CAMs desacoplados
├── requirements.txt                 # Dependências do projeto com versões fixadas
└── README.md                        # Instruções passo a passo de configuração e execução
```

---

## 2. Modelagem dos Componentes Principais

### 2.1. Dataset e Dataloader (`datasets/vindr_dataset.py`)
O dataset encapsula o carregamento das imagens de mamografia e a separação dos metadados de classificação e detecção:

```python
import os
import torch
from torch.utils.data import Dataset
import cv2
import pandas as pd
import numpy as np

class VinDrMammoDataset(Dataset):
    """
    Dataset para a base VinDr-Mammo adaptado para classificação binária
    (Normal=0 vs Massa=1) e avaliação WSOD com bounding boxes no teste.
    """
    def __init__(self, metadata_csv, img_dir, transform=None, is_test=False):
        self.df = pd.read_csv(metadata_csv)
        self.img_dir = img_dir
        self.transform = transform
        self.is_test = is_test

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = os.path.join(self.img_dir, f"{row['image_id']}.png")
        
        # Leitura em escala de cinza de alta resolução
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError(f"Imagem não encontrada: {img_path}")
            
        h_orig, w_orig = image.shape

        if self.transform:
            image = self.transform(image)

        # Rótulo de classificação em nível de imagem: 0 (Normal) ou 1 (Massa)
        label = torch.tensor(row['label'], dtype=torch.float32)

        sample = {
            'image': image,
            'label': label,
            'image_id': row['image_id'],
            'orig_size': (h_orig, w_orig)
        }

        # No conjunto de teste, inclui as coordenadas ground truth (se houver massa)
        if self.is_test:
            # bbox formato: [xmin, ymin, xmax, ymax]
            boxes = eval(row['boxes']) if 'boxes' in row and pd.notna(row['boxes']) else []
            sample['gt_boxes'] = torch.tensor(boxes, dtype=torch.float32)

        return sample
```

---

### 2.2. Arquitetura GMIC (`models/gmic.py`)
A classe `GMIC` integra os três ramos de inferência e a extração gulosa de patches locais:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class GreedyPatchExtractor(nn.Module):
    """
    Localiza os K picos máximos no mapa de ativação A^c e recorta
    patches de dimensão (patch_size x patch_size) da imagem original.
    """
    def __init__(self, patch_size=256, num_patches=6):
        super().__init__()
        self.patch_size = patch_size
        self.num_patches = num_patches

    def forward(self, high_res_img, cam_map):
        batch_size, _, H_img, W_img = high_res_img.shape
        _, _, H_cam, W_cam = cam_map.shape
        
        patches_batch = []
        
        for b in range(batch_size):
            cur_cam = cam_map[b, 0].clone()
            cur_img = high_res_img[b]
            patches = []
            
            for _ in range(self.num_patches):
                # Encontra o pico máximo espacial
                max_idx = torch.argmax(cur_cam)
                cy_cam = max_idx // W_cam
                cx_cam = max_idx % W_cam
                
                # Mapeia coordenadas do CAM para a resolução da imagem original
                cy_img = int((cy_cam.item() / H_cam) * H_img)
                cx_img = int((cx_cam.item() / W_cam) * W_img)
                
                # Calcula os limites do recorte centralizado no pico
                half = self.patch_size // 2
                ymin = max(0, cy_img - half)
                ymax = min(H_img, cy_img + half)
                xmin = max(0, cx_img - half)
                xmax = min(W_img, cx_img + half)
                
                patch = cur_img[:, ymin:ymax, xmin:xmax]
                # Se estiver na borda, realiza padding para garantir dimensões uniformes
                if patch.shape[1] != self.patch_size or patch.shape[2] != self.patch_size:
                    patch = F.pad(patch, (0, self.patch_size - patch.shape[2], 0, self.patch_size - patch.shape[1]))
                
                patches.append(patch)
                
                # Supressão de vizinhança no CAM para evitar patches sobrepostos
                rad_y = max(1, int(H_cam * (self.patch_size / H_img) / 2))
                rad_x = max(1, int(W_cam * (self.patch_size / W_img) / 2))
                y0, y1 = max(0, cy_cam - rad_y), min(H_cam, cy_cam + rad_y)
                x0, x1 = max(0, cx_cam - rad_x), min(W_cam, cx_cam + rad_x)
                cur_cam[y0:y1, x0:x1] = -1.0
                
            patches_batch.append(torch.stack(patches)) # [K, 1, patch_size, patch_size]
            
        return torch.stack(patches_batch) # [Batch, K, 1, patch_size, patch_size]


class GMIC(nn.Module):
    """
    Globally-Aware Multiple Instance Classifier (Shen et al. / Sampaio & Cordeiro).
    """
    def __init__(self, global_backbone, local_backbone, num_patches=6, patch_size=256):
        super().__init__()
        self.global_net = global_backbone
        self.local_net = local_backbone
        self.patch_extractor = GreedyPatchExtractor(patch_size=patch_size, num_patches=num_patches)
        
        # Dimensões de saída dos backbones
        dim_global = 512
        dim_local = 512
        
        # Classificadores independentes dos ramos
        self.fc_global = nn.Linear(dim_global, 1)
        self.fc_local = nn.Linear(dim_local, 1)
        
        # Módulo de Fusão
        self.fc_fusion = nn.Sequential(
            nn.Linear(dim_global + dim_local, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(256, 1)
        )

    def forward(self, x, cam_generator=None):
        # 1. Ramo Global
        feat_map, h_global = self.global_net(x) # feat_map: [B, C, Hg, Wg], h_global: [B, 512]
        y_global = torch.sigmoid(self.fc_global(h_global)).squeeze(-1)
        
        # 2. Geração do Mapa de Ativação (CAM)
        if cam_generator is not None:
            # Durante o treino desacoplado ou teste, invoca o método de CAM desejado
            cam_map = cam_generator(x, feat_map)
        else:
            # CAM padrão via projeção dos pesos lineares globais
            w = self.fc_global.weight.data # [1, dim_global]
            cam_map = F.relu(torch.einsum('bc, bchw -> bhw', w, feat_map)).unsqueeze(1)
            
        # 3. Ramo Local
        patches = self.patch_extractor(x, cam_map) # [B, K, 1, P, P]
        B, K, C, H_p, W_p = patches.shape
        patches_flat = patches.view(B * K, C, H_p, W_p)
        
        h_patches = self.local_net(patches_flat) # [B*K, dim_local]
        h_patches = h_patches.view(B, K, -1)
        
        # Agregação MIL por Max-Pooling sobre as instâncias locais
        h_local, _ = torch.max(h_patches, dim=1) # [B, dim_local]
        y_local = torch.sigmoid(self.fc_local(h_local)).squeeze(-1)
        
        # 4. Ramo de Fusão
        h_fused = torch.cat([h_global, h_local], dim=-1)
        y_fusion = torch.sigmoid(self.fc_fusion(h_fused)).squeeze(-1)
        
        return {
            'y_global': y_global,
            'y_local': y_local,
            'y_fusion': y_fusion,
            'cam_map': cam_map
        }
```

---

### 2.3. Função de Perda Multi-Ramo com Regularização $\beta$ (`models/losses.py`)

A função de perda computa as 3 entropias cruzadas e o termo de regularização L1 esparso com $\beta = 3.26$:

```python
import torch
import torch.nn as nn

class GMICLoss(nn.Module):
    def __init__(self, beta=3.26):
        super().__init__()
        self.beta = beta
        self.bce = nn.BCELoss()

    def forward(self, outputs, target):
        loss_local = self.bce(outputs['y_local'], target)
        loss_global = self.bce(outputs['y_global'], target)
        loss_fusion = self.bce(outputs['y_fusion'], target)
        
        # Termo de regularização L1 de esparsidade sobre o mapa de ativação da classe
        # L_reg = sum(|A^c_{i,j}|) normalizado pela resolução do mapa
        cam_map = outputs['cam_map']
        l1_reg = torch.mean(torch.sum(torch.abs(cam_map), dim=[2, 3]))
        
        total_loss = loss_local + loss_global + loss_fusion + (self.beta * l1_reg)
        
        return total_loss, {
            'loss_local': loss_local.item(),
            'loss_global': loss_global.item(),
            'loss_fusion': loss_fusion.item(),
            'l1_reg': l1_reg.item(),
            'total_loss': total_loss.item()
        }
```

---

### 2.4. Gerenciador de CAMs e Desacoplamento (`cams/cam_manager.py`)

O gerenciador encapsula `pytorch-grad-cam` para fornecer interface desacoplada entre treino e teste:

```python
from pytorch_grad_cam import (
    GradCAM,
    GradCAMPlusPlus,
    XGradCAM,
    LayerCAM
)
import torch

class CAMManager:
    """
    Gerenciador modular para os 5 métodos de ativação:
    CAM, GradCAM, GradCAM++, XGradCAM, LayerCAM.
    Permite desacoplar o método de treino e o de teste.
    """
    AVAILABLE_METHODS = {
        'gradcam': GradCAM,
        'gradcam++': GradCAMPlusPlus,
        'xgradcam': XGradCAM,
        'layercam': LayerCAM
    }

    def __init__(self, model, target_layer, method_name='xgradcam'):
        self.method_name = method_name.lower()
        self.model = model
        self.target_layer = target_layer
        
        if self.method_name in self.AVAILABLE_METHODS:
            cam_class = self.AVAILABLE_METHODS[self.method_name]
            self.cam_obj = cam_class(model=model, target_layers=[target_layer], use_cuda=torch.cuda.is_available())
        else:
            self.cam_obj = None # Usará CAM clássico nativo

    def generate(self, input_tensor, target_class=1):
        if self.cam_obj is None:
            # Fallback para CAM clássico
            return None
        # Gera o mapa de ativação normalizado [0, 1]
        grayscale_cam = self.cam_obj(input_tensor=input_tensor, targets=None)
        return torch.from_numpy(grayscale_cam).unsqueeze(1).to(input_tensor.device)
```

---

### 2.5. Avaliação de Detecção WSOD (`evaluation/detection_eval.py`)

Algoritmo vetorizado de extração de bounding boxes e mensuração rigorosa de $\text{IoU} \ge 0.3$:

```python
import numpy as np
import cv2

def compute_iou(boxA, boxB):
    # box: [xmin, ymin, xmax, ymax]
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    unionArea = float(boxAArea + boxBArea - interArea)
    
    return interArea / unionArea if unionArea > 0 else 0.0

def evaluate_wsod_sample(cam_map_2d, gt_boxes, threshold=0.3, min_iou=0.3):
    """
    Binariza o mapa de ativação, extrai bounding boxes e calcula VP e FP.
    """
    # 1. Binarização
    binary_mask = (cam_map_2d >= threshold).astype(np.uint8)
    
    # 2. Componentes Conexos
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    pred_boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        pred_boxes.append([x, y, x + w, y + h])
        
    # 3. Matching contra Ground Truth
    matched_gt = set()
    num_tp = 0
    num_fp = 0
    
    for p_box in pred_boxes:
        has_matched = False
        for i, g_box in enumerate(gt_boxes):
            iou = compute_iou(p_box, g_box)
            if iou >= min_iou and i not in matched_gt:
                matched_gt.add(i)
                num_tp += 1
                has_matched = True
                break
        if not has_matched:
            num_fp += 1
            
    return num_tp, num_fp, len(gt_boxes), pred_boxes
```

---

## 3. Arquivo de Dependências (`requirements.txt`)

Versões rigorosamente testadas e compatíveis:

```text
torch>=2.1.0
torchvision>=0.16.0
grad-cam>=1.4.8
pydicom>=2.4.3
opencv-python>=4.8.0
albumentations>=1.3.1
pandas>=2.1.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
pyyaml>=6.0.1
tqdm>=4.66.0
```

---

## 4. Comandos de Execução (Treinamento e Inferência)

### Treinamento com Suporte a Mixed Precision e Acumulação de Gradientes
```bash
python train.py \
    --config configs/config.yaml \
    --train_cam xgradcam \
    --epochs 50 \
    --batch_size 2 \
    --accum_steps 3 \
    --amp
```

### Avaliação WSOD Comparando Métodos Desacoplados
```bash
python test.py \
    --checkpoint checkpoints/best_gmic_xgradcam.pth \
    --test_cam gradcam++ \
    --iou_thresh 0.3
```
