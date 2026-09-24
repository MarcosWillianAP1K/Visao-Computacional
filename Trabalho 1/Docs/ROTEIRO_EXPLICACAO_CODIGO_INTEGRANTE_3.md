# Roteiro de Apresentacao e Explicacao do Codigo
**UFPI - Campus Senador Helvidio Nunes de Barros**  
**Disciplina:** Topicos Especiais em Visao Computacional  
**Professor:** Prof. Me. Jose Denes Lima Araujo  
**Grupo 4:** Tecnicas de Segmentacao Baseada em Regiao (Secao 10.5 - Gonzalez & Woods)  
**Apresentador:** Integrante 3 (O Analista Experimental)  
**Tempo estimado:** 4 a 5 minutos (Slides 9 ao 13)

---

## 1. Entrada e Frase de Transicao
Assim que o Integrante 2 concluir a fundamentacao teorica, assuma a palavra com firmeza:

> "Obrigado, [Nome do Integrante 2]. Agora que compreendemos a formulacao teorica do Watershed e do K-Means, eu vou apresentar os nossos experimentos praticos em codigo, demonstrando o comportamento real de cada tecnica com imagens do mundo real."

---

## 2. Slide 9: Aplicacao Pratica 1 - Watershed em Objetos Sobrepostos

### Imagem a projetar:
Painel com as 6 etapas (`watershed_pipeline_completo.png`).

### Roteiro de fala:
> "No nosso primeiro experimento, abordamos um dos problemas mais classicos da visao computacional industrial: a segmentacao de objetos em contato. Aqui temos 24 moedas circulares sobre fundo claro.
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

## 3. Slide 10: Aplicacao Pratica 2 - K-Means em Segmentacao Colorida

### Imagem a projetar:
Painel com a variacao de K (`kmeans_comparativo_k.png`) e as mascaras isoladas de K=3 (`kmeans_mascaras_k3.png`).

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

## 4. Slide 11: Confronto Pratico 1 - Cenario das Moedas (A Forca do Watershed)

### Imagem a projetar:
Duelo das moedas (`comparativo_toque_moedas.png`).

### Roteiro de fala:
> "Para aprofundar a analise, fizemos um confronto direto aplicando ambos os algoritmos exatamente nas mesmas imagens.
>
> Aqui no Cenario 1, submetemos as moedas encostadas ao K-Means e ao Watershed:
> - O K-Means com K=2, visto na figura (b), falha totalmente na separacao por toque. Como todas as moedas sao de bronze e tem a mesma assinatura espectral de cor, o K-Means joga todos os pixels das moedas no mesmo cluster, gerando um unico bloco continuo indiferenciado.
> - Ja o Watershed, visto na figura (c), utiliza o relevo topografico da Transformada de Distancia e ergue barragens nos pontos de estrangulamento geometrico, individualizando com perfeicao todas as 24 moedas.
>
> Conclusao do Cenario 1: O Watershed vence de forma absoluta quando o desafio envolve separacao de objetos em contato com geometria regular e cores homogeneas."

---

## 5. Slide 12: Confronto Pratico 2 - Cenario da Borboleta (A Forca do K-Means)

### Imagem a projetar:
Duelo da cena natural (`comparativo_cena_borboleta.png`).

### Roteiro de fala:
> "Agora, olhem o que acontece quando invertemos o cenario e submetemos uma cena natural rica em texturas, sombras e cores a ambos os metodos:
> - O K-Means com K=3 em L\*a\*b\*, visto na figura (b), atinge um resultado semantico limpo e estavel. Ele separa com facilidade os tres planos (objeto, folhagem e fundo), mesmo com contornos difusos e iluminacao irregular.
> - Ja o Watershed, visto na figura (c), se aplicado sobre o gradiente sem marcadores manuais ultra especializados, sofre de sobre-segmentacao severa (over-segmentation). Como a folha possui nervuras e as asas tem escamas e padroes finos, o gradiente gerou mais de 5.700 micro-bacias locais, fatiando a imagem inteira em linhas vermelhas irrelevantes, exatamente como previsto na Figura 10.57 do livro de Gonzalez & Woods.
>
> Conclusao do Cenario 2: O K-Means vence com folga em cenas naturais onde as fronteiras sao texturizadas ou difusas, situacao em que o Watershed puro se perde no excesso de ruidos locais."

---

## 6. Slide 13: Sintese Comparativa e Recomendacoes de Engenharia

### Imagem a projetar:
Tabela sintese das tres dimensoes tecnicas e diretrizes finais.

