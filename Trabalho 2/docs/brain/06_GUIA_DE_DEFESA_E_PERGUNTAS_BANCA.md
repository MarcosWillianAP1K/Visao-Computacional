# 06. Guia de Defesa e Banco de Perguntas da Banca Avaliadora
## Blindagem Individual para Nota Máxima (5,0 Pontos) com o Prof. Dr. José Denes Lima Araújo

---

## 1. Como Conquistar a Nota Máxima nos Critérios Individuais

A avaliação individual totaliza **5,0 pontos** distribuídos em:
- **Domínio da parte apresentada (2,0 pts):** Conhecimento seguro dos conceitos, fórmulas, hiperparâmetros e causas dos fenômenos observados.
- **Clareza e comunicação (2,0 pts):** Linguagem técnica formal de Visão Computacional, fluência verbal e concisão.
- **Participação, postura e envolvimento (1,0 pt):** Atenção ativa contínua, postura profissional em vídeo e prontidão no momento da arguição.

> [!TIP]
> **A Regra de Ouro da Sabatina Acadêmica:**  
> Nunca responda *"não sei"* ou dê respostas monossilábicas (*"sim"*, *"não"*). Quando o professor formular uma pergunta desafiadora:
> 1. Reconheça a relevância da pergunta (*"Excelente colocação, Professor Denes..."*).
> 2. Cite a teoria de base (ex: viés indutivo, regularização, *data leakage*).
> 3. Conecte com os dados empíricos dos artigos (ex: os 99% da UFCSPA ou os 79% do ViT-Small).
> 4. Se a resposta exigir uma hipótese, fundamente-a na literatura de Visão Computacional.

---

## 2. Perguntas e Respostas Técnicas: Artigo 1 (UFCSPA – CNN Brain Tumor)

### Pergunta 1.1: *"Por que os autores do Artigo 1 optaram por criar uma CNN customizada adaptada da AlexNet do zero, em vez de simplesmente usar uma ResNet-50 ou EfficientNet pré-treinada por transferência de aprendizado?"*
- **Intenção da Banca:** Verificar se o aluno entende o trade-off entre capacidade do modelo, sobreajuste (*overfitting*) e complexidade de inferência em imagens médicas.
- **Resposta Recomendada:**  
  *"Professor, essa escolha foi pautada pelo princípio da parcimônia arquitetural e prevenção contra o sobreajuste. Uma ResNet-50 possui mais de 25 milhões de parâmetros treináveis, enquanto uma EfficientNet-B0 possui cerca de 5 milhões. Em um conjunto de dados fatiado de ressonância com 5.500 imagens redimensionadas para $64 \times 64$, redes excessivamente profundas como a ResNet-50 sofrem com saturação de gradientes e rápida memorização de ruído (overfitting), mesmo com transferência de aprendizado. Ao desenhar uma CNN sob medida com apenas 3 blocos convolucionais (16, 32 e 64 filtros) e uma camada densa de 32 neurônios, os autores obtiveram um modelo extremamente leve, com baixa contagem de parâmetros, convergência acelerada em 60 épocas e capaz de rodar inferência em frações de milissegundo até em computadores de baixo custo de postos de saúde, atingindo 99% de acurácia sem a necessidade de sobrecarga computacional de uma ResNet."*
- **Armadilha a Evitar:** Não diga que os autores "não sabiam usar ResNet" ou que a AlexNet é "melhor que a ResNet". Destaque a adequação entre o tamanho da imagem ($64 \times 64$), o tamanho do dataset e a capacidade da rede.

---

### Pergunta 1.2: *"O que é o Grad-CAM e como ele funciona matematicamente no Artigo 1? Por que os autores precisaram validá-lo em uma base externa?"*
- **Intenção da Banca:** Avaliar o entendimento de Explicabilidade em Inteligência Artificial (XAI).
- **Resposta Recomendada:**  
  *"O Grad-CAM (Gradient-weighted Class Activation Mapping) é uma técnica de explicabilidade que calcula o gradiente da pontuação da classe predita $y^c$ em relação a cada mapa de ativação convolucional $A^k$ da última camada convolucional da rede. Esses gradientes são integrados por Global Average Pooling para gerar pesos de importância $\alpha_k^c$:*
  $$\alpha_k^c = \frac{1}{Z} \sum_{i} \sum_{j} \frac{\partial y^c}{\partial A_{i,j}^k}$$
  *Em seguida, realiza-se a combinação linear desses mapas com a função ReLU para reter apenas as feições com influência positiva no diagnóstico:*
  $$L_{\text{Grad-CAM}}^c = \text{ReLU}\left(\sum_k \alpha_k^c A^k\right)$$
  *Isso gera um mapa térmico bidimensional que é sobreposto à ressonância. A validação em base externa (Bhuvaji et al.) foi um ato de extremo rigor científico: os autores queriam comprovar que os mapas de calor não estavam 'sobreajustados' à iluminação e contraste do dataset de treino, provando que a rede de fato localiza a morfologia anatômica do tumor mesmo em imagens de scanners de ressonância não vistos previamente."*
