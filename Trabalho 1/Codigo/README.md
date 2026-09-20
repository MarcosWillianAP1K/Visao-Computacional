# 🔬 Trabalho 1 - Segmentação de Imagens (Grupo 4)
**Universidade Federal do Piauí – UFPI**  
**Disciplina:** Tópicos Especiais em Visão Computacional — Prof. José Denes Lima Araújo  
**Tema:** Técnicas de Segmentação Baseada em Região (Seção 10.5 — Gonzalez & Woods)  
**Apresentador:** Integrante 3 — *O Analista Experimental (Prática, Particularidades & Fechamento)*  

---

## 📁 Estrutura de Arquivos

```
Trabalho 1/Codigo/
├── 01_watershed_segmentation.ipynb      # Notebook Jupyter principal de Watershed
├── 02_kmeans_segmentation.ipynb         # Notebook Jupyter principal de K-Means (L*a*b*)
├── 03_comparativo_watershed_vs_kmeans.ipynb # Notebook comparativo do Slide 11
├── 01_watershed_segmentation.py         # Script Python standalone equivalente
├── 02_kmeans_segmentation.py            # Script Python standalone equivalente
├── 03_comparativo_watershed_vs_kmeans.py# Script Python standalone equivalente
├── construir_trabalho.py                # Gerador/executor automatizado de notebooks
├── requirements.txt                     # Dependências do projeto
├── imagens/                             # Imagens de teste canônicas
│   ├── moedas_sobrepostas.jpg           # Imagem oficial de moedas tangentes
│   ├── cena_colorida.jpg                # Imagem fotográfica com planos bem definidos
│   ├── butterfly.jpg                    # Borboleta em vegetação
│   └── moedas_brasil.png                # Dataset de moedas adicionais
└── resultados/                          # Gráficos e figuras em alta resolução gerados
    ├── watershed_pipeline_completo.png  # Pipeline de 6 etapas do Watershed (Slide 9)
    ├── kmeans_comparativo_k.png         # Variação de K=2, 3, 5 no espaço L*a*b* (Slide 10)
    ├── kmeans_mascaras_k3.png           # Isolamento dos 3 clusters e máscaras
    └── comparativo_toque_watershed_vs_kmeans.png # Duelo Watershed vs K-Means (Slide 11)
```

---

## 🚀 Como Executar

### Opção 1: No Google Colab ou VS Code com Servidor do Colab (Recomendado)
1. Abra qualquer um dos arquivos `.ipynb` diretamente no **VS Code** ou faça o upload para o **Google Colab**.
2. Conecte-se ao runtime do Google Colab (ou ambiente local com Python 3).
3. Execute as células em ordem: os notebooks são **100% autossuficientes** e efetuam o download automático das imagens canônicas caso não estejam presentes no ambiente da nuvem.

### Opção 2: Linha de Comando (Scripts Python Standalone)
Caso queira executar os scripts via terminal local:
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar o Watershed
python 01_watershed_segmentation.py

# 3. Executar o K-Means
python 02_kmeans_segmentation.py

# 4. Executar o Comparativo Prático
python 03_comparativo_watershed_vs_kmeans.py
```
Todas as figuras resultantes serão salvas automaticamente na pasta `resultados/`.