| Dimensao Tecnica | Transformada de Watershed | Clustering K-Means | Vencedor Pratico |
| :--- | :--- | :--- | :--- |
| **Separacao de Toque** | Modela o estrangulamento via relevo da distancia e ergue barragens conexas. | Cego a geometria espacial: cores iguais fundem-se no mesmo cluster. | **Watershed** (Cenario 1) |
| **Cenas Naturais e Texturas** | Sofre sobre-segmentacao severa no gradiente sem marcadores refinados. | Agrupa planos de cor com estabilidade sob o espaco L\*a\*b\*. | **K-Means** (Cenario 2) |
| **Dependencia de Bordas** | Elevada: exige transicoes continuas no gradiente ou formas regulares. | Nula: segmenta cores mesmo com bordas difusas ou inexistentes. | **K-Means** |
| **Prontidao para Metrologia** | Imediata: entrega rotulos individuais prontos para contagem e area. | Requer pos-processamento de analise de componentes conexos. | **Watershed** |

### Roteiro de fala:
> "Sintetizando as nossas recomendacoes praticas de engenharia de visao computacional:
>
> - Utilize a Transformada de Watershed com Marcadores em aplicacoes industriais e laboratoriais voltadas para contagem automatizada e metrologia (ex: controle de qualidade de pecas, contagem de comprimidos, celulas em microscopia e graos).
> - Utilize o Clustering K-Means e a sua evolucao em Superpixels (SLIC) para simplificacao de cenas fotograficas, quantizacao de paletas de cor, remocao de fundo e como pre-processamento semantico para redes neurais profundas.
>
> Nossa bibliografia oficial foi o livro Processamento Digital de Imagens de Rafael C. Gonzalez e Richard E. Woods, capitulo 10, secao 10.5 da 3ª e da 4ª Edicoes.
> Agradecemos a atencao do professor Jose Denes e dos colegas, e estamos a disposicao para as perguntas da banca."

---

## 7. Dicionario de Defesa para Perguntas da Banca (Prof. Jose Denes)

### 1. "Por que somar 1 aos marcadores (`markers = markers + 1`) no Watershed?"
**Resposta:** "Porque na implementacao `cv2.watershed` do OpenCV, o rotulo 0 e reservado exclusivamente para a regiao desconhecida, onde a inundacao acontece e as barragens sao disputadas. O `connectedComponents` rotula o fundo como 0. Se nao somassemos 1, o fundo seria interpretado como area de disputa e a imagem inteira seria destruida."

### 2. "Por que usar 70% da distancia maxima (`0.7 * max_dist`)?"
**Resposta:** "O valor de 0.7 foi obtido pela relacao geometrica entre o raio da moeda e o estrangulamento de contato. As moedas tem raio medio de 24 pixels. Nas pontas de contato a distancia cai para menos de 10 pixels, enquanto no centro mantem 24. Cortar em 70% elimina com seguranca os contatos mantendo os 24 centros isolados."

### 3. "O que significa o valor -1 retornado pelo Watershed?"
**Resposta:** "Representa os pixels das Watershed Lines, isto e, as barragens morfologicas de 1 pixel de espessura construidas quando a agua de duas bacias vizinhas ameacou se misturar."

### 4. "Por que o K-Means falha nas moedas, mas vence na borboleta?"
**Resposta:** "Porque o K-Means avalia apenas cor e nao coordenadas espaciais. Nas moedas, como todas tem a mesma cor de bronze, o K-Means nao enxerga o toque e une tudo em um bloco. Ja na borboleta, a imagem possui diferencas tonais claras entre objeto, folha e fundo, entao o K-Means isola os planos com perfeicao, enquanto o Watershed gera mais de 5.700 bacias no gradiente por causa das nervuras e texturas."

### 5. "Qual a vantagem do espaco L\*a\*b\* sobre o RGB no K-Means?"
**Resposta:** "No RGB, variacoes de sombra afetam R, G e B juntos, distorcendo a distancia euclidiana. No espaco L\*a\*b\*, o canal L\* isola o brilho, enquanto a\* e b\* preservam a cromaticidade pura, tornando o agrupamento estavel contra sombras."

### 6. "Como o algoritmo SLIC resolve a limitacao espacial do K-Means?"
**Resposta:** "O SLIC expande o vetor de atributos de 3D para 5D: `z = [L*, a*, b*, x, y]^T`. Ao incluir as coordenadas espaciais x e y ponderadas e restringir a busca a janelas locais de 2S x 2S, o SLIC forca os pixels agrupados a serem vizinhos contiguos, eliminando o problema de misturar pixels distantes."
