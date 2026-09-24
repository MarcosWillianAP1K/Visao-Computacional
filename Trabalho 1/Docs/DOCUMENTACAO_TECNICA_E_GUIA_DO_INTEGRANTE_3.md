# 📚 DOCUMENTAÇÃO TÉCNICA E GUIA DEFINITIVO DO INTEGRANTE 3

## Técnicas de Segmentação Baseada em Região (Seção 10.5 — Gonzalez & Woods)

**Universidade Federal do Piauí – UFPI | Campus Senador Helvídio Nunes de Barros (CSHNB)**  
**Curso:** Bacharelado em Sistemas de Informação | 6º Período  
**Disciplina:** Tópicos Especiais em Visão Computacional  
**Professor:** Prof. Me. José Denes Lima Araújo  
**Equipe:** Grupo 4 (Segmentação Baseada em Região)  
**Papel:** **Integrante 3 — O Analista Experimental (Prática, Particularidades & Fechamento)**  

---

# 📑 Sumário Executivo

1. [Visão Geral e Atribuição do Integrante 3](#1-visão-geral-e-atribuição-do-integrante-3)
2. [Fundamentação Teórica dos Métodos](#2-fundamentação-teórica-dos-métodos)
   - [2.1 A Transformada de Watershed com Marcadores (3ª e 4ª Edições)](#21-a-transformada-de-watershed-com-marcadores)
   - [2.2 O Agrupamento K-Means e Espaço CIE L\*a\*b\* (4ª Edição)](#22-o-agrupamento-k-means-e-espaço-cie-lab)
3. [Engenharia de Código: Explicação Linha por Linha](#3-engenharia-de-código-explicação-linha-por-linha)
   - [3.1 Código 1: Watershed com Marcadores e Distância (`01_watershed_segmentation.ipynb`)](#31-código-1-watershed-com-marcadores-e-distância)
   - [3.2 Código 2: K-Means em Espaço L\*a\*b\* (`02_kmeans_segmentation.ipynb`)](#32-código-2-k-means-em-espaço-lab)
   - [3.3 Código 3: Confronto Prático de Toque (`03_comparativo_watershed_vs_kmeans.ipynb`)](#33-código-3-confronto-prático-de-toque)
4. [Análise das Particularidades Práticas e Resultados Experimentais](#4-análise-das-particularidades-práticas-e-resultados-experimentais)
5. [Roteiro Completo de Apresentação Oral (Slides 9 ao 12)](#5-roteiro-completo-de-apresentação-oral-slides-9-ao-12)
6. [Guia de Defesa contra Perguntas da Banca (Prof. José Denes)](#6-guia-de-defesa-contra-perguntas-da-banca)

---

# 1. Visão Geral e Atribuição do Integrante 3

O trabalho consiste na apresentação de seminário e entrega de código referente ao **Capítulo 10 ("Segmentação de Imagens")** do livro clássico de Rafael C. Gonzalez e Richard E. Woods. O **Grupo 4** ficou responsável pela **Seção 10.5: Técnicas de Segmentação Baseada em Região**, abrangendo:

1. **Transformada de Watershed** (Seção 10.5 do livro da 3ª edição).
2. **Clustering K-Means e Superpixels** (Seção *"Region Segmentation Using Clustering and Superpixels"* do livro da 4ª edição).

### Divisão em Trio do Grupo 4

- **Integrante 1 (O Especialista em Watershed):** Apresenta os fundamentos conceituais, a analogia topográfica das bacias hidrográficas, a construção morfológica de barragens (*dams*) e a motivação matemática para marcadores.
- **Integrante 2 (O Especialista em K-Means & Agrupamento):** Apresenta o aprendizado não supervisionado, a função de custo $J$, os espaços de cores ($RGB$ vs $L^*a^*b^*$), a transição para superpixels (SLIC) e a tabela comparativa teórica.
- **Integrante 3 (VOCÊ - O Analista Experimental):** Responsável por **todos os experimentos em código**, validação visual com imagens reais, discussão profunda das particularidades práticas e fechamento das conclusões com recomendações de engenharia perante a banca.

---

# 2. Fundamentação Teórica dos Métodos

## 2.1 A Transformada de Watershed com Marcadores

A Transformada de Watershed é um método morfológico originário da mecânica dos fluidos e da geografia, introduzido no processamento de imagens por Fernand Meyer e Serge Beucher (CMM - École des Mines de Paris).

### A Analogia Topográfica Tridimensional

Considere uma imagem digital bidimensional $f(x, y)$ em níveis de cinza ou uma imagem gradiente $g(x, y) = \|\nabla f(x, y)\|$. No espaço tridimensional:

- As coordenadas $(x, y)$ definem o plano horizontal do relevo geográfico.
- O valor da intensidade em cada pixel representa a **altitude** (altura) da montanha ou vale.

Nessa topografia, existem três categorias formais de pontos:

1. **Mínimos Regionais:** Vales planos ou pontos mais baixos do relevo circundante.
2. **Bacias de Captação (*Catchment Basins*):** Uma bacia hidrográfica associada a um mínimo regional $M_i$ é o conjunto de todos os pontos onde uma gota de chuva que caísse escorreria com certeza absoluta para $M_i$.
3. **Linhas Divisórias de Águas (*Watershed Lines*):** Cristas do relevo onde uma gota de água teria igual probabilidade de escorrer para dois ou mais mínimos distintos.

### A Simulação de Inundação e a Construção de Barragens (*Dams*)

Conceitualmente, o algoritmo fura pequenos orifícios em cada mínimo regional e mergulha a topografia inteira em um reservatório de água. A água sobe por esses orifícios a uma taxa uniforme de inundação $n = \min + 1, \dots, \max + 1$:

- Conforme a água sobe, as bacias de captação começam a ser preenchidas.
- No instante exato em que a água de duas bacias vizinhas $C(M_1)$ e $C(M_2)$ ameaça transbordar e se fundir em um mesmo componente conexo $q$, **uma barragem (dam) é erguida**.
- A barragem é construída por **dilatações morfológicas sucessivas com elemento estruturante simétrico $3 \times 3$**, restritas ao componente conexo $q$, até sobrar uma fronteira contínua de exatamente **1 pixel de espessura**, à qual é atribuído um valor superior à intensidade máxima da imagem (ou rótulo $-1$).
- **Propriedade Matemática Fundamental:** As linhas de watershed formam **caminhos conexos fechados**, eliminando completamente o problema de fronteiras abertas ou descontínuas típico dos detectores de borda tradicionais (Sobel, Prewitt, Laplaciano).

```
   Altitude (Relevo)
       ^                 Barragem (Watershed Line)
       |                            |
       |       /\                   |                   /\
       |      /  \                 / \                 /  \
       |     /    \               /   \               /    \
       |    /      \    Água     /  |  \    Água     /      \
       |   /        \~~~~~~~~~~~/   |   \~~~~~~~~~~~/        \
       |  /          \_________/    |    \_________/          \
       | /            Mínimo M1     |     Mínimo M2            \
       +----------------------------+----------------------------> Coordenadas (x, y)
```

### O Desafio da Sobre-Segmentação (*Over-segmentation*)

Se a Transformada de Watershed for aplicada diretamente sobre a imagem pura ou sobre seu gradiente bruto, pequenas variações locais de textura e ruído de alta frequência criam centenas de mínimos regionais espúrios. A consequência prática é a **sobre-segmentação catastrófica**, dividindo a imagem em milhares de fragmentos microscópicos inúteis.

### A Solução Canônica: Watershed Controlado por Marcadores

Para domesticar o Watershed, Gonzalez & Woods prescrevem a **introdução de conhecimento prévio (*a priori*) através de Marcadores**:

1. **Marcadores Internos (Sure Foreground / Sementes):** Componentes conexos localizados exclusivamente no interior de cada objeto de interesse.
2. **Marcador Externo (Sure Background):** Regiões que certamente pertencem ao fundo da imagem.
3. **Área Desconhecida (*Unknown*):** A zona de transição e dúvida onde as barragens devem ser disputadas e construídas.

No caso clássico de **objetos circulares ou regulares em contato (moedas, núcleos celulares, comprimidos)**, a ferramenta matemática mais poderosa para gerar os marcadores internos é a **Transformada de Distância Euclidiana**:
$$D(p) = \min_{q \in \text{Fundo}} \|p - q\|_2$$
Como os objetos se tocam apenas nas bordas externas, a distância ao fundo atinge picos de elevação exatamente no centro geométrico de cada moeda. Ao aplicar um limiar sobre esses picos ($0.7 \cdot D_{\max}$), **os centros se desconectam fisicamente**, fornecendo exatamente uma semente interna para cada objeto individual!

---

## 2.2 O Agrupamento K-Means e Espaço CIE L\*a\*b\*

Abordado na Seção 10.5 da 4ª Edição (*"Region Segmentation Using Clustering and Superpixels"*), o K-Means muda radicalmente o paradigma: sai a topografia morfológica e entra o **aprendizado de máquina não supervisionado no espaço de atributos**.

### Formulação Matemática

Seja uma imagem composta por $N$ pixels, onde cada pixel é representado por um vetor de características $z_i \in \mathbb{R}^d$ (por exemplo, os canais de cor). O objetivo do K-Means é particionar esses $N$ vetores em $K$ clusters disjuntos $\{C_1, C_2, \dots, C_K\}$ com médias (centroides) $\{m_1, m_2, \dots, m_K\}$, minimizando a soma das distâncias euclidianas quadradas (**função de custo de compactude intra-cluster / inércia $J$**):

$$J = \sum_{k=1}^{K} \sum_{z_i \in C_k} \|z_i - m_k\|^2$$

### Passo a Passo do Algoritmo Clássico

1. **Inicialização:** Escolha dos $K$ centroides iniciais $m_1, \dots, m_K$ (geralmente aleatórios ou via k-means++).
2. **Atribuição:** Cada pixel $z_i$ é associado ao centroide mais próximo:
   $$C_k = \left\{ z_i : \|z_i - m_k\|^2 \le \|z_i - m_j\|^2, \; \forall j \ne k \right\}$$
3. **Atualização:** Recalculam-se as posições dos centroides como a média aritmética de todos os pontos atribuídos ao cluster:
   $$m_k = \frac{1}{|C_k|} \sum_{z_i \in C_k} z_i$$
4. **Critério de Parada:** O ciclo de Atribuição-Atualização se repete até que o deslocamento dos centroides seja desprezível ($\Delta m \approx 0$ ou $\Delta m < \varepsilon$) ou o número máximo de iterações seja atingido.

### Por que o Espaço de Cores CIE L\*a\*b\* é Superior ao RGB?

O livro enfatiza que utilizar distâncias euclidianas no espaço RGB padrão é conceitualmente falho para segmentação perceptual:

- **No espaço RGB:** As componentes $R$, $G$ e $B$ possuem alta correlação estatística mútua. A informação de luminância (brilho) está dispersa em todos os três canais. Se uma sombra incide sobre uma folha verde, seus valores de $R$, $G$ e $B$ caem drasticamente, fazendo com que o K-Means classifique a área sombreada como um objeto completamente diferente da área iluminada.
- **No espaço CIE $L^*a^*b^*$:**
  - $L^* \in [0, 100]$: Representa a **Luminância** perceptual (do preto absoluto ao branco puro).
  - $a^* \in [-128, +127]$: Eixo cromático **Verde $\leftrightarrow$ Vermelho**.
  - $b^* \in [-128, +127]$: Eixo cromático **Azul $\leftrightarrow$ Amarelo**.
  
Ao desacoplar o brilho das coordenadas cromáticas, a distância euclidiana no plano $(a^*, b^*)$ ou no espaço ponderado $(L^*, a^*, b^*)$ reflete a **cor real intrínseca** da superfície, conferindo enorme robustez contra sombras e iluminação não uniforme.

### A Particularidade Crucial: Ausência de Restrição Espacial

O K-Means padrão opera **exclusivamente no espaço de cores**. O vetor de cada pixel é $z_i = [L_i, a_i, b_i]^T$, sem qualquer coordenada espacial $(x_i, y_i)$.

- **Consequência:** Pixels com cores idênticas situados em cantos opostos da imagem recebem o mesmo rótulo. Não existe qualquer garantia de que um cluster forme uma região fisicamente contígua.
- **A Solução da 4ª Edição:** O algoritmo **SLIC (Simple Linear Iterative Clustering)** introduz as coordenadas cartesianas no vetor de características:
  $$z = [L^*, a^*, b^*, x, y]^T$$
  restringindo a busca a janelas locais de tamanho $2S \times 2S$, gerando **Superpixels regulares, compactos e contíguos** com complexidade linear $O(N)$.

---

# 3. Engenharia de Código: Explicação Linha por Linha

Todos os códigos foram projetados para serem executados tanto no **Google Colab** quanto no **VS Code com kernel local ou remoto**, contando com mecanismo de download automático das imagens canônicas.

## 3.1 Código 1: Watershed com Marcadores e Distância

**Arquivo:** `Trabalho 1/Codigo/01_watershed_segmentation.ipynb` (e versão `.py`)

Abaixo está a análise minuciosa de cada bloco lógico implementado:

### Bloco 1: Preparação do Ambiente e Download da Imagem

```python
import os
import sys
import urllib.request
import cv2
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("imagens", exist_ok=True)
os.makedirs("resultados", exist_ok=True)

img_path = os.path.join("imagens", "moedas_sobrepostas.jpg")
if not os.path.exists(img_path):
    url = "https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_watershed/images/water_coins.jpg"
    urllib.request.urlretrieve(url, img_path)
```

- **Por que foi feito assim?** No Google Colab, a máquina virtual é temporária e inicia limpa. O bloco cria as pastas necessárias e baixa a imagem canônica de teste (`water_coins.jpg` da documentação oficial do OpenCV) se ela não existir localmente, garantindo execução com 1 clique sem erros de arquivo.

### Bloco 2: Carregamento e Conversão de Cores

```python
img_bgr = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
```

- `cv2.imread`: Carrega a imagem no padrão BGR do OpenCV.
- `cv2.COLOR_BGR2RGB`: Converte para RGB para exibição fidedigna no Matplotlib.
- `cv2.COLOR_BGR2GRAY`: Converte para níveis de cinza (matriz 2D de intensidades $0$ a $255$), necessária para as operações morfológicas e transformada de distância.

### Bloco 3: Limiarização de Otsu e Abertura Morfológica

```python
otsu_thresh, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
num_labels_otsu, _ = cv2.connectedComponents(opening)
```

- `cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU`: Como o fundo da imagem é branco ($\approx 255$) e as moedas são escuras, a flag inversa inverte o resultado, tornando as moedas brancas ($255$) e o fundo preto ($0$). O parâmetro $0$ indica que o limiar ótimo é computado matematicamente pelo critério de Otsu (que resultou em $T^* = 162.0$).
- `cv2.morphologyEx(..., cv2.MORPH_OPEN, ...)`: Aplica a **abertura morfológica**, que consiste em uma erosão seguida de dilatação com elemento estruturante $3 \times 3$ preenchido com $1$s. Essa operação elimina pequenos pontos de ruído branco no fundo e microfuros escuros sobre as moedas.
- `cv2.connectedComponents(opening)`: Rotula componentes conexos na máscara binária. **Resultado:** Retorna apenas **1 componente conexo** (`num_labels_otsu - 1 == 1`), demonstrando perante a banca a **falha absoluta do método global de Otsu** em separar objetos tangentes.

### Bloco 4: Delimitação do Fundo Seguro (Sure Background)

```python
sure_bg = cv2.dilate(opening, kernel, iterations=3)
```

- `cv2.dilate`: Aplica $3$ iterações de dilatação morfológica com o kernel $3 \times 3$.
- **Objetivo físico:** Ao dilatar a área das moedas, expandimos as fronteiras dos objetos para dentro do fundo. Logo, qualquer pixel que permaneça preto com valor $0$ após essa dilatação é **com 100% de certeza fundo real** da imagem.

### Bloco 5: Transformada de Distância Euclidiana e Primeiro Plano Seguro

```python
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
max_dist = dist_transform.max()
thresh_dist = 0.7 * max_dist
_, sure_fg = cv2.threshold(dist_transform, thresh_dist, 255, 0)
sure_fg = np.uint8(sure_fg)
```

- `cv2.distanceTransform(opening, cv2.DIST_L2, 5)`: Executa o algoritmo de Transformada de Distância Euclidiana exata ($\ell_2$) com máscara de convolução de tamanho $5 \times 5$. Para cada pixel branco da moeda, calcula a menor distância geométrica em pixels até o pixel de fundo mais próximo.
- `dist_transform.max()`: Retorna a distância máxima encontrada (neste teste: $23.97$ pixels, que corresponde exatamente ao raio interno médio das moedas).
- `thresh_dist = 0.7 * max_dist`: Estabelece o limiar de corte nos picos de altitude topográfica da distância ($70\%$ do pico máximo).
- `cv2.threshold(..., 255, 0)`: Binariza os picos. Como os pontos de toque entre moedas adjacentes possuem distância ao fundo baixa (próxima de zero), apenas os núcleos geométricos centrais de cada moeda sobrevivem.
- **Resultado espetacular:** As moedas que estavam fundidas em um único bloco se transformam em **24 pequenas ilhas brancas completamente isoladas e desconectadas** (`sure_fg`).

### Bloco 6: Região Desconhecida (Zona de Dúvida)

```python
unknown = cv2.subtract(sure_bg, sure_fg)
```

- `cv2.subtract(sure_bg, sure_fg)`: Subtrai a máscara das sementes internas da máscara do fundo dilatado.
- **Significado físico:** O resultado é uma malha em forma de anel ao redor de cada moeda que engloba exatamente as bordas verdadeiras e os pontos de estrangulamento onde as moedas se tocam. Essa é a região onde o algoritmo de inundação do Watershed terá que atuar para erguer as barragens.

### Bloco 7: Rotulação Conexa e Preparação da Matriz de Marcadores

```python
num_labels, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0
```

- `cv2.connectedComponents(sure_fg)`: Atribui um identificador inteiro único para cada semente desconectada ($1, 2, \dots, 24$).
- `markers = markers + 1`: **Etapa crítica exigida pela especificação do Watershed no OpenCV!** Como o fundo era rotulado com $0$, somamos $+1$ para que o **fundo definitivo receba o rótulo 1** e as moedas passem a ter rótulos de $2$ a $25$.
- `markers[unknown == 255] = 0`: Atribui o rótulo $0$ para toda a região desconhecida. É exatamente sobre os pixels de valor $0$ que a simulação de inundação irá disputar a água e construir as barragens!

### Bloco 8: Execução da Transformada de Watershed

```python
img_watershed = img_rgb.copy()
markers_result = cv2.watershed(img_watershed, markers)
img_watershed[markers_result == -1] = [255, 0, 0]
```

- `cv2.watershed(img_watershed, markers)`: Executa o algoritmo de Meyer. Ele inunda a topografia a partir dos marcadores rotulados ($1, 2, \dots, 25$) avançando pela região $0$. No momento exato em que a bacia de captação de uma moeda se encontra com a bacia da moeda vizinha, o algoritmo detecta o transbordamento e constrói uma **barragem morfológica (dam) de 1 pixel de espessura**, atribuindo a ela o valor especial **$-1$**.
- `img_watershed[markers_result == -1] = [255, 0, 0]`: Pinta todos os pixels de barragem com a cor vermelha pura, demarcando a separação exata nos pontos de contato.

### Bloco 9: Metrologia, Centróides e Contagem Individual

```python
coin_labels = [lbl for lbl in np.unique(markers_result) if lbl > 1]
for i, lbl in enumerate(coin_labels, 1):
    mask = np.uint8(markers_result == lbl)
    areas.append(np.sum(mask))
    M = cv2.moments(mask)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.putText(img_metrologia, str(i), (cX - 8, cY + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 0), 2)
```

- Demonstra a **prontidão para análise**: o código itera sobre cada moeda individual ($lbl = 2 \dots 25$), calcula a área em pixels (`np.sum(mask)`), calcula os momentos espaciais de 1ª ordem ($M_{10}$ e $M_{01}$) e 0ª ordem ($M_{00}$) para extrair o centróide cartesiano exato:
  $$cX = \frac{M_{10}}{M_{00}}, \quad cY = \frac{M_{01}}{M_{00}}$$
  e insere o número identificador de $1$ a $24$ em verde no centro de cada moeda!

---

## 3.2 Código 2: K-Means em Espaço L\*a\*b\*

**Arquivo:** `Trabalho 1/Codigo/02_kmeans_segmentation.ipynb` (e versão `.py`)

### Bloco 1: Decomposição e Projeção no Espaço CIE L\*a\*b\*

```python
img_bgr = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
L, a, b = cv2.split(img_lab)
```

- Converte a imagem fotográfica (`cena_colorida.jpg` / borboleta em folhagem) para o espaço $L^*a^*b^*$ com `cv2.COLOR_BGR2LAB`.
- `cv2.split`: Isola os três canais físicos:
  - $L$: Mostra a intensidade da luz e sombras.
  - $a$: Destaca fortemente o verde da folha em oposição a manchas vermelhas da borboleta.
  - $b$: Destaca o componente amarelo da folha estriada.

### Bloco 2: A Função de Agrupamento Matricial

```python
def executar_kmeans(imagem_rgb, k, usar_lab=True, tentativas=10, max_iter=100, eps=0.2):
    if usar_lab:
        img_espaco = cv2.cvtColor(imagem_rgb, cv2.COLOR_RGB2LAB)
    else:
        img_espaco = imagem_rgb.copy()
        
    H, W, C = img_espaco.shape
    amostras = img_espaco.reshape((-1, 3)).astype(np.float32)
    
    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter, eps)
    compactness, rotulos, centroides = cv2.kmeans(
        amostras, k, None, criterio, tentativas, cv2.KMEANS_RANDOM_CENTERS
    )
    
    centroides = np.uint8(centroides)
    imagem_quantizada = centroides[rotulos.flatten()].reshape((H, W, C))
    mapa_rotulos = rotulos.reshape((H, W))
    
    if usar_lab:
        imagem_quantizada_rgb = cv2.cvtColor(imagem_quantizada, cv2.COLOR_LAB2RGB)
    else:
        imagem_quantizada_rgb = imagem_quantizada
        
    return imagem_quantizada_rgb, mapa_rotulos, compactness, centroides
```

- `amostras = img_espaco.reshape((-1, 3)).astype(np.float32)`: A imagem com dimensões $(H, W, 3)$ é transformada em uma matriz bidimensional de dimensões $(N, 3)$, onde $N = H \times W$ é o número total de pixels ($175.508$ pixels) e cada linha é uma amostra com três variáveis ($L^*, a^*, b^*$). O OpenCV exige dados do tipo `float32`.
- `criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)`: Define o critério de convergência: o algoritmo para se atingir $100$ iterações OU se o deslocamento médio de todos os centroides na iteração atual for menor que $0.2$ unidades de distância.
- `tentativas = 10`: Como o K-Means clássico é sensível à inicialização dos centroides e pode convergir para mínimos locais subótimos, a rotina roda $10$ vezes com inicializações aleatórias distintas (`cv2.KMEANS_RANDOM_CENTERS`) e seleciona a execução que produziu a menor compactude (menor erro quadrático $J$).
- `centroides[rotulos.flatten()].reshape((H, W, C))`: Constrói a **imagem quantizada em cores**, substituindo a cor original de cada um dos $175.508$ pixels pela cor média exata do seu centroide atribuído.

### Bloco 3: Avaliação Sistemática de $K \in \{2, 3, 5\}$

Os testes computaram a inércia intra-cluster $J$:

- **Para $K = 2$:** $J = 3.43 \times 10^8$. A dispersão intra-cluster é elevadíssima. O algoritmo funde a folha verde com o plano de fundo, separando apenas o corpo escuro da borboleta.
- **Para $K = 3$:** $J = 1.83 \times 10^8$. Ocorre uma queda brutal na inércia (**o "cotovelo" da curva de dispersão**). A imagem atinge a partição semântica perfeita dos 3 planos: (1) Objeto de interesse, (2) Vegetação verde e (3) Fundo claro.
- **Para $K = 5$:** $J = 1.03 \times 10^8$. A redução no erro é modesta, mas a cena sofre sobre-segmentação cromática, fatiando a mesma folha contínua em múltiplos tons artificiais.

### Bloco 4: Isolamento e Extração de Máscaras em $K = 3$

```python
for c in range(3):
    mask = (labels_k3 == c)
    recorte = np.zeros_like(img_rgb)
    recorte[mask] = img_rgb[mask]
```

- Gera as máscaras binárias booleanas de cada cluster e multiplica pela imagem RGB original, recortando com fidelidade cirúrgica apenas a parte física da cena pertencente àquele grupo.

---

## 3.3 Código 3: Confronto Prático de Toque

**Arquivo:** `Trabalho 1/Codigo/03_comparativo_watershed_vs_kmeans.ipynb` (e versão `.py`)

Aplica K-Means e Watershed na **mesma imagem de moedas tangentes**:

- **K-Means ($K=2$):** Como todas as moedas são feitas do mesmo material de bronze e o fundo é papel branco, o espaço de cor só possui dois agrupamentos dominantes: bronze e branco. Ao agrupar os pixels bronze e calcular os componentes conexos resultantes, o K-Means entrega **1 único bloco conexo de moedas** ($0$ moedas separadas).
- **Watershed:** Enxerga a variação geométrica através do gradiente e da transformada de distância, ergue as barragens nos pontos de toque e entrega **24 moedas separadas**.

---

# 4. Análise das Particularidades Práticas e Resultados Experimentais

Esta seção reúne as constatações experimentais essenciais que você deverá citar com firmeza no seu seminário:

### 1. Separação por Toque (O Embate Central)

- **K-Means:** É **cego à geometria e ao relevo**. Dois objetos que se tocam e possuem a mesma cor ou textura têm idêntica assinatura de densidade probabilística no espaço de atributos. Logo, o K-Means é **estruturalmente incapaz** de separar objetos encostados sem um pós-processamento morfológico complexo.
- **Watershed:** É **baseado em relevo e propagação geodésica**. Através da curvatura topográfica da Transformada de Distância, cada objeto circular gera um vale independente. As barragens morfológicas encontram o ponto de estrangulamento geométrico exato entre os círculos (*necking point*), separando-os com perfeição.

### 2. Dependência de Bordas e Contornos

- **Watershed:** Depende criticamente da existência de **bordas nítidas no gradiente** ou de uma geometria regular para o cálculo de distâncias. Se a transição entre o objeto e o fundo for difusa, com contraste quase nulo ou gradientes suaves, a água transborda sem criar barragem correta (*leakage problem*).
- **K-Means:** Não depende de bordas! O K-Means agrupa pixels por similaridade de cor mesmo que o contorno do objeto seja completamente borrado, difuso ou inexista uma linha contínua de gradiente.

### 3. Conectividade e Prontidão para Análise

- **Watershed:** As linhas de barragem possuem a garantia matemática formal de formarem **fronteiras conexas e fechadas**. Cada região recebe um rótulo exclusivo, estando imediatamente pronta para metrologia (contagem, área, perímetro, excentricidade).
- **K-Means Tradicional:** Não possui nenhuma restrição de adjacência espacial. Pixels idênticos em cantos opostos da cena caem no mesmo cluster. Para obter objetos individuais a partir do K-Means, é obrigatório executar uma etapa posterior de rotulação de componentes conexos.

---

# 5. Roteiro Completo de Apresentação Oral (Slides 9 ao 12)

Apresente com postura ereta, tom de voz seguro e firme, olhando para a banca e alternando o olhar para os slides quando indicar as imagens.

---

### 🎙️ Frase de Entrada (Transição do Integrante 2 para Você)
>
> *"Obrigado, [Nome do Integrante 2]. Agora que compreendemos a formulação teórica tanto do relevo morfológico do Watershed quanto do espaço métrico do K-Means, eu vou apresentar a nossa análise experimental com imagens reais, demonstrando o comportamento do código e as particularidades práticas de cada método."*

---

### 🖼️ Slide 9: Aplicação Prática 1 — Watershed em Objetos Sobrepostos

*(Tempo estimado de fala: ~1 minuto e 15 segundos)*

**O que apontar no slide:**

- Aponte para a **figura (a)** (moedas encostadas).
- Aponte para a **figura (b)** (binarização de Otsu unindo tudo).
- Aponte para a **figura (c)** (o mapa colorido de distância euclidiana com os picos amarelos).
- Aponte para a **figura (d)** (as 24 sementes desconectadas).
- Aponte para a **figura (f)** (o resultado final com as linhas vermelhas de barragem e a contagem de 1 a 24).

**O que falar:**
> *"Neste primeiro experimento prático, submetemos um dos problemas mais desafiadores da visão computacional industrial: a segmentação de objetos tangentes e sobrepostos. Aqui temos 24 moedas dispostas sobre uma bancada clara.*
>
> *Se tentarmos resolver esse problema com técnicas clássicas baseadas apenas em intensidade pontual — como a limiarização global de Otsu, vista na figura (b) —, o algoritmo falha completamente. Como as moedas encostam umas nas outras e o ponto de toque tem a mesma cor dos objetos, o Otsu gera uma única massa branca indistinta, detectando apenas um único componente conexo.*
>
> *Para solucionar isso, implementamos o pipeline completo de Watershed baseado em marcadores. Primeiro, limpamos pequenos ruídos com abertura morfológica e dilatamos a máscara para garantir o fundo seguro na figura (a).*
>
> *O grande pulo do gato está na figura (c): calculamos a Transformada de Distância Euclidiana exata. Como as moedas são circulares, a distância até a borda de fundo atinge o valor máximo exatamente no centro geométrico de cada moeda. Ao limiarizarmos esses picos em 70% da distância máxima, como visto na figura (d), nós desconectamos os objetos e encontramos com precisão cirúrgica as 24 sementes internas.*
>
> *Por fim, na figura (f), a Transformada de Watershed simulou a inundação a partir dessas sementes pela área desconhecida. No momento exato em que a água de duas moedas ameaçou transbordar no ponto de estrangulamento geométrico, o algoritmo ergueu barragens morfológicas de 1 pixel com valor menos um, destacadas em vermelho. O resultado prático foi o isolamento perfeito de todas as 24 moedas, permitindo calcular a área média de cada uma e numerá-las automaticamente."*

---

### 🖼️ Slide 10: Aplicação Prática 2 — K-Means em Segmentação Colorida

*(Tempo estimado de fala: ~1 minuto e 15 segundos)*

**O que apontar no slide:**

- Aponte para a imagem original da borboleta na folhagem.
- Aponte para a comparação entre $K=2$, $K=3$ e $K=5$.
- Aponte para as máscaras binárias do $K=3$, destacando como o corpo da borboleta, a folha e o fundo foram isolados.
- Destaque a particularidade: aponte para as manchas brancas na asa da borboleta e mostre que elas caíram no mesmo grupo do fundo claro!

**O que falar:**
> *"Na nossa segunda aplicação prática, avaliamos o agrupamento não supervisionado via K-Means em uma cena fotográfica colorida com três planos nítidos: plano de fundo, vegetação e objeto de interesse.*
>
> *Seguindo a recomendação da Seção 10.5 da 4ª Edição do Gonzalez & Woods, nós não aplicamos o K-Means no espaço RGB. Nós projetamos os pixels no espaço perceptual CIE L\*a\*b\*. Isso é fundamental porque o canal L\* isola a luminância, permitindo que os eixos a\* e b\* agrupem a cromaticidade pura da folha verde e da borboleta, reduzindo drasticamente a sensibilidade a sombras e variações de iluminação.*
>
> *Ao variarmos o hiperparâmetro K, observamos empiricamente: com K igual a 2, temos sub-segmentação, pois a folhagem e o fundo são forçados no mesmo grupo. Com K igual a 5, temos sobre-segmentação tonal, dividindo a mesma folha em múltiplos tons de gradiente. O equilíbrio semântico perfeito ocorreu com K igual a 3, onde a inércia intra-cluster sofre uma queda brusca e conseguimos extrair as três máscaras isoladas vistas abaixo: o corpo da borboleta com 28% da imagem, a vegetação com 33% e o fundo com 37%.*
>
> *Porém, quero chamar a atenção da banca para uma particularidade prática crucial evidenciada no nosso código: reparem que as manchas claras na asa da borboleta receberam o mesmo rótulo do fundo claro distante. Isso ocorre porque o K-Means tradicional opera apenas no espaço de cores e não possui restrição de adjacência espacial. Essa limitação é a razão exata pela qual o livro propõe a evolução para os Superpixels com o algoritmo SLIC, que incorpora as coordenadas x e y no vetor de atributos."*

---

### 🖼️ Slide 11: Discussão Comparativa das Particularidades

*(Tempo estimado de fala: ~1 minuto)*

**O que apontar no slide:**

- Aponte para o duelo visual: mostre o K-Means falhando na imagem de moedas (1 bloco marrom) ao lado do Watershed separando todas as 24 moedas.
- Percorra as 3 linhas da tabela comparativa.

**O que falar:**
> *"Chegando ao embate comparativo direto entre as duas técnicas da Seção 10.5, sintetizamos três dimensões fundamentais de engenharia:*
>
> *A primeira é a Separação de Toque: para responder se poderíamos usar K-Means nas moedas, submetemos a mesma imagem ao K-Means. Como as moedas de bronze possuem idêntica assinatura de cor, o K-Means funde todas em um único cluster, gerando um bloco conexo indistinto. O Watershed resolve isso perfeitamente porque utiliza a topografia e a curvatura da distância para construir barragens morfológicas.*
>
> *A segunda dimensão é a Dependência de Bordas: aqui a vantagem se inverte. O Watershed depende fortemente de gradientes definidos ou contornos geométricos. Se a imagem tiver bordas difusas ou transições suaves, a água vaza. O K-Means, por operar no espaço estatístico de atributos, consegue segmentar texturas e cores mesmo onde não existem bordas ou contornos perceptíveis.*
>
> *E a terceira dimensão é a Prontidão para Análise: o Watershed entrega fronteiras fechadas com identificadores únicos para cada objeto, estando pronto para contagem e medição de área. O K-Means entrega grupos desconexos de pixels, exigindo etapas posteriores de rotulação e filtragem."*

---

### 🖼️ Slide 12: Conclusão Final & Referências

*(Tempo estimado de fala: ~45 segundos)*

**O que falar:**
> *"Como conclusões finais e recomendações práticas de engenharia de visão computacional:*
>
> *Recomendamos o uso da Transformada de Watershed baseada em Marcadores para tarefas industriais, laboratoriais e biomédicas que exijam contagem automatizada e metrologia individualizada de elementos regulares ou celulares em contato.*
>
> *Recomendamos o Clustering K-Means e a sua extensão moderna em Superpixels para tarefas de simplificação de cena, compressão de cores, extração de regiões cromáticas homogêneas e como pré-processamento de alto nível para modelos de aprendizado profundo e redes neurais.*
>
> *Nossa implementação utilizou como referência oficial o livro Digital Image Processing de Gonzalez & Woods, Seção 10.5 da 3ª e da 4ª Edições.*
>
> *Agradecemos a atenção do professor José Denes e dos colegas de classe, e a equipe está totalmente à disposição para as perguntas da banca."*

---

# 6. Guia de Defesa contra Perguntas da Banca

Aqui estão as 10 perguntas mais prováveis que o Prof. José Denes Lima Araújo pode fazer sobre o seu código, com respostas diretas e precisas:

### Pergunta 1: *"Por que no código do Watershed você somou 1 aos marcadores (`markers = markers + 1`) e atribuiu 0 à área desconhecida?"*

**Sua Resposta:**  
*"Professor, essa é uma exigência estrita do algoritmo `cv2.watershed` do OpenCV. A função `cv2.connectedComponents` rotula o fundo como 0 e os objetos como 1, 2, 3... Porém, no Watershed do OpenCV, o rótulo 0 é reservado exclusivamente para a 'zona desconhecida' — a área onde a inundação deve ocorrer e onde as barragens serão disputadas. Por isso, somamos 1 a toda a matriz para que o fundo garantido vire rótulo 1 e os objetos comecem a partir do rótulo 2. Em seguida, setamos a região desconhecida com 0. Se não fizéssemos esse deslocamento, o algoritmo interpretaria o fundo como área de disputa e destruiria a segmentação."*

---

### Pergunta 2: *"Qual o critério matemático utilizado para definir o limiar da transformada de distância em 70% (`0.7 * max_dist`)?"*

**Sua Resposta:**  
*"O valor de 70% foi definido empiricamente com base na relação entre o raio dos círculos e a largura da zona de contato. Como as moedas são circulares com raio em torno de 24 pixels, a distância ao fundo nas bordas tangentes cai para valores abaixo de 10 a 12 pixels, enquanto os centros mantêm valores próximos de 24. Um limiar muito baixo (por exemplo, 30%) manteria as sementes conectadas pelas pontes de toque. Um limiar excessivamente alto (como 95%) correria o risco de perder moedas menores ou que sofreram oclusão parcial. O valor de 0.7 garantiu isolamento perfeito de 100% dos 24 centros sem falsos negativos."*

---

### Pergunta 3: *"Por que o algoritmo de Watershed atribui exatamente o valor -1 para as barragens?"*

**Sua Resposta:**  
*"O valor -1 é a convenção numérica adotada pelo OpenCV para representar as Watershed Lines, ou seja, as cristas do relevo onde as barragens morfológicas de 1 pixel de espessura foram erguidas. Como todos os componentes identificados recebem números inteiros positivos (1 para fundo, 2 para objeto 1, 3 para objeto 2, etc.), o valor negativo -1 permite que a gente filtre, visualize e desenhe facilmente os contornos de separação sobre a imagem colorida, sem confundir as bordas com nenhum objeto segmentado."*

---

### Pergunta 4: *"O que aconteceria se aplicássemos o Watershed no gradiente direto da imagem das moedas sem usar a transformada de distância?"*

**Sua Resposta:**  
*"Haveria uma sobre-segmentação severa (over-segmentation). Como as moedas possuem gravações em relevo na superfície (números, rostos e datas), o gradiente nessas ranhuras internas gera dezenas de cristas e vales locais. O Watershed direto criaria dezenas de pequenas bacias dentro de cada moeda, fatiando a imagem em centenas de fragmentos inúteis, exatamente como demonstrado na Figura 10.57 do livro do Gonzalez & Woods."*

---

### Pergunta 5: *"Por que converter a imagem para o espaço CIE L\*a\*b\* antes de rodar o K-Means?"*

**Sua Resposta:**  
*"Porque o K-Means calcula a distância euclidiana entre os pontos, e no espaço RGB a distância euclidiana não é perceptualmente uniforme. Pequenas variações de sombra reduzem simultaneamente os valores de R, G e B, fazendo o algoritmo achar que uma folha ensolarada e uma folha sombreada são coisas diferentes. No espaço L\*a\*b\*, o canal L\* concentra a luminância, enquanto a\* e b\* retêm a informação de cor pura. Isso permite que o K-Means agrupe pixels pela sua assinatura cromática real, conferindo grande estabilidade contra sombreamentos."*

---

### Pergunta 6: *"O que representa o retorno `compactness` da função `cv2.kmeans`?"*

**Sua Resposta:**  
*"Representa a inércia intra-cluster, que é exatamente a função de custo J da Seção 10.5: a soma das distâncias euclidianas quadradas entre cada pixel e o centroide do seu respectivo cluster. Quanto menor o J, mais densos e coesos são os clusters. Nos nossos testes, ao passar de K=2 para K=3, a inércia caiu de 3.43 x 10^8 para 1.83 x 10^8, demonstrando que K=3 é o ponto ótimo de inflexão ('cotovelo') antes da sobre-segmentação."*

---

### Pergunta 7: *"Por que o K-Means falhou em separar as moedas no teste comparativo do Slide 11?"*

**Sua Resposta:**  
*"Porque o K-Means é um classificador puramente espectral: ele não possui nenhuma informação sobre onde o pixel está localizado na imagem. Como as moedas de bronze têm todas a mesma cor e textura, os pixels de duas moedas que estão encostadas caem no mesmo ponto do espaço de atributos. O K-Means classifica todos os pixels das moedas no mesmo cluster. Quando tentamos extrair os objetos conexos dessa máscara, temos apenas um único bloco contínuo."*

---

### Pergunta 8: *"Como o algoritmo SLIC de superpixels resolve essa limitação do K-Means tradicional?"*

**Sua Resposta:**  
*"O SLIC, introduzido na 4ª edição do Gonzalez & Woods, expande o vetor de características de 3 dimensões de cor para um vetor 5D: z = [L\*, a\*, b\*, x, y]^T. Ao adicionar as coordenadas espaciais x e y ponderadas por uma constante de compactude e restringir a busca de centroides a janelas locais de tamanho 2S x 2S, o SLIC força os clusters a formarem regiões fisicamente vizinhas e contíguas, gerando superpixels regulares e eliminando o agrupamento de regiões distantes."*

---

### Pergunta 9: *"Quais critérios de parada foram configurados no `cv2.kmeans` e por que usamos 10 tentativas?"*

**Sua Resposta:**  
*"Usamos como critério combinado a flag `cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER`, estabelecendo um teto de 100 iterações ou convergência quando o deslocamento médio dos centroides for inferior a epsilon = 0.2. Usamos 10 tentativas com inicializações aleatórias distintas porque o K-Means é sensível aos centroides iniciais e pode convergir para mínimos locais indesejados. O algoritmo executa as 10 vezes e retém automaticamente a solução com a menor inércia J."*

---

### Pergunta 10: *"Como foi feita a contagem e a metrologia individual das moedas no código?"*

**Sua Resposta:**  
*"Após o Watershed retornar os marcadores com as barragens delimitadas por -1, o código seleciona os rótulos válidos maiores que 1 (excluindo fundo e bordas). Para cada rótulo, criamos uma máscara binária booleana. A área é calculada pela contagem de pixels ativos com `np.sum(mask)`. Em seguida, calculamos os momentos estatísticos de ordem zero e primeira ordem com `cv2.moments(mask)` para encontrar as coordenadas exatas do centróide cartesiano (m10/m00 e m01/m00) e plotamos a numeração sequencial de 1 a 24 no centro de cada moeda."*

---

## 🏆 Checklist Final para o Dia da Apresentação

- [x] Notebooks prontos e pré-renderizados em `Trabalho 1/Codigo/`.
- [x] Gráficos de alta resolução salvos em `Trabalho 1/Codigo/resultados/`.
- [x] Roteiro ensaiado focando na transição e nos tempos de fala (Slide 9 ao 12).
- [x] Respostas das 10 perguntas na ponta da língua para a banca do Prof. José Denes!
