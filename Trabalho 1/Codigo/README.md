# Trabalho 1 - Segmentacao de Imagens (Grupo 4)
**Universidade Federal do Piaui - UFPI**  
**Disciplina:** Topicos Especiais em Visao Computacional - Prof. Jose Denes Lima Araujo  
**Tema:** Tecnicas de Segmentacao Baseada em Regiao (Secao 10.5 - Gonzalez & Woods)  
**Apresentador:** Integrante 3 (Analise Experimental e Codigo)

---

## Estrutura de Arquivos

```
Trabalho 1/Codigo/
├── 01_watershed_segmentation.ipynb          # Notebook de Watershed com Marcadores (Slide 9)
├── 02_kmeans_segmentation.ipynb             # Notebook de K-Means em espaco L*a*b* (Slide 10)
├── 03_comparativo_watershed_vs_kmeans.ipynb # Notebook comparativo de toque (Slide 11)
├── imagens/                                 # Imagens de teste canônicas
│   ├── moedas_sobrepostas.jpg
│   ├── cena_colorida.jpg
│   ├── butterfly.jpg
│   └── moedas_brasil.png
└── resultados/                              # Graficos gerados para os slides
    ├── watershed_pipeline_completo.png
    ├── kmeans_comparativo_k.png
    ├── kmeans_mascaras_k3.png
    └── comparativo_toque_watershed_vs_kmeans.png
```

---

## Como Executar no Google Colab ou VS Code

1. Abra qualquer um dos arquivos `.ipynb` diretamente no **VS Code** (usando a extensao Jupyter) ou faca o upload para o **Google Colab**.
2. Conecte ao runtime Python.
3. Execute as celulas em ordem. Todos os notebooks ja vem pre-executados e possuem rotina de download automatico caso as imagens nao estejam presentes no ambiente em nuvem.