- **Armadilha a Evitar:** Confundir Grad-CAM com CAM tradicional (CAM exige Global Average Pooling rígido antes da camada de classificação, enquanto o Grad-CAM aceita qualquer arquitetura convolucional via retropropagação de gradientes).

---

### Pergunta 1.3: *"Como os autores do Artigo 1 preveniram o vazamento de dados (Data Leakage) e qual a função do K-Fold Cross Validation?"*
- **Intenção da Banca:** Verificar o domínio de boas práticas metodológicas de aprendizado de máquina.
- **Resposta Recomendada:**  
  *"Para evitar vazamento de dados (data leakage), os autores adotaram duas medidas cruciais: primeiro, a separação entre treino e teste independente foi realizada antes de qualquer procedimento de normalização por 255 e transformações, garantindo que estatísticas de teste não vazassem para os parâmetros de treinamento. Segundo, utilizaram o K-Fold Cross Validation com 5 dobras no subconjunto de treino. Em cada dobra, 80% dos dados calibraram os pesos e 20% serviram como validação cega temporária. Além disso, aplicaram embaralhamento contínuo (data shuffling) das amostras a cada época para impedir que o otimizador Adam memorizasse a ordem das classes, resultando em curvas de aprendizado robustas e livres de viés sequencial."*

---

### Pergunta 1.4: *"No Artigo 1, por que os autores substituíram amostras da pasta Glioma pelo dataset Figshare? O que isso nos ensina sobre benchmarks públicos?"*
- **Intenção da Banca:** Testar a percepção crítica sobre qualidade de dados (*Data-Centric AI*).
- **Resposta Recomendada:**  
  *"Essa foi uma das contribuições mais valiosas da UFCSPA. Ao realizarem uma auditoria exploratória visual no dataset Brain Tumor do Kaggle, os autores descobriram a presença de rótulos incorretos (label noise): imagens classificadas como gliomas eram na verdade meningiomas ou cortes normais. Se a rede fosse treinada com esses dados contaminados, ela aprenderia falsas correlações. Eles substituíram cirurgicamente essas amostras pelas do dataset Figshare, que possui curadoria médica validada. Isso nos ensina que, em Visão Computacional Médica, o paradigma de Data-Centric AI é imperativo: antes de ajustar hiperparâmetros de redes profundas, é obrigatório auditar a integridade sanitária dos rótulos do dataset."*

---

## 3. Perguntas e Respostas Técnicas: Artigo 2 (PUC Minas / UFMG – ViT Patches Dinâmicos)

### Pergunta 2.1: *"No Artigo 2, como funciona a projeção linear e por que a projeção convolucional superou a linear em todos os testes de patches dinâmicos?"*
- **Intenção da Banca:** Entender se o aluno domina o mecanismo de entrada dos Vision Transformers.
- **Resposta Recomendada:**  
  *"Na formulação clássica do ViT de Dosovitskiy, uma imagem $224 \times 224$ é dividida em patches $16 \times 16 \times 3$. Na Projeção Linear, cada patch achatado de 768 números é multiplicado por uma matriz linear $E$ para virar um vetor embedding de dimensão $D$. Isso significa que o modelo não possui nenhuma noção espacial prévia sobre o conteúdo daquele patch. Já na Projeção Convolucional, aplica-se uma camada Conv2D com kernel $16 \times 16$, stride $16$ e $D$ canais de saída. A convolução atua como um filtro espacial local contínuo que extrai gradientes de cor e bordas morfológicas do núcleo celular antes de enviar os tokens para o Transformer. Conforme demonstrado na Tabela 2, a abordagem convolucional superou a linear em todos os cinco métodos dinâmicos (por exemplo, na Espiral saltou de 0,69 para 0,78), exatamente porque reintroduziu o viés indutivo de localidade que a projeção linear pura ignora."*

---

