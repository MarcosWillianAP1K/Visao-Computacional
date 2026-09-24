# Roteiro de Apresentacao e Explicacao do Codigo
**UFPI - Campus Senador Helvidio Nunes de Barros**  
**Disciplina:** Topicos Especiais em Visao Computacional  
**Professor:** Prof. Me. Jose Denes Lima Araujo  
**Grupo 4:** Tecnicas de Segmentacao Baseada em Regiao (Secao 10.5 - Gonzalez & Woods)  
**Apresentador:** Integrante 3 (O Analista Experimental)  
**Tempo estimado:** 4 a 5 minutos (Slides 9 ao 12)

---

## 1. Entrada e Frase de Transicao
Assim que o Integrante 2 concluir a tabela comparativa teorica, assuma a palavra imediatamente:

> "Obrigado, [Nome do Integrante 2]. Agora que compreendemos a base teorica do Watershed e do K-Means, eu vou apresentar os nossos experimentos praticos com codigo em Python, demonstrando o comportamento real de cada algoritmo em cenarios do mundo real."

---

## 2. Slide 9: Aplicacao Pratica 1 - Watershed em Objetos Sobrepostos

### O que mostrar na tela:
O painel multipainel com as 6 etapas (`watershed_pipeline_completo.png`).

### Roteiro de fala:
> "No nosso primeiro experimento, abordamos um problema classico e desafiador da visao computacional: a segmentacao de objetos em contato. Aqui temos 24 moedas circulares sobre fundo claro.
>
> Na figura (b), demonstramos porque metodos convencionais baseados puramente em intensidade, como a limiarizacao de Otsu, falham. Como as moedas encostam umas nas outras e o ponto de contato tem a mesma cor escura do metal, o Otsu une todas em uma unica massa branca contínua, detectando apenas um unico componente conexo.
>
> Para resolver isso, implementamos o Watershed controlado por marcadores. Aplicamos abertura morfologica para limpar ruidos e dilatamos a regiao para definir o fundo seguro na figura (a).
>
> O ponto central esta na figura (c): calculamos a Transformada de Distancia Euclidiana. Como as moedas sao circulares, a distancia ate a borda de fundo atinge picos de altitude exatamente no centro de cada moeda. Ao limiarizarmos esses picos em 70% do valor maximo, eliminamos as pontes de contato e isolamos exatamente as 24 sementes centrais vistas na figura (d).
>
> Por fim, na figura (f), o Watershed simula a inundacao partindo dessas sementes. No exato ponto de estrangulamento geometrico entre duas moedas vizinhas, o algoritmo ergue barragens morfologicas de 1 pixel de espessura com rotulo menos um, que destacamos em vermelho.
>
> O algoritmo entregou com 100% de precisao todas as 24 moedas separadas e prontas para analise metrologica, permitindo calcular o centroide de cada uma e a area media de aproximadamente 2.200 pixels."

---

### Se o Professor pedir: "Abra o Notebook e me mostre o codigo bruto do Watershed"

Voce vai abrir o arquivo `01_watershed_segmentation.ipynb` e apontar para as linhas-chave:

1. **Binarizacao e Abertura:**
   ```python
   otsu_val, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
   opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
   ```
   *O que explicar:* "Usamos `THRESH_BINARY_INV` porque o fundo original e claro e as moedas sao escuras. A abertura morfologica com kernel 3x3 faz uma erosao seguida de dilatacao, eliminando pequenos ruidos brancos no fundo sem alterar a forma das moedas."

2. **Fundo Seguro (sure_bg):**
   ```python
   sure_bg = cv2.dilate(opening, kernel, iterations=3)
   ```
   *O que explicar:* "Ao dilatar a mascara das moedas por 3 iteracoes, avancamos as bordas para dentro do fundo. O que continua preto (valor zero) apos essa dilatacao e garantidamente fundo real."

3. **Transformada de Distancia e Sementes (sure_fg):**
   ```python
   dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
   _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
   ```
   *O que explicar:* "A funcao `cv2.distanceTransform` com metrica euclidiana `DIST_L2` calcula para cada pixel branco a distancia euclidiana ate a borda de fundo mais proxima. O centro das moedas atinge a distancia maxima (~24 pixels). Ao cortar em 70% desse valor maximo, os pontos de toque (que tem distancia baixa) somem, restando apenas os centros geometricos desconectados."

