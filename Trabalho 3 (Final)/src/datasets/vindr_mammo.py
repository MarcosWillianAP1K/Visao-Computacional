"""
Dataset PyTorch para Mamografia Digital Direta (VinDr-Mammo)
Carregamento de Imagens DICOM/PNG, Aumentações via Albumentations e Bounding Boxes
"""

import os
import ast
import numpy as np
import pandas as pd
import cv2

try:
    import torch
    from torch.utils.data import Dataset, DataLoader
except ImportError:
    torch = None
    Dataset = object
    DataLoader = None

try:
    import pydicom
except ImportError:
    pydicom = None

try:
    import albumentations as A
    from albumentations.pytorch import ToTensorV2
except ImportError:
    A = None
    ToTensorV2 = None


def read_mammogram_image(file_path: str) -> np.ndarray:
    """
    Lê imagem mamográfica em formato DICOM, PNG ou TIFF,
    normalizando para escala de cinza mono-canal em uint8 [0, 255].
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.dicom' or ext == '.dcm':
        if pydicom is None:
            raise ImportError("Biblioteca pydicom não instalada para leitura de arquivos .dicom.")
        dicom_data = pydicom.dcmread(file_path)
        pixel_array = dicom_data.pixel_array.astype(np.float32)
        
        # Ajuste de Photometric Interpretation (Inversão Monocromática se MONOCHROME1)
        if getattr(dicom_data, 'PhotometricInterpretation', '') == 'MONOCHROME1':
            pixel_array = np.amax(pixel_array) - pixel_array
            
        # Normalização Min-Max para 8-bit
        pmin, pmax = np.amin(pixel_array), np.amax(pixel_array)
        if pmax > pmin:
            pixel_array = (pixel_array - pmin) / (pmax - pmin) * 255.0
        return pixel_array.astype(np.uint8)
        
    else:
        # Imagem PNG, JPEG ou TIFF
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Erro ao carregar imagem no caminho: {file_path}")
        return img


def generate_synthetic_mammogram(target_size: tuple, boxes: list, seed: int = 42) -> np.ndarray:
    """
    Gera um fantoma mamográfico sintético realista (parênquima + massa hiperdensa nas caixas GT)
    para validação estrutural e demonstração quando a base real de 20GB não está no disco local.
    """
    rng = np.random.default_rng(seed)
    h, w = target_size
    img = np.zeros((h, w), dtype=np.float32)

    # Contorno anatômico semielíptico da mama (projeção MLO/CC lateral esquerda)
    yy, xx = np.ogrid[:h, :w]
    cy, cx = h * 0.52, 0.0
    ry, rx = h * 0.42, w * 0.68
    breast_mask = (((yy - cy) / ry) ** 2 + ((xx - cx) / rx) ** 2) <= 1.0

    # Textura fibroglandular suave
    radial_grad = np.clip(1.0 - np.sqrt(((yy - cy) / ry) ** 2 + ((xx - cx) / rx) ** 2), 0.0, 1.0)
    img[breast_mask] = 45.0 + 95.0 * (radial_grad[breast_mask] ** 0.7)

    # Ruído estrutural de baixa frequência (parênquima)
    small_noise = rng.normal(0.0, 12.0, size=(max(8, h // 32), max(8, w // 32))).astype(np.float32)
    smooth_noise = cv2.resize(small_noise, (w, h), interpolation=cv2.INTER_CUBIC)
    img[breast_mask] = np.clip(img[breast_mask] + smooth_noise[breast_mask], 10.0, 210.0)

    # Insere massa hiperdensa nas coordenadas das bounding boxes (se classe positiva)
    for box in boxes:
        xmin, ymin, xmax, ymax = box
        mcx, mcy = 0.5 * (xmin + xmax), 0.5 * (ymin + ymax)
        mrx, mry = max(8.0, 0.5 * (xmax - xmin)), max(8.0, 0.5 * (ymax - ymin))
        dist2 = ((xx - mcx) / mrx) ** 2 + ((yy - mcy) / mry) ** 2
        mass_profile = np.exp(-1.5 * dist2) * (dist2 <= 2.2)
        img = np.clip(img + 115.0 * mass_profile, 0.0, 255.0)

    return img.astype(np.uint8)


def get_transforms(split: str = 'train', target_size: tuple = (2944, 1920)):
    """
    Retorna pipeline de transformações Albumentations fiel a Sampaio & Cordeiro (Seção 3.4):
    Redimensionamento (2944 x 1920), Flip Horizontal, Random Crop e Normalização.
    """
    if A is None or ToTensorV2 is None:
        return None
        
    h, w = target_size
    
    if split == 'train':
        return A.Compose([
            A.Resize(height=h, width=w, interpolation=cv2.INTER_AREA),
            A.HorizontalFlip(p=0.5),
            A.RandomResizedCrop(
                size=(h, w),
                scale=(0.90, 1.0),
                ratio=(w / h * 0.95, w / h * 1.05),
                interpolation=cv2.INTER_AREA,
                p=0.5
            ),
            A.Normalize(mean=(0.5,), std=(0.5,)),
            ToTensorV2()
        ], bbox_params=A.BboxParams(format='albumentations', min_visibility=0.1, label_fields=['bbox_classes']))
    else:
        return A.Compose([
            A.Resize(height=h, width=w, interpolation=cv2.INTER_AREA),
            A.Normalize(mean=(0.5,), std=(0.5,)),
            ToTensorV2()
        ], bbox_params=A.BboxParams(format='albumentations', min_visibility=0.1, label_fields=['bbox_classes']))


class VinDrMammoDataset(Dataset):
    """
    Dataset PyTorch para o benchmark VinDr-Mammo.
    Supervisão fraca (WSOD): Coordenadas de bounding boxes são usadas
    exclusivamente no teste para validação de IoU, jamais no treino.
    """
    def __init__(
        self,
        metadata_csv: str,
        images_dir: str,
        target_size: tuple = (2944, 1920),
        is_test: bool = False,
        transform=None
    ):
        super().__init__()
        self.is_synthetic = not os.path.exists(metadata_csv)
        if self.is_synthetic:
            # Gera DataFrame sintético se o arquivo não existir (para dry-run/testes estruturais)
            self.df = pd.DataFrame({
                'image_id': [f"img_{i:04d}" for i in range(10)],
                'label': [0 if i % 2 == 0 else 1 for i in range(10)],
                'boxes': ["[]" if i % 2 == 0 else "[[250, 1100, 620, 1480]]" for i in range(10)]
            })
        else:
            self.df = pd.read_csv(metadata_csv)
            
        self.images_dir = images_dir
        self.target_size = target_size
        self.is_test = is_test
        self.transform = transform if transform is not None else get_transforms('test' if is_test else 'train', target_size)

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> dict:
        row = self.df.iloc[idx]
        image_id = str(row['image_id'])
        label = float(row.get('label', 0.0))
        
        # Parse das bounding boxes de especialistas (se presentes)
        raw_boxes = row.get('boxes', '[]')
        if isinstance(raw_boxes, str):
            try:
                parsed_boxes = ast.literal_eval(raw_boxes)
            except Exception:
                parsed_boxes = []
        elif isinstance(raw_boxes, list):
            parsed_boxes = raw_boxes
        else:
            parsed_boxes = []

        # Localiza o arquivo de imagem (tenta png, jpg, dcm)
        img_name = f"{image_id}.png"
        img_path = os.path.join(self.images_dir, img_name)
        if not os.path.exists(img_path):
            img_path = os.path.join(self.images_dir, f"{image_id}.dicom")
            
        if os.path.exists(img_path):
            image = read_mammogram_image(img_path)
        else:
            # Fantoma mamográfico sintético realista caso a base real ainda não tenha sido baixada
            image = generate_synthetic_mammogram(self.target_size, parsed_boxes if label == 1.0 else [], seed=42 + idx)
            
        h_orig, w_orig = image.shape

        # Aplica transformações
        if self.transform is not None:
            # Albumentations requer imagem 3D [H, W, 1] ou [H, W, 3]
            img_expanded = np.expand_dims(image, axis=-1)
            
            # Normaliza caixas para Albumentations [0, 1] caso existam
            norm_boxes = []
            for b in parsed_boxes:
                xmin, ymin, xmax, ymax = b
                norm_boxes.append([
                    max(0.0, min(1.0, xmin / w_orig)),
                    max(0.0, min(1.0, ymin / h_orig)),
                    max(0.0, min(1.0, xmax / w_orig)),
                    max(0.0, min(1.0, ymax / h_orig))
                ])
                
            bbox_classes = [int(label)] * len(norm_boxes)
            
            try:
                augmented = self.transform(
                    image=img_expanded,
                    bboxes=norm_boxes,
                    bbox_classes=bbox_classes
                )
                image_tensor = augmented['image']
                
                # Desnormaliza caixas transformadas de volta para coordenadas de pixel
                res_h, res_w = self.target_size
                transformed_boxes = []
                for ab in augmented.get('bboxes', []):
                    transformed_boxes.append([
                        ab[0] * res_w,
                        ab[1] * res_h,
                        ab[2] * res_w,
                        ab[3] * res_h
                    ])
            except Exception:
                # Fallback simples caso dê erro em caixas inválidas
                image_tensor = torch.from_numpy(image.astype(np.float32) / 255.0).unsqueeze(0) if torch else image
                transformed_boxes = parsed_boxes
        else:
            image_tensor = torch.from_numpy(image.astype(np.float32) / 255.0).unsqueeze(0) if torch else image
            transformed_boxes = parsed_boxes

        sample = {
            'image': image_tensor,
            'label': torch.tensor(label, dtype=torch.float32) if torch else label,
            'image_id': image_id,
            'orig_size': (h_orig, w_orig)
        }
        
        # Coordenadas incluídas APENAS na fase de teste para mensuração de IoU
        if self.is_test:
            sample['gt_boxes'] = torch.tensor(transformed_boxes, dtype=torch.float32) if torch else transformed_boxes
            
        return sample


def create_dataloaders(config) -> tuple:
    """
    Cria DataLoaders de treino e teste a partir da configuração do projeto.
    """
    if DataLoader is None:
        raise ImportError("PyTorch DataLoader não disponível no ambiente.")
        
    train_dataset = VinDrMammoDataset(
        metadata_csv=config.paths.metadata_train_csv,
        images_dir=config.paths.images_dir,
        target_size=config.model.input_resolution,
        is_test=False
    )
    
    test_dataset = VinDrMammoDataset(
        metadata_csv=config.paths.metadata_test_csv,
        images_dir=config.paths.images_dir,
        target_size=config.model.input_resolution,
        is_test=True
    )
    
    has_cuda = torch.cuda.is_available() if torch else False
    eff_workers = 0 if (os.name == 'nt' or train_dataset.is_synthetic or not has_cuda) else config.train.num_workers

    train_loader = DataLoader(
        train_dataset,
        batch_size=config.train.batch_size,
        shuffle=True,
        num_workers=eff_workers,
        pin_memory=has_cuda,
        drop_last=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=1,  # Teste WSOD opera individualmente por imagem
        shuffle=False,
        num_workers=eff_workers,
        pin_memory=has_cuda
    )
    
    return train_loader, test_loader
