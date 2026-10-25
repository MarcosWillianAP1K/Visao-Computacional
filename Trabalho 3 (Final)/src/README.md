# Base de Código Modular PyTorch — GMIC & WSOD em Mamografia

> **Disciplina**: Tópicos Especiais em Visão Computacional (UFPI / CSHNB)  
> **Docente**: Prof. Dr. José Denes Lima Araújo  
> **Equipe**: Grupo 4  
> **Artigo Reproduzido**: *"A Study on Class Activation Map Methods to Detect Masses in Mammography Images using Weakly Supervised Learning"* (Sampaio & Cordeiro — UFRPE, SBC 2022)

---

## 1. Visão Geral da Arquitetura de Software

Esta base de código implementa de forma desacoplada, modular e orientada a objetos o modelo **GMIC (Globally-Aware Multiple Instance Classifier)** e o ecossistema de **5 geradores de Mapas de Ativação de Classe (CAM)**, permitindo investigar o desacoplamento de saliência entre treinamento e teste para detecção fracamente supervisionada de objetos (WSOD).

```
Trabalho 3 (Final)/src/
├── config.py                 # Hiperparâmetros, resoluções, batch size e beta=3.26
├── requirements.txt          # Dependências do projeto com versões fixadas
├── utils.py                  # Reprodutibilidade (seed), logging e visualização de calor
├── datasets/
│   ├── __init__.py
│   └── vindr_mammo.py        # Leitor DICOM/PNG, Albumentations e parsing de bboxes
├── models/
│   ├── __init__.py
│   ├── backbones.py          # ResNet-22 global e ResNet-18 local
│   ├── gmic.py               # Arquitetura GMIC completa (Global, Patches, Local, Fusão)
│   └── losses.py             # Multi-branch BCE + Regularização de esparsidade L1 (beta=3.26)
├── cams/
│   ├── __init__.py
│   └── cam_manager.py        # Interface desacoplada para CAM, GradCAM, ++, XGrad e LayerCAM
├── evaluation/
│   ├── __init__.py
│   └── metrics.py            # Acurácia, AUC-ROC, TPR, TNR, IoU >= 0.3 e FPPI
├── train.py                  # Script CLI de treinamento com AMP (FP16) e Acumulação
├── test.py                   # Script CLI de inferência, avaliação e geração de Tabelas 1 e 2
└── README.md                 # Este guia técnico de execução
```

---

## 2. Instalação e Requisitos de Ambiente

Recomenda-se a utilização de um ambiente virtual Python (Conda ou `venv`):

```bash
# 1. Criação do ambiente virtual
python -m venv venv_gmic
source venv_gmic/bin/activate   # No Linux/Mac
# ou: .\venv_gmic\Scripts\activate  # No Windows

# 2. Instalação das dependências
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Estruturação do Dataset VinDr-Mammo

Os dados devem ser organizados na pasta `data/vindr-mammo/` (ou caminho especificado em `config.py`):

```
data/vindr-mammo/
├── images/
│   ├── {image_id}.png (ou .dicom)
│   └── ...
├── train_metadata.csv       # 1.978 imagens (989 Normais, 989 Massas)
└── test_metadata.csv        # 474 imagens (237 Normais, 237 Massas com boxes)
```

O arquivo `test_metadata.csv` contém as seguintes colunas obrigatórias:
- `image_id`: Identificador único do exame mamográfico.
- `label`: `0` (Normal) ou `1` (Massa).
- `boxes`: Lista de coordenadas no formato `[[xmin, ymin, xmax, ymax], ...]`.

> **Isolamento de Supervisão (WSOD)**: As coordenadas espaciais são ignoradas e ocultadas durante todo o treinamento, sendo carregadas unicamente na rotina de inferência (`test.py`) para cálculo do $\text{IoU} \ge 0.3$.

---

## 4. Instruções de Treinamento (`train.py`)

O script `train.py` conta com suporte nativo a **Automatic Mixed Precision (AMP FP16)** e **Acumulação de Gradientes** para viabilizar o processamento de imagens de altíssima resolução sem erro de memória (`CUDA Out of Memory`):

### Exemplo de Treino com Modelo Campeão (XGrad-CAM no Treino):
```bash
python train.py \
    --train_cam xgradcam \
    --epochs 50 \
    --batch_size 2 \
    --accum_steps 3 \
    --lr 0.0001 \
    --beta 3.26 \
    --amp \
    --save_dir checkpoints
```

*Nota*: `batch_size = 2` com `accum_steps = 3` resulta em um **batch virtual exato de 6 imagens**, equivalente à configuração canônica de Shen et al. e Sampaio & Cordeiro.

---

## 5. Instruções de Teste e Inferência (`test.py`)

O script `test.py` avalia a classificação global (Tabela 1) e executa a varredura de detecção espacial de massas (Tabela 2):

### A. Avaliar Combinação Campeã Desacoplada:
Treinada com XGrad-CAM e avaliada no teste com Grad-CAM++:
```bash
python test.py \
    --checkpoint checkpoints/best_model.pth \
    --test_cam gradcam++ \
    --iou_thresh 0.3 \
    --cam_thresh 0.3 \
    --save_heatmaps \
    --output_dir results
```

### B. Avaliar Toda a Matriz Desacoplada (5 CAMs):
Executa os 5 geradores de CAM e reproduz a matriz completa da Tabela 2:
```bash
python test.py \
    --checkpoint checkpoints/best_model.pth \
    --test_cam all \
    --output_dir results
```

Os resultados formatados são impressos no terminal e exportados para `results/relatorio_avaliacao_tabelas.txt`.

---

## 6. Verificação de Sintaxe e Testes Estruturais

Para certificar que todos os módulos estão íntegros e sem erros de sintaxe:
```bash
python -m py_compile config.py utils.py datasets/*.py models/*.py cams/*.py evaluation/*.py train.py test.py
```
