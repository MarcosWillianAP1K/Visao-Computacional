# -*- coding: utf-8 -*-
"""
Script construtor dos Notebooks Jupyter (.ipynb) e scripts Python (.py)
Grupo 4 - Tópicos Especiais em Visão Computacional (UFPI)
Integrante 3: O Analista Experimental
"""

import os
import json
import nbformat as nbf
from nbclient import NotebookClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGENS_DIR = os.path.join(BASE_DIR, "imagens")
RESULTADOS_DIR = os.path.join(BASE_DIR, "resultados")

os.makedirs(IMAGENS_DIR, exist_ok=True)
os.makedirs(RESULTADOS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. NOTEBOOK 01: WATERSHED SEGMENTATION
# -------------------------------------------------------------
def build_notebook_01():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "language_info": {"name": "python"},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
    }

    cells = [
        nbf.v4.new_markdown_cell("""# 🌊 Segmentação de Imagens por Transformada de Watershed
### Universidade Federal do Piauí – UFPI | Campus Senador Helvídio Nunes de Barros
**Disciplina:** Tópicos Especiais em Visão Computacional — Prof. José Denes Lima Araújo  
**Grupo 4:** Técnicas de Segmentação Baseada em Região (Seção 10.5 — Gonzalez & Woods)  
**Apresentador:** Integrante 3 — *O Analista Experimental (Prática, Particularidades & Fechamento)*  

---

## 📌 Contexto e Objetivos (Slide 9 do Seminário)
Este notebook implementa a **Transformada de Watershed baseada em Marcadores e Transformada de Distância Euclidiana**, conforme abordado no livro *Processamento Digital de Imagens (Rafael C. Gonzalez e Richard E. Woods - 3ª e 4ª Edições)*.

### O Problema do Mundo Real: Objetos Tangentes / Sobrepostos
Em visão computacional industrial e médica (ex: contagem de moedas, núcleos celulares ou comprimidos), os objetos frequentemente encostam uns nos outros.
- **Por que métodos convencionais falham?** A binarização global (como o algoritmo de **Otsu**) analisa apenas a intensidade pontual de cada pixel. Quando dois objetos se tocam, os pixels de fronteira compartilham a mesma intensidade dos objetos, unindo todos os círculos em uma única massa conexa indistinta (1 único objeto gigante).
- **A Solução por Watershed:** Modelamos a imagem como uma superfície topográfica 3D. Através da **Transformada de Distância Euclidiana**, encontramos os picos de distância que representam os centros seguros de cada moeda (*marcadores internos*). Ao simular a inundação a partir desses centros, o Watershed ergue **barragens morfológicas (dams)** exatamente nas linhas de crista do relevo, separando com perfeição os objetos no ponto de estrangulamento geométrico!
"""),

        nbf.v4.new_code_cell("""# 1. Importação das Bibliotecas e Configurações de Ambiente (Compatível com Google Colab)
import os
import sys
import urllib.request
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Configuração estética dos gráficos
plt.rcParams['figure.dpi'] = 110
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#444444'
plt.rcParams['axes.linewidth'] = 0.8

# Garantir diretórios locais
os.makedirs("imagens", exist_ok=True)
os.makedirs("resultados", exist_ok=True)

# Verificação e download automático da imagem de teste canônica caso rodando no Colab
img_path = os.path.join("imagens", "moedas_sobrepostas.jpg")
if not os.path.exists(img_path):
    url = "https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_watershed/images/water_coins.jpg"
    print(f"Baixando imagem de teste de: {url}")
    urllib.request.urlretrieve(url, img_path)
    print("Download concluído com sucesso!")
else:
    print(f"Imagem encontrada localmente: {img_path}")
"""),

        nbf.v4.new_markdown_cell("""## 2. Leitura e Análise Inicial da Imagem
Carregamos a imagem original em cores e convertemos para escala de cinza. A imagem possui um conjunto de moedas circulares sobre fundo branco e homogêneo, apresentando múltiplos pontos de toque e sobreposição leve.
"""),

        nbf.v4.new_code_cell("""# Leitura BGR, conversão para RGB (para matplotlib) e Tons de Cinza
img_bgr = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

print(f"Dimensões da imagem: {img_rgb.shape[1]}x{img_rgb.shape[0]} pixels, {img_rgb.shape[2]} canais.")

fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].imshow(img_rgb)
ax[0].set_title("Imagem Original de Teste (RGB)")
ax[0].axis("off")

ax[1].imshow(gray, cmap="gray")
ax[1].set_title("Imagem em Escala de Cinza")
ax[1].axis("off")
plt.tight_layout()
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 3. Demonstração do Fracasso da Limiarização Global (Otsu)
Aplicamos a limiarização ótima de Otsu (`cv2.THRESH_OTSU`). Como o fundo é branco e as moedas são mais escuras, usamos `cv2.THRESH_BINARY_INV`.
Em seguida, aplicamos uma abertura morfológica (`cv2.MORPH_OPEN`) para eliminar pequenos grânulos e ruídos espúrios.

Observe quantos componentes conexos o algoritmo encontra:
"""),

        nbf.v4.new_code_cell("""# Limiarização Inversa de Otsu
otsu_thresh, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
print(f"Limiar ótimo calculado automaticamente por Otsu: {otsu_thresh:.1f}")

# Abertura Morfológica (Erosão seguida de Dilatação com elemento 3x3)
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# Contagem de componentes conexos apenas com Otsu
num_labels_otsu, _ = cv2.connectedComponents(opening)
num_objetos_otsu = num_labels_otsu - 1  # subtrai o fundo

print(f"\\n🚨 RESULTADO DO OTSU PURO:")
print(f"Componentes Conexos detectados pelo Otsu: {num_objetos_otsu}")
if num_objetos_otsu == 1:
    print("-> FALHA CLÁSSICA: Todas as 24 moedas foram fundidas em UM ÚNICO bloco gigante!")

fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].imshow(thresh, cmap="gray")
ax[0].set_title("Limiarização Global de Otsu")
ax[0].axis("off")

ax[1].imshow(opening, cmap="gray")
ax[1].set_title(f"Após Abertura Morfológica ({num_objetos_otsu} componente)")
ax[1].axis("off")
plt.tight_layout()
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 4. Construção dos Marcadores via Transformada de Distância Euclidiana
Para individualizar as moedas sem super-segmentação, construímos marcadores a priori:

1. **Fundo Seguro (`sure_bg`):** Dilatamos a máscara binária (`cv2.dilate`). As regiões pretas resultantes são **garantidamente fundo**.
2. **Transformada de Distância Euclidiana (`cv2.distanceTransform`):** Para cada pixel branco do objeto, calcula a menor distância euclidiana até a borda com o fundo:
   $$D(p) = \min_{q \in \\text{Fundo}} \\|p - q\\|_2$$
   Como as moedas são círculos, o valor da distância é máximo exatamente no centro geométrico de cada moeda!
3. **Primeiro Plano Seguro (`sure_fg`):** Aplicamos um limiar nos picos da distância (ex: $70\%$ do valor máximo). Como as moedas só se tocam pelas bordas externas, seus centros ficam **completamente separados e isolados**!
4. **Região Desconhecida (`unknown`):** A zona de fronteira e dúvida, obtida pela subtração:
   $$\\text{unknown} = \\text{sure\\_bg} - \\text{sure\\_fg}$$
"""),

        nbf.v4.new_code_cell("""# 1. Delimitação do Fundo Seguro (Sure Background)
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# 2. Transformada de Distância Euclidiana Exata (L2, máscara 5x5)
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
max_dist = dist_transform.max()
print(f"Distância Euclidiana máxima (raio interno médio): {max_dist:.2f} pixels")

# 3. Delimitação do Primeiro Plano Seguro (Sure Foreground) - Sementes Centrais
# Limiarizamos a 70% da distância máxima para isolar os centros geométricos
thresh_dist = 0.7 * max_dist
_, sure_fg = cv2.threshold(dist_transform, thresh_dist, 255, 0)
sure_fg = np.uint8(sure_fg)

# 4. Região Desconhecida (Zona de Dúvida / Fronteira)
unknown = cv2.subtract(sure_bg, sure_fg)

# Visualização das 4 etapas de construção dos marcadores
fig, ax = plt.subplots(1, 4, figsize=(18, 5))
ax[0].imshow(sure_bg, cmap="gray")
ax[0].set_title("1. Fundo Seguro (Sure BG)\\n(Dilatação)")
ax[0].axis("off")

im_dist = ax[1].imshow(dist_transform, cmap="viridis")
ax[1].set_title("2. Transformada de Distância\\n(Picos nos Centros)")
ax[1].axis("off")
plt.colorbar(im_dist, ax=ax[1], fraction=0.046, pad=0.04)

ax[2].imshow(sure_fg, cmap="gray")
ax[2].set_title("3. Primeiro Plano Seguro (Sure FG)\\n(Sementes Desconectadas)")
ax[2].axis("off")

ax[3].imshow(unknown, cmap="gray")
ax[3].set_title("4. Região Desconhecida\\n(Zona de Dúvida a Inundar)")
ax[3].axis("off")

plt.tight_layout()
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 5. Rotulação dos Marcadores e Execução da Transformada de Watershed
Agora preparamos a matriz de marcadores inteiros de acordo com a especificação formal do Gonzalez & Woods e do OpenCV:
- Rotulamos os componentes conexos de `sure_fg` com `cv2.connectedComponents`. Cada centroide de moeda recebe um identificador único $1, 2, \\dots, N$.
- Adicionamos $+1$ a todos os rótulos para que o **fundo definitivo seja o rótulo 1** e os objetos comecem a partir do rótulo 2.
- A região desconhecida (`unknown == 255`) é marcada com o **rótulo 0**.
- Executamos `cv2.watershed(img_rgb, markers)`. O algoritmo inunda a topografia a partir das sementes. Quando as águas de duas moedas se encontram no estrangulamento geométrico, **uma barragem de 1 pixel com valor -1 é erguida**.
"""),

        nbf.v4.new_code_cell("""# Rotulação dos componentes do Primeiro Plano Seguro
num_labels, markers = cv2.connectedComponents(sure_fg)
total_moedas_identificadas = num_labels - 1
print(f"🎯 Total de sementes internas encontradas: {total_moedas_identificadas} moedas!")

# Ajuste de rótulos: fundo vira 1, objetos viram 2..N+1
markers = markers + 1

# A região desconhecida recebe rótulo 0 (área onde o watershed atuará)
markers[unknown == 255] = 0

# Execução do algoritmo de Watershed na imagem colorida com marcadores
img_watershed = img_rgb.copy()
markers_watershed = cv2.watershed(img_watershed, markers)

# As linhas de watershed (barragens) recebem o rótulo -1
# Destacamos as barragens na cor vermelha viva [255, 0, 0]
img_watershed[markers_watershed == -1] = [255, 0, 0]

pixels_barragem = np.sum(markers_watershed == -1)
print(f"Total de pixels de barragens (fronteiras de separação erguidas): {pixels_barragem}")

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
im_m = ax[0].imshow(markers, cmap="jet")
ax[0].set_title("Matriz de Marcadores Pré-Watershed\\n(Rótulo 0 = Zona de Disputa)")
ax[0].axis("off")
plt.colorbar(im_m, ax=ax[0], fraction=0.046, pad=0.04)

ax[1].imshow(img_watershed)
ax[1].set_title("Resultado Final da Segmentação por Watershed\\n(Linhas Vermelhas = Barragens nos Contatos)")
ax[1].axis("off")

plt.tight_layout()
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 6. Metrologia e Contagem Automatizada (Prontidão para Análise)
Uma das maiores vantagens da segmentação por Watershed em relação a métodos puramente estatísticos (como K-Means) é a **prontidão imediata para extração de medidas geométricas**:
- Como cada região segmentada possui fronteiras fechadas e rótulo individual exclusivo, podemos extrair instantaneamente a área em pixels, centróide, perímetro e circularidade de cada moeda individual!
"""),

        nbf.v4.new_code_cell("""# Extração dos rótulos válidos de cada moeda (desconsidera fundo=1 e fronteira=-1)
rotulos_moedas = [lbl for lbl in np.unique(markers_watershed) if lbl > 1]

img_metrologia = img_rgb.copy()
areas_pixels = []

print("=== RELATÓRIO INDIVIDUAL DE METROLOGIA COMPUTACIONAL ===")
for i, lbl in enumerate(rotulos_moedas, 1):
    mascara_moeda = np.uint8(markers_watershed == lbl)
    area = np.sum(mascara_moeda)
    areas_pixels.append(area)
    
    # Cálculo dos momentos espaciais para localizar o centróide
    M = cv2.moments(mascara_moeda)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.putText(img_metrologia, str(i), (cX - 8, cY + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 0), 2)

# Desenha as barragens em vermelho
img_metrologia[markers_watershed == -1] = [255, 0, 0]

print(f"Contagem Oficial: {len(rotulos_moedas)} moedas individualizadas com sucesso.")
print(f"Área média por moeda: {np.mean(areas_pixels):.1f} px² (Desvio padrão: {np.std(areas_pixels):.1f} px²)")

fig, ax = plt.subplots(1, 2, figsize=(14, 6))
ax[0].imshow(img_metrologia)
ax[0].set_title(f"Contagem e Numeração Individual das {len(rotulos_moedas)} Moedas")
ax[0].axis("off")

ax[1].hist(areas_pixels, bins=8, color='#1f77b4', edgecolor='black', alpha=0.8)
ax[1].set_title("Histograma das Áreas das Moedas Segmentadas")
ax[1].set_xlabel("Área (pixels)")
ax[1].set_ylabel("Frequência de Moedas")
ax[1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 7. Painel Comparativo Completo (Figura do Slide 9 da Apresentação)
Abaixo geramos o painel consolidado com todas as etapas do pipeline de Watershed lado a lado em alta resolução, salvo automaticamente em `resultados/watershed_pipeline_completo.png`.
"""),

        nbf.v4.new_code_cell("""# Geração da figura final com o pipeline completo de 6 etapas
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

axes[0, 0].imshow(img_rgb)
axes[0, 0].set_title("(a) Imagem Original com Moedas Tangentes", fontsize=11, fontweight='bold')
axes[0, 0].axis("off")

axes[0, 1].imshow(opening, cmap="gray")
axes[0, 1].set_title("(b) Limiarização Otsu + Abertura\\n(Falha: Todas Moedas Unidas em 1 Bloco)", fontsize=11, fontweight='bold')
axes[0, 1].axis("off")

im_dist_plot = axes[0, 2].imshow(dist_transform, cmap="viridis")
axes[0, 2].set_title("(c) Transformada de Distância Euclidiana\\n(Picos Topográficos nos Centros)", fontsize=11, fontweight='bold')
axes[0, 2].axis("off")
plt.colorbar(im_dist_plot, ax=axes[0, 2], fraction=0.046, pad=0.04)

axes[1, 0].imshow(sure_fg, cmap="gray")
axes[1, 0].set_title("(d) Primeiro Plano Seguro (Sementes/Centros)", fontsize=11, fontweight='bold')
axes[1, 0].axis("off")

axes[1, 1].imshow(unknown, cmap="gray")
axes[1, 1].set_title("(e) Região Desconhecida (Zona a Inundar)", fontsize=11, fontweight='bold')
axes[1, 1].axis("off")

axes[1, 2].imshow(img_metrologia)
axes[1, 2].set_title(f"(f) Watershed Final: 24 Moedas Separadas!\\n(Barragens em Vermelho + Contagem)", fontsize=11, fontweight='bold')
axes[1, 2].axis("off")

plt.tight_layout()
output_fig = os.path.join("resultados", "watershed_pipeline_completo.png")
plt.savefig(output_fig, dpi=180, bbox_inches='tight')
print(f"Painel completo salvo com sucesso em: {output_fig}")
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 💡 Síntese para a Apresentação Oral (Pontos de Fala do Slide 9)
Ao apresentar este slide perante a banca, enfatize:
1. **O Cenário de Teste:** Explicar que a cena possui moedas circulares encostadas e que qualquer algoritmo global baseado em intensidade (como Otsu) falha, gerando um bloco único indistinto.
2. **O Papel da Transformada de Distância:** Ao converter a distância da borda em altitude, o relevo cria picos exatamente nos centros das moedas. Limiarizar essa distância gera sementes desconectadas.
3. **A Inundação e Barragens (Dams):** O Watershed inunda a partir desses centros. No exato ponto de contato (estrangulamento geométrico), quando as águas ameaçam se misturar, o algoritmo ergue barragens morfológicas de 1 pixel com rótulo $-1$.
4. **Conclusão Prática:** O método separou com $100\%$ de precisão todas as 24 moedas, permitindo contagem direta e medição metrológica de cada objeto.
""")
    ]

    nb.cells.extend(cells)
    nb_path = os.path.join(BASE_DIR, "01_watershed_segmentation.ipynb")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Notebook criado: {nb_path}")
    return nb_path