4. **Regiao Desconhecida e Ajuste de Rotulos:**
   ```python
   unknown = cv2.subtract(sure_bg, sure_fg)
   num_labels, markers = cv2.connectedComponents(sure_fg)
   markers = markers + 1
   markers[unknown == 255] = 0
   ```
   *O que explicar:* "A regiao desconhecida `unknown` e a diferenca entre o fundo dilatado e os centros; e a zona onde as bordas reais estao e onde haverá a disputa da inundacao. O `connectedComponents` rotula as sementes de 1 a 24. No OpenCV, somamos mais 1 (`markers = markers + 1`) para que o fundo garantido vire rotulo 1 e as moedas fiquem de 2 a 25. Em seguida, colocamos rotulo 0 na area desconhecida, pois o OpenCV exige que o rotulo zero seja a regiao onde o Watershed vai trabalhar."

5. **Execucao e Barragens:**
   ```python
   markers_result = cv2.watershed(img_watershed, markers)
   img_watershed[markers_result == -1] = [255, 0, 0]
   ```
   *O que explicar:* "A funcao `cv2.watershed` inunda a partir dos marcadores rotulados. Onde duas bacias vizinhas ameacam se encontrar, ele constroi uma barragem morfologica e marca o pixel com o rotulo -1. Nós simplesmente pintamos os pixels de rotulo -1 de vermelho."

---

## 3. Slide 10: Aplicacao Pratica 2 - K-Means em Segmentacao Colorida

### O que mostrar na tela:
O comparativo de K (`kmeans_comparativo_k.png`) e as mascaras isoladas de K=3 (`kmeans_mascaras_k3.png`).

### Roteiro de fala:
> "Na segunda aplicacao pratica, avaliamos o agrupamento estatistico nao supervisionado via K-Means em uma cena colorida contendo tres planos: o fundo, a vegetacao e o objeto de interesse (a borboleta).
>
> Seguindo a orientacao da 4ª Edicao do Gonzalez & Woods, convertemos a imagem para o espaco CIE L\*a\*b\*. No RGB convencional, a variacao de luminosidade e sombras distorce a distancia euclidiana. No espaco L\*a\*b\*, o canal L\* isola o brilho, permitindo que os eixos a\* e b\* agrupem a cor pura da folha e da borboleta com estabilidade.
>
> Avaliamos o comportamento ao variar o numero de clusters K:
> - Com K igual a 2, temos sub-segmentacao: o algoritmo junta o fundo e a folhagem verde em um unico grupo, separando apenas a borboleta.
> - Com K igual a 5, temos sobre-segmentacao tonal: a mesma folha e dividida em varios tons artificiais de verde devido a gradientes de luz.
> - Com K igual a 3, encontramos a particao semantica ideal: conseguimos isolar a borboleta com 28% da imagem, a folhagem verde com 33% e o plano de fundo com 37%.
>
> Porem, evidenciamos uma particularidade crucial do K-Means tradicional: notem que as manchas claras na asa da borboleta receberam o mesmo rotulo do fundo claro distante. Isso ocorre porque o K-Means atua puramente no espaco das cores e nao possui restricao espacial.
>
> Essa limitacao e o motivo exato pelo qual o livro introduz os Superpixels (SLIC), que expandem o vetor para 5 dimensoes incluindo as coordenadas x e y, forcando os agrupamentos a formarem regioes vizinhas e continuas."

---

### Se o Professor pedir: "Me mostre o codigo bruto do K-Means"

Voce vai abrir o arquivo `02_kmeans_segmentation.ipynb` e mostrar a funcao:

```python
def executar_kmeans(imagem_rgb, k, usar_lab=True):
    img_espaco = cv2.cvtColor(imagem_rgb, cv2.COLOR_RGB2LAB)
    H, W, C = img_espaco.shape
    amostras = img_espaco.reshape((-1, 3)).astype(np.float32)
    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    compactude, rotulos, centroides = cv2.kmeans(
        amostras, k, None, criterio, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    centroides = np.uint8(centroides)
    imagem_quantizada = centroides[rotulos.flatten()].reshape((H, W, C))
    return cv2.cvtColor(imagem_quantizada, cv2.COLOR_LAB2RGB), rotulos.reshape((H, W)), compactude
```
*O que explicar:*
- `reshape((-1, 3))`: "O K-Means nao recebe uma imagem em formato de grade 2D. Ele precisa de uma tabela de amostras onde cada linha e um pixel e as 3 colunas sao os atributos (L, a, b). Por isso achatamos a imagem de (H, W, 3) para (N, 3)."
- `criterio`: "Paramos se atingir 100 iteracoes ou se o deslocamento medio dos centroides for menor que 0.2."
- `tentativas = 10`: "O K-Means tradicional pode cair em minimos locais dependendo de onde os centroides comecam. Rodamos 10 vezes com inicializacao aleatoria e o algoritmo retem a de menor erro quadratico (compactude)."
- `rotulos.flatten()`: "Substituimos o vetor de cada pixel pelo valor do centroide ao qual ele foi atribuido, reconstruindo a imagem quantizada."