### Pergunta 2.2: *"Por que a técnica de extração em Grid Regular convencional superou todas as 5 propostas dinâmicas (GrabCut, Espiral, etc.)?"*
- **Intenção da Banca:** Explorar a discussão crítica central e a compreensão do "resultado negativo" do artigo.
- **Resposta Recomendada:**  
  *"Professor, essa foi a descoberta experimental mais contundente do artigo. O grid regular obteve 79% de acurácia no teste contra 78% da Espiral e 76% do GrabCut. Isso decorreu de três fatores interligados:*
  *1. Sobreposição Espacial Excessiva (Over-Clustering): Ao forçar 196 patches a convergirem sobre um núcleo celular de apenas 90 por 90 pixels, os patches sobrepuseram-se em mais de 80%, tornando os vetores de consulta e chave quase idênticos e saturando a atenção em redundância inútil.*
  *2. Destruição dos Positional Embeddings: Os pesos pré-treinados na ImageNet-21k aprenderam representações posicionais de uma grade cartesiana rígida $14 \times 14$. Amostragens aleatórias ou em espiral distorceram essa ordem espacial aprendida.*
  *3. Supressão do Citoplasma Marginal: O diagnóstico do Sistema Bethesda exige avaliar a relação núcleo-citoplasma. Ao concentrar todos os patches dinamicamente no núcleo, o modelo perdeu a visão global do citoplasma periférico, que o grid convencional captura perfeitamente."*

---

### Pergunta 2.3: *"Como funciona o algoritmo GrabCut na técnica de Seleção por Segmentação (SS) e qual o papel do fallback de 10%?"*
- **Intenção da Banca:** Verificar o conhecimento de processamento clássico de imagens associado ao aprendizado profundo.
- **Resposta Recomendada:**  
  *"O GrabCut é um algoritmo de segmentação interativa baseado em Modelos de Mistura Gaussiana (GMM) e cortes em grafos (Graph Cut / Min-Cut/Max-Flow) desenvolvido por Rother et al. No Artigo 2, o algoritmo é automatizado para inicializar um retângulo delimitador ao redor da célula, modelando as distribuições de cor do núcleo e do citoplasma em relação ao fundo branco da lâmina e convergindo iterativamente para uma máscara binária do objeto celular. Os centros dos 196 patches dinâmicos foram restritos exclusivamente aos pixels brancos (foreground) dessa máscara. Contudo, em células muito pequenas ou em detritos celulares, a máscara gerada poderia conter pouquíssimos pixels. Para evitar divisões por zero ou superconcentração de centenas de patches sobre uma área quase pontual, os autores implementaram um mecanismo de fallback: se a máscara binária representasse menos de 10% da área da imagem, o algoritmo abortava a seleção dinâmica e recorria à extração em grade regular uniforme."*

---

### Pergunta 2.4: *"Por que o modelo ViT-Base, apesar de ter muito mais parâmetros que o ViT-Small, apresentou acurácia inferior tanto no baseline quanto nos dinâmicos?"*
- **Intenção da Banca:** Testar a compreensão prática de infraestrutura de treinamento e subajuste por congelamento excessivo.
- **Resposta Recomendada:**  
  *"O ViT-Base possui aproximadamente 86 milhões de parâmetros, contra 22 milhões do ViT-Small. Os autores reportaram que, devido ao limite de memória da GPU Tesla T4 (15 GB) no Google Colab PRO e para evitar estouro de memória, eles só conseguiram descongelar o último bloco MLP do codificador do ViT-Base, mantendo todas as outras 11 camadas de atenção estritamente congeladas. Em contraste, no ViT-Small (que rodou localmente na RTX 2060), eles descongelaram os 2 primeiros blocos e os 3 últimos blocos do codificador. Como o ViT-Small teve muito mais camadas livres para adaptar suas matrizes de atenção aos padrões histológicos da citologia cervical, ele generalizou substancialmente melhor (79% contra 75% do ViT-Base). Isso ilustra um clássico trade-off de engenharia: um modelo menor com descongelamento estratégico supera um modelo gigante sub-treinado e excessivamente congelado."*

---

## 4. Perguntas de Confronto e Visão Computacional Teórica

### Pergunta 3.1: *"Se uma CNN com 3 blocos atingiu 99% de acurácia no Artigo 1, por que o Vision Transformer do Artigo 2 sofreu para chegar a 79%, e um Ensemble de CNNs (Diniz et al.) chegou a 95% na mesma base CRIC?"*
- **Intenção da Banca:** Testar o cerne da discussão teórica do seminário (Viés Indutivo vs Autoatenção Global).
- **Resposta Recomendada:**  
  *"Professor, a explicação reside no conceito de Viés Indutivo (Inductive Bias) e no fenômeno de Fome de Dados (Data-Hunger). As Redes Neurais Convolucionais possuem operadores matemáticos fixos que forçam o aprendizado a respeitar a conectividade local e a invariância à translação. O modelo da UFCSPA aplicou essa estrutura a um problema onde o tumor é uma massa macroscópica evidente em ressonância. Já na base CRIC do Artigo 2, a tarefa é uma classificação sutil entre 6 graus celulares contínuos do Sistema Bethesda, onde a diferença entre ASC-US e HSIL é milimétrica. Os Vision Transformers não assumem localidade a priori; eles tratam os patches como uma sequência desordenada e calculam correlações all-to-all. Para aprender a geometria visual sem viés prévio, o ViT requer dezenas de milhões de imagens. Em um dataset médico de apenas 6.000 imagens de treino balanceadas, o ViT sofre de sub-aprendizado estrutural, motivo pelo qual tanto a CNN customizada do Artigo 1 quanto o Ensemble de CNNs de Diniz et al. (95%) superaram com ampla folga o Transformer."*