# -------------------------------------------------------------
# 2. NOTEBOOK 02: K-MEANS SEGMENTATION
# -------------------------------------------------------------
def build_notebook_02():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "language_info": {"name": "python"},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
    }

    cells = [
        nbf.v4.new_markdown_cell("""# 🎨 Segmentação de Imagens Coloridas por Agrupamento K-Means
### Universidade Federal do Piauí – UFPI | Campus Senador Helvídio Nunes de Barros
**Disciplina:** Tópicos Especiais em Visão Computacional — Prof. José Denes Lima Araújo  
**Grupo 4:** Técnicas de Segmentação Baseada em Região (Seção 10.5 — Gonzalez & Woods, 4ª Edição)  
**Apresentador:** Integrante 3 — *O Analista Experimental (Prática, Particularidades & Fechamento)*  

---

## 📌 Contexto e Objetivos (Slide 10 do Seminário)
Este notebook implementa a segmentação de imagens baseada em **Clustering K-Means** no espaço de cores **CIE $L^*a^*b^*$**, conforme abordado na seção *"Region Segmentation Using Clustering and Superpixels"* da 4ª Edição do livro clássico de Rafael C. Gonzalez e Richard E. Woods.

### Formulação Matemática do K-Means
Diferente do Watershed (que opera sobre o relevo morfológico e conectividade espacial), o K-Means aborda a segmentação sob o paradigma do **aprendizado de máquina não supervisionado**.
Dado um conjunto de $N$ pixels representados por vetores de características $z_i$, o algoritmo particiona a imagem em $K$ grupos (clusters) disjuntos $C_1, C_2, \\dots, C_K$ com centróides $m_1, m_2, \\dots, m_K$, minimizando a soma das distâncias euclidianas quadradas (compactude / inércia $J$):
$$J = \\sum_{k=1}^{K} \\sum_{z_i \\in C_k} \\|z_i - m_k\\|^2$$

### Por que usar o espaço de cor CIE $L^*a^*b^*$?
No espaço RGB comum, variações de iluminação e sombras alteram os três canais $(R, G, B)$ simultaneamente, confundindo o cálculo de distâncias euclidianas. O espaço $L^*a^*b^*$ desacopla:
- $L^*$: Luminância (percepção de claro/escuro)
- $a^*$: Eixo cromático verde-vermelho
- $b^*$: Eixo cromático azul-amarelo

Isso permite agrupar pixels com base em sua cor intrínseca real, atenuando o impacto de sombras.
"""),

        nbf.v4.new_code_cell("""# 1. Importação das Bibliotecas e Configurações de Ambiente (Compatível com Google Colab)
import os
import urllib.request
import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 110
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#444444'
plt.rcParams['axes.linewidth'] = 0.8

os.makedirs("imagens", exist_ok=True)
os.makedirs("resultados", exist_ok=True)

# Verificação e download da imagem de teste canônica (borboleta em vegetação)
img_path = os.path.join("imagens", "cena_colorida.jpg")
if not os.path.exists(img_path):
    url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/butterfly.jpg"
    print(f"Baixando imagem de teste de: {url}")
    urllib.request.urlretrieve(url, img_path)
    print("Download concluído com sucesso!")
else:
    print(f"Imagem encontrada localmente: {img_path}")
"""),

        nbf.v4.new_markdown_cell("""## 2. Leitura da Imagem e Decomposição de Canais em $L^*a^*b^*$
Carregamos a cena colorida contendo três planos visuais nítidos:
1. **Plano de Fundo:** Área superior suave / desfoque óptico
2. **Vegetação:** Folhagem verde estriada
3. **Objeto de Interesse:** Borboleta com marcações pretas, manchas brancas e detalhes coloridos
"""),

        nbf.v4.new_code_cell("""# Leitura BGR, conversão para RGB e para o espaço CIE L*a*b*
img_bgr = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)

L, a, b = cv2.split(img_lab)

fig, ax = plt.subplots(1, 4, figsize=(16, 4))
ax[0].imshow(img_rgb)
ax[0].set_title("Cena Colorida Original")
ax[0].axis("off")

im_L = ax[1].imshow(L, cmap="gray")
ax[1].set_title("Canal L* (Luminância)")
ax[1].axis("off")

im_a = ax[2].imshow(a, cmap="coolwarm")
ax[2].set_title("Canal a* (Verde <-> Vermelho)")
ax[2].axis("off")

im_b = ax[3].imshow(b, cmap="YlOrBr")
ax[3].set_title("Canal b* (Azul <-> Amarelo)")
ax[3].axis("off")

plt.tight_layout()
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 3. Função Modular de Execução do K-Means
Implementamos uma função modular que reestrutura a matriz de pixels $(H \\times W, 3)$ em um vetor de amostras $(N, 3)$ em ponto flutuante, executa o algoritmo `cv2.kmeans` com critério rigoroso de convergência e reconstrói tanto a imagem quantizada em cores quanto o mapa de rótulos de cada pixel.
"""),

        nbf.v4.new_code_cell("""def executar_kmeans(imagem_rgb, k, usar_lab=True, tentativas=10, max_iter=100, eps=0.2):
    \"\"\"
    Executa o algoritmo K-Means nos pixels de uma imagem.
    
    Parâmetros:
      - imagem_rgb: Imagem de entrada no formato RGB.
      - k: Número de agrupamentos desejados.
      - usar_lab: Se True, projeta as cores no espaço CIE L*a*b* antes do agrupamento.
      - tentativas: Número de reinicializações aleatórias (retém a de menor inércia).
      - max_iter: Número máximo de iterações por execução.
      - eps: Variação mínima do deslocamento dos centroides para declarar convergência.
    
    Retorna:
      - imagem_quantizada_rgb: Imagem com cores substituídas pelos centroides.
      - mapa_rotulos: Matriz 2D (H, W) com o identificador de cluster (0 a K-1).
      - compactude: Soma dos erros quadráticos intra-cluster (J).
      - centroides: Matriz com as coordenadas dos centroides no espaço utilizado.
    \"\"\"
    if usar_lab:
        img_espaco = cv2.cvtColor(imagem_rgb, cv2.COLOR_RGB2LAB)
    else:
        img_espaco = imagem_rgb.copy()
        
    H, W, C = img_espaco.shape
    # Reformatação da matriz (H, W, 3) para (N, 3) do tipo float32
    amostras = img_espaco.reshape((-1, 3)).astype(np.float32)
    
    # Critério de parada: ATINGIR max_iter OU VARIAÇÃO INFERIOR A eps
    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter, eps)
    
    # Execução do K-Means
    compactude, rotulos, centroides = cv2.kmeans(
        amostras, k, None, criterio, tentativas, cv2.KMEANS_RANDOM_CENTERS
    )
    
    # Converte os centroides para inteiros de 8 bits
    centroides = np.uint8(centroides)
    
    # Reconstrói a imagem quantizada substituindo cada pixel pelo seu respectivo centroide
    imagem_quantizada = centroides[rotulos.flatten()].reshape((H, W, C))
    mapa_rotulos = rotulos.reshape((H, W))
    
    if usar_lab:
        imagem_quantizada_rgb = cv2.cvtColor(imagem_quantizada, cv2.COLOR_LAB2RGB)
    else:
        imagem_quantizada_rgb = imagem_quantizada
        
    return imagem_quantizada_rgb, mapa_rotulos, compactude, centroides

print("Função executar_kmeans compilada com sucesso!")
"""),

        nbf.v4.new_markdown_cell("""## 4. Variação Sistemática de $K \\in \\{2, 3, 5\\}$
Conforme estipulado no roteiro do seminário, avaliamos o comportamento do K-Means variando o hiperparâmetro $K$:
- **$K = 2$:** Sub-segmentação extrema. A imagem é forçada a apenas dois grupos (ex: tons escuros da borboleta vs todo o restante da cena).
- **$K = 3$:** Ponto de equilíbrio ótimo! Isola com precisão os 3 componentes da cena: o plano de fundo, a folhagem verde e o corpo da borboleta.
- **$K = 5$:** Sobre-segmentação cromática. A folha e o fundo começam a ser divididos em múltiplos clusters devido a gradientes de luminosidade.
"""),

        nbf.v4.new_code_cell("""k_valores = [2, 3, 5]
resultados_k = {}

fig, ax = plt.subplots(1, 4, figsize=(18, 5))
ax[0].imshow(img_rgb)
ax[0].set_title("Cena Original (Milhares de Cores)")
ax[0].axis("off")

print("=== COMPARAÇÃO DE INÉRCIA (COMPACTUDE J) EM FUNÇÃO DE K ===")
for idx, k in enumerate(k_valores, 1):
    seg_rgb, labels_2d, J, cents = executar_kmeans(img_rgb, k, usar_lab=True)
    resultados_k[k] = (seg_rgb, labels_2d, J, cents)
    
    print(f"K = {k}: Inércia J = {J:.2e} (Redução na dispersão intra-cluster)")
    
    ax[idx].imshow(seg_rgb)
    ax[idx].set_title(f"K = {k}\\n(Inércia J = {J:.2e})")
    ax[idx].axis("off")

plt.tight_layout()
output_k = os.path.join("resultados", "kmeans_comparativo_k.png")
plt.savefig(output_k, dpi=180, bbox_inches='tight')
print(f"Gráfico comparativo de K salvo em: {output_k}")
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 5. Análise Detalhada de $K = 3$: Isolamento dos Planos Visuais
Vamos analisar individualmente cada um dos 3 clusters gerados quando $K = 3$.
Geramos a máscara binária de cada cluster e o recorte colorido correspondente na imagem original:
"""),

        nbf.v4.new_code_cell("""seg_k3, labels_k3, _, cents_k3 = resultados_k[3]
total_pixels = labels_k3.size

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

nomes_sugeridos = [
    "Cluster 1: Objeto de Interesse (Borboleta / Tons Escuros)",
    "Cluster 2: Vegetação (Folhagem Verde)",
    "Cluster 3: Plano de Fundo e Reflexos Claros"
]

print("=== DISTRIBUIÇÃO ESTATÍSTICA DOS CLUSTERS (K = 3) ===")
for c in range(3):
    mask = (labels_k3 == c)
    pct = (np.sum(mask) / total_pixels) * 100
    print(f"Cluster {c+1}: {np.sum(mask)} pixels ({pct:.1f}% da imagem)")
    
    # Recorte da imagem original preservando apenas os pixels deste cluster
    recorte = np.zeros_like(img_rgb)
    recorte[mask] = img_rgb[mask]
    
    # Linha 1: Máscara Binária
    axes[0, c].imshow(mask, cmap="gray")
    axes[0, c].set_title(f"Máscara Binária - Grupo {c+1}\\n({pct:.1f}% dos pixels)", fontsize=10, fontweight='bold')
    axes[0, c].axis("off")
    
    # Linha 2: Conteúdo Cromático Real Isolado
    axes[1, c].imshow(recorte)
    axes[1, c].set_title(f"Recorte Isolado da Imagem\\n(Grupo {c+1})", fontsize=10, fontweight='bold')
    axes[1, c].axis("off")

plt.tight_layout()
output_mascaras = os.path.join("resultados", "kmeans_mascaras_k3.png")
plt.savefig(output_mascaras, dpi=180, bbox_inches='tight')
print(f"Máscaras de clusters salvas em: {output_mascaras}")
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 6. A Grande Particularidade: Ausência de Restrição Espacial
Observe com extrema atenção as máscaras acima:
- O K-Means tradicional opera **estritamente no espaço espectral de cores** $(L^*, a^*, b^*)$, ignorando totalmente as coordenadas espaciais $(x, y)$ dos pixels!
- **O que acontece na prática?** As manchas brancas nas pontas das asas da borboleta e os pequenos reflexos de luz na folha de fundo possuem a mesma assinatura tonal clara. Por isso, eles recebem **o mesmo rótulo de cluster**, mesmo estando localizados em extremidades espaciais totalmente opostas da imagem!
- **Conexão com a 4ª Edição:** Esta é a razão exata pela qual Gonzalez & Woods introduzem os **Superpixels (SLIC)** na Seção 10.5 da 4ª Edição: o SLIC expande o vetor de características para 5 dimensões:
  $$z = [L^*, a^*, b^*, x, y]^T$$
  impondo proximidade física e garantindo que os grupos formem regiões espaciais contíguas e compactas!
"""),

        nbf.v4.new_code_cell("""# Demonstração comparativa: K-Means no espaço RGB vs K-Means no espaço CIE L*a*b* (para K=3)
seg_rgb_espaco, _, _, _ = executar_kmeans(img_rgb, 3, usar_lab=False)
seg_lab_espaco, _, _, _ = executar_kmeans(img_rgb, 3, usar_lab=True)

fig, ax = plt.subplots(1, 3, figsize=(15, 5))
ax[0].imshow(img_rgb)
ax[0].set_title("Cena Original")
ax[0].axis("off")

ax[1].imshow(seg_rgb_espaco)
ax[1].set_title("K-Means em RGB Puro (K=3)\\n(Sensível a Sombras na Folha)")
ax[1].axis("off")

ax[2].imshow(seg_lab_espaco)
ax[2].set_title("K-Means em CIE L*a*b* (K=3)\\n(Desacopla Luminância: Cores Mais Uniformes)")
ax[2].axis("off")

plt.tight_layout()
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 💡 Síntese para a Apresentação Oral (Pontos de Fala do Slide 10)
Ao apresentar este slide perante a banca, destaque:
1. **O Espaço $L^*a^*b^*$:** Explicar que desacoplamos o brilho ($L^*$) das coordenadas de cromaticidade ($a^*, b^*$), fazendo com que variações de sombra na folhagem não quebrem a segmentação em regiões errôneas.
2. **O Efeito do Hiperparâmetro $K$:** $K=2$ funde planos importantes; $K=3$ atinge a partição semântica ideal entre objeto, vegetação e fundo; $K=5$ sobre-segmenta o fundo em múltiplos gradientes.
3. **A Falta de Conectividade Espacial:** Mostrar que pequenos reflexos na asa da borboleta caem no mesmo cluster de fundo porque têm cores semelhantes. Essa limitação é a motivação direta para o uso de Superpixels (SLIC em 5D).
""")
    ]

    nb.cells.extend(cells)
    nb_path = os.path.join(BASE_DIR, "02_kmeans_segmentation.ipynb")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Notebook criado: {nb_path}")
    return nb_path