---

## 4. Slide 11: Discussao Comparativa das Particularidades

### O que mostrar na tela:
O duelo visual (`comparativo_toque_watershed_vs_kmeans.png`) e a tabela das 3 dimensoes.

### Roteiro de fala:
> "Para sintetizar o embate tecnico perante a banca, aplicamos ambos os algoritmos exatamente na mesma imagem de moedas tangentes, analisando tres dimensoes:
>
> 1. Separacao de Toque: O K-Means falha totalmente na separacao por toque. Como todas as moedas sao de bronze e tem a mesma cor, o K-Means coloca todas no mesmo cluster espectral, resultando em 1 unico bloco continuo. Ja o Watershed utiliza a topografia e a curvatura da Transformada de Distancia para erguer barragens nos pontos de estrangulamento, separando todas as 24 moedas.
>
> 2. Dependencia de Bordas: Aqui a situacao se inverte. O Watershed depende de transicoes nitidas de gradiente ou geometria circular clara para calcular a distancia. O K-Means e independente de bordas: ele consegue segmentar texturas e cores mesmo que o contorno do objeto seja difuso ou inexistente.
>
> 3. Prontidao para Analise: O Watershed entrega regioes conexas fechadas com rotulos individuais unicos, pronto para metrologia e contagem automatica. O K-Means entrega nuvens de pixels sem garantia de conexidade, exigindo etapas posteriores de rotulacao e filtragem."

---

## 5. Slide 12: Conclusao Final e Recomendacoes de Engenharia

### Roteiro de fala:
> "Concluindo o nosso trabalho, estabelecemos duas recomendacoes diretas de engenharia:
>
> - Utilize a Transformada de Watershed baseada em Marcadores quando o objetivo for contagem automatizada, inspecao industrial de pecas ou metrologia celular/biomedica onde objetos regulares se tocam.
> - Utilize o Clustering K-Means e sua extensao em Superpixels quando o objetivo for simplificacao de cenas complexas, quantizacao de paleta de cores ou como etapa de pre-processamento semantico para redes neurais profundas.
>
> Nossa bibliografia base foi o capitulo 10 de Gonzalez & Woods, secao 10.5 da 3ª e 4ª edicoes.
> Agradecemos ao professor Jose Denes e a turma, e estamos abertos a perguntas."

---

## 6. Dicionario de Defesa para Perguntas da Banca (Prof. Jose Denes)

### 1. "Por que somar 1 aos marcadores (`markers = markers + 1`)?"
**Resposta:** "Porque no OpenCV, o rotulo 0 e reservado exclusivamente para a regiao desconhecida, onde a inundacao acontece e as barragens sao disputadas. O `connectedComponents` rotula o fundo como 0. Se nao somassemos 1, o fundo seria interpretado como area de disputa e a imagem inteira seria destruida."

### 2. "Por que usar 70% da distancia maxima (`0.7 * max_dist`)?"
**Resposta:** "O valor de 0.7 foi obtido pela relacao geometrica entre o raio da moeda e o estrangulamento de contato. As moedas tem raio medio de 24 pixels. Nas pontas de contato a distancia cai para menos de 10 pixels, enquanto no centro mantem 24. Cortar em 70% elimina com seguranca os contatos mantendo os 24 centros isolados."

### 3. "O que significa o valor -1 retornado pelo Watershed?"
**Resposta:** "Representa os pixels das Watershed Lines, isto e, as barragens morfologicas de 1 pixel de espessura construidas quando a agua de duas bacias vizinhas ameacou se misturar."

### 4. "Por que o K-Means nao separa as moedas encostadas?"
**Resposta:** "Porque o K-Means e um agrupador puramente espectral. Ele nao recebe as coordenadas (x, y). Como duas moedas encostadas possuem a mesma cor de bronze, seus pixels caem no mesmo ponto do espaco de atributos e recebem o mesmo rotulo."

### 5. "Qual a vantagem do espaco L\*a\*b\* sobre o RGB no K-Means?"
**Resposta:** "No RGB, variacoes de sombra afetam R, G e B juntos, confundindo o calculo da distancia euclidiana. No espaco L\*a\*b\*, o canal L\* isola o brilho, enquanto a\* e b\* preservam a cromaticidade pura, tornando o agrupamento estavel contra sombras."
