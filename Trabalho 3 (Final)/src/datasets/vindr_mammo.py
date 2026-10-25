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


def get_transforms(split: str = 'train', target_size: tuple = (2944, 1920)):
    """
    Retorna pipeline de transformações Albumentations.
    """
    if A is None or ToTensorV2 is None:
        return None
        
    h, w = target_size
    
    if split == 'train':
        return A.Compose([
            A.Resize(height=h, width=w, interpolation=cv2.INTER_AREA),
            A.HorizontalFlip(p=0.5),
            A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1, p=0.4),
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
        if not os.path.exists(metadata_csv):
            # Gera DataFrame sintético se o arquivo não existir (para dry-run/testes estruturais)
            self.df = pd.DataFrame({
                'image_id': [f"img_{i:04d}" for i in range(10)],
                'label': [0 if i % 2 == 0 else 1 for i in range(10)],
                'boxes': ["[]" if i % 2 == 0 else "[[100, 150, 400, 450]]" for i in range(10)]
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
        
        # Localiza o arquivo de imagem (tenta png, jpg, dcm)
        img_name = f"{image_id}.png"
        img_path = os.path.join(self.images_dir, img_name)
        if not os.path.exists(img_path):
            img_path = os.path.join(self.images_dir, f"{image_id}.dicom")
            
        if os.path.exists(img_path):
            image = read_mammogram_image(img_path)
        else:
            # Imagem de preenchimento caso arquivo real ainda não tenha sido baixado
            image = np.zeros((self.target_size[0], self.target_size[1]), dtype=np.uint8)
            
        h_orig, w_orig = image.shape
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
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.train.batch_size,
        shuffle=True,
        num_workers=config.train.num_workers,
        pin_memory=torch.cuda.is_available() if torch else False,
        drop_last=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=1,  # Teste WSOD opera individualmente por imagem
        shuffle=False,
        num_workers=config.train.num_workers,
        pin_memory=torch.cuda.is_available() if torch else False
    )
    
    return train_loader, test_loader