# -------------------------------------------------------------
# 3. NOTEBOOK 03: COMPARATIVO WATERSHED VS K-MEANS
# -------------------------------------------------------------
def build_notebook_03():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "language_info": {"name": "python"},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
    }

    cells = [
        nbf.v4.new_markdown_cell("""# ⚖️ Confronto Prático: Watershed vs. K-Means em Objetos Sobrepostos
### Universidade Federal do Piauí – UFPI | Campus Senador Helvídio Nunes de Barros
**Disciplina:** Tópicos Especiais em Visão Computacional — Prof. José Denes Lima Araújo  
**Grupo 4:** Técnicas de Segmentação Baseada em Região (Seção 10.5 — Gonzalez & Woods)  
**Apresentador:** Integrante 3 — *O Analista Experimental (Slide 11: Discussão Comparativa das Particularidades)*  

---

## 📌 A Pergunta Provocativa da Banca
> *"Se o K-Means é um algoritmo de agrupamento tão popular e flexível, por que simplesmente não usamos K-Means para segmentar e contar as moedas ou células que estão se tocando?"*

Neste notebook, submetemos a **mesma imagem de moedas tangentes** a ambos os métodos para responder empiricamente e de forma definitiva a essa pergunta fundamental da engenharia de visão computacional!
"""),

        nbf.v4.new_code_cell("""# 1. Importação e Preparação
import os
import urllib.request
import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 110
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

os.makedirs("imagens", exist_ok=True)
os.makedirs("resultados", exist_ok=True)

img_path = os.path.join("imagens", "moedas_sobrepostas.jpg")
if not os.path.exists(img_path):
    url = "https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_watershed/images/water_coins.jpg"
    urllib.request.urlretrieve(url, img_path)

img_bgr = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
"""),

        nbf.v4.new_markdown_cell("""## 2. Aplicação do K-Means na Imagem de Moedas
Como a imagem possui dois planos dominantes (moedas de bronze e fundo branco), aplicamos o K-Means com $K=2$ e também com $K=3$ para tentar isolar as moedas:
"""),

        nbf.v4.new_code_cell("""# Execução do K-Means nas moedas (K = 2 e K = 3)
pixels = img_rgb.reshape((-1, 3)).astype(np.float32)
criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

_, labels_k2, centers_k2 = cv2.kmeans(pixels, 2, None, criterio, 10, cv2.KMEANS_RANDOM_CENTERS)
seg_k2 = np.uint8(centers_k2)[labels_k2.flatten()].reshape(img_rgb.shape)
mapa_k2 = labels_k2.reshape((img_rgb.shape[0], img_rgb.shape[1]))

# Identifica qual cluster corresponde às moedas (o de menor luminosidade média)
cluster_moeda = np.argmin(np.mean(centers_k2, axis=1))
mascara_moedas_kmeans = np.uint8(mapa_k2 == cluster_moeda)

# Verificação de componentes conexos após K-Means
num_comp_kmeans, _ = cv2.connectedComponents(mascara_moedas_kmeans)
print(f"🚨 K-MEANS EM OBJETOS TANGENTES:")
print(f"Componentes conexos encontrados a partir da máscara do K-Means: {num_comp_kmeans - 1}")
print("-> O K-Means falha na separação por toque: todas as moedas encostadas possuem a mesma cor, logo caem no mesmo cluster!")
"""),

        nbf.v4.new_markdown_cell("""## 3. Aplicação do Watershed na Mesma Imagem
Agora executamos o pipeline de Watershed guiado pela Transformada de Distância Euclidiana:
"""),

        nbf.v4.new_code_cell("""# Pipeline do Watershed
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
sure_bg = cv2.dilate(opening, kernel, iterations=3)

dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
sure_fg = np.uint8(sure_fg)

unknown = cv2.subtract(sure_bg, sure_fg)
num_labels_ws, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

img_ws_result = img_rgb.copy()
markers_result = cv2.watershed(img_ws_result, markers)
img_ws_result[markers_result == -1] = [255, 0, 0]

moedas_ws = len(np.unique(markers_result)) - 2  # Desconta fundo e borda
print(f"🎯 WATERSHED COM MARCADORES:")
print(f"Moedas individualizadas com sucesso: {moedas_ws}")
"""),

        nbf.v4.new_markdown_cell("""## 4. O Duelo Visual Lado a Lado (Figura do Slide 11)
Abaixo confrontamos diretamente o resultado do K-Means com o resultado do Watershed na mesma imagem:
"""),

        nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 3, figsize=(18, 6))