---

### Pergunta 3.2: *"O Artigo 2 dividiu os dados estritamente por paciente. Por que isso é importante e qual é o risco análogo no Artigo 1?"*
- **Intenção da Banca:** Avaliar se o grupo entende a diferença entre separação por imagem (*slice-level*) e por indivíduo (*patient-level*).
- **Resposta Recomendada:**  
  *"A estratificação por paciente é o padrão-ouro na IA médica para evitar data leakage espúrio. Cada lâmina citológica possui variações específicas de pH, tempo de exposição ao corante e espessura do esfregaço daquela paciente. Se o particionamento fosse aleatório no nível de células, células da mesma lâmina estariam no treino e no teste, permitindo que a rede atingisse acurácia inflada simplesmente memorizando o tom de fundo da lâmina daquela paciente, e não a atipia celular. No Artigo 1, os autores fatiaram exames de ressonância magnética volumétrica 2D do Kaggle. Há um risco metodológico potencial de que fatias adjacentes do crânio do mesmo indivíduo tenham caído simultaneamente no treino e no teste (slice leakage). O grupo da UFCSPA mitigou essa incerteza de forma elegante ao demonstrar que a explicabilidade via Grad-CAM generalizou com perfeição em um dataset externo inédito, mas metodologicamente a divisão por paciente do Artigo 2 é mais rigorosa."*

---

### Pergunta 3.3: *"Se vocês fossem continuar a pesquisa do Artigo 2 sobre citologia cervical, quais modificações proporiam para fazer o Vision Transformer superar a CNN?"*
- **Intenção da Banca:** Avaliar pensamento crítico propositivo e visão de futuro em IA.
- **Resposta Recomendada:**  
  *"Proporíamos três intervenções técnicas fundamentais:*  
  *1. Adoção de Arquiteturas Hierárquicas como o Swin Transformer:* Em vez de manter patches rígidos $16 \times 16$ com atenção global quadrática, o Swin Transformer computa atenção em janelas locais deslocadas (*Shifted Windows*), reinjetando o viés de localidade das CNNs com a expressividade da atenção multi-escala.*  
  *2. Positional Embeddings Deformáveis / 2D Contínuos:* Se mantivéssemos a amostragem em espiral, calcularíamos embeddings posicionais senoidais contínuos baseados na distância euclidiana radial real de cada patch em relação ao núcleo, em vez de usar os embeddings discretos 1D da ImageNet.*  
  *3. Aumento Sintético Massivo com Modelos de Difusão ou GANs:* Para saciar a fome de dados do ViT na classe minoritária de carcinoma (SCC, que só tinha 103 amostras originais), geraríamos amostras sintéticas fotorrealistas de alta fidelidade morfológica, expandindo a base de treino para além de 50.000 núcleos balanceados."*

---

## 5. Matriz Rápida de Resposta de Emergência

Caso o professor faça uma pergunta muito específica e o grupo hesite por 3 segundos, consulte mentalmente este resumo executivo:

```
+-----------------------------------+---------------------------------------------------------------+
| CONCEITO QUESTIONADO              | RESPOSTA-CHAVE EM 1 FRASE                                     |
+-----------------------------------+---------------------------------------------------------------+
| Por que Dropout progressivo?      | Preserva bordas nas primeiras camadas e evita coadaptação     |
|                                   | de feições complexas nas camadas profundas.                   |
| Por que Softmax na saída?         | Converte logits em distribuição de probabilidades normalizada |
|                                   | que soma 1.0 sobre as classes mutuamente exclusivas.          |
| O que faz o Early Stopping?       | Monitora a loss de validação e interrompe o treino se não     |
|                                   | houver melhora após paciência de 18 épocas (evita overfit).   |
| Por que Albumentations no CRIC?   | Fornece transformações afins seguras (flips, rotações) para   |
|                                   | oversampling das classes raras sem deformar a morfologia.     |
| O que é o token [CLS]?            | Token vetorial prefixado à sequência que agrega a atenção de  |
|                                   | todos os outros 196 patches para alimentar a decisão final.   |
| Complexidade do ViT vs CNN?       | Autoatenção é O(N²) quadrática na quantidade de patches;     |
|                                   | Convolução é O(H·W) linear no tamanho espacial da imagem.     |
+-----------------------------------+---------------------------------------------------------------+
```