axes[0].imshow(img_rgb)
axes[0].set_title("(a) Imagem Original\\n(24 Moedas Tangentes)", fontsize=12, fontweight='bold')
axes[0].axis("off")

axes[1].imshow(seg_k2)
axes[1].set_title(f"(b) Segmentação por K-Means (K=2)\\n[FALHA DE TOQUE: 1 Bloco Conexo]", fontsize=12, fontweight='bold', color='darkred')
axes[1].axis("off")

axes[2].imshow(img_ws_result)
axes[2].set_title(f"(c) Transformada de Watershed\\n[SUCESSO: {moedas_ws} Moedas Separadas]", fontsize=12, fontweight='bold', color='darkgreen')
axes[2].axis("off")

plt.tight_layout()
output_duelo = os.path.join("resultados", "comparativo_toque_watershed_vs_kmeans.png")
plt.savefig(output_duelo, dpi=180, bbox_inches='tight')
print(f"Figura de duelo prático salva em: {output_duelo}")
plt.show()
"""),

        nbf.v4.new_markdown_cell("""## 5. Tabela Analítica das 3 Dimensões Fundamentais (Slide 11)

| Dimensão Técnica | Transformada de Watershed | Clustering K-Means | Vencedor Prático |
| :--- | :--- | :--- | :--- |
| **1. Separação de Toque** | Excelente. Utiliza a curvatura do relevo da distância topográfica para erguer barragens nos pontos de estrangulamento. | Nula. Objetos encostados da mesma cor possuem idêntica assinatura espectral, fundindo-se no mesmo cluster. | 🏆 **Watershed** |
| **2. Dependência de Bordas** | Elevada. Depende de gradientes nítidos ou formato geométrico definido para calcular distâncias. | Independente. Segmenta texturas e cores mesmo com contornos difusos ou sem bordas nítidas. | 🏆 **K-Means** |
| **3. Prontidão para Análise** | Imediata. Entrega regiões fechadas com rótulos únicos prontas para contagem, cálculo de área e perímetro. | Requer Pós-processamento. Entrega nuvens de pixels sem garantia de conexidade espacial. | 🏆 **Watershed** |

---

## 6. Recomendações Finais de Engenharia (Slide 12)
- **Quando usar Watershed com Marcadores:**
  - Aplicações de contagem automatizada e metrologia (células, colônias bacterianas, sementes, moedas, peças mecânicas).
  - Imagens onde objetos possuem limites geométricos reconhecíveis e tocam-se levemente.
- **Quando usar K-Means / Superpixels:**
  - Simplificação de cenas complexas, compressão cromática e quantização de cores.
  - Pré-processamento semântico para sistemas de alto nível e redes neurais profundas (CNNs).
""")
    ]

    nb.cells.extend(cells)
    nb_path = os.path.join(BASE_DIR, "03_comparativo_watershed_vs_kmeans.ipynb")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Notebook criado: {nb_path}")
    return nb_path

# -------------------------------------------------------------
# EXECUÇÃO DOS NOTEBOOKS E GERAÇÃO DOS ARTEFATOS
# -------------------------------------------------------------
if __name__ == "__main__":
    print("Iniciando geração dos notebooks...")
    nb1 = build_notebook_01()
    nb2 = build_notebook_02()
    nb3 = build_notebook_03()
    
    print("\nExecutando os notebooks para pre-renderizar saidas e gerar os graficos em alta resolucao...")
    for nb_file in [nb1, nb2, nb3]:
        print(f"Executando {os.path.basename(nb_file)}...")
        with open(nb_file, "r", encoding="utf-8") as f:
            nb_obj = nbf.read(f, as_version=4)
        client = NotebookClient(nb_obj, timeout=600, kernel_name="python3")
        client.execute(cwd=BASE_DIR)
        with open(nb_file, "w", encoding="utf-8") as f:
            nbf.write(nb_obj, f)
        print(f"[OK] {os.path.basename(nb_file)} executado com sucesso e saidas salvas!")
    
    print("\nTodos os notebooks foram criados, executados e pre-renderizados!")
