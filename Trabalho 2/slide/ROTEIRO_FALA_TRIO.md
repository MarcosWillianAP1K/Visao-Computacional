# Roteiro Completo de Fala e Ensaio para o Trio (Grupo 4)
## Guia de Apresentação Oral, Marcação Minuto a Minuto e Transições Formais
### Disciplina: Tópicos Especiais em Visão Computacional — UFPI | Prof. Dr. José Denes Lima Araújo

---

## 1. Visão Geral da Gestão de Tempo e Critérios de Avaliação

Para atingir a nota máxima (**5,0 pontos individuais** e **5,0 pontos de grupo**):
- **Tempo Mínimo Exigido:** 30 minutos (abaixo de 30 minutos acarreta penalidade severa por falta de densidade analítica).
- **Tempo Máximo Permitido:** 40 minutos (interrupção mandatória pela banca).
- **Tempo Alvo do Grupo 4:** **34 a 36 minutos** (zona de segurança com 4 minutos de folga para imprevistos).

```
Cronograma Geral da Sessão Oral (00:00 a 40:00):
┌───────────────────────────┬───────────────┬───────────────────────────────┬──────────────┐
│ BLOCO TEMÁTICO            │ RESPONSÁVEL   │ CONTEÚDO PRINCIPAL            │ TEMPO-ALVO   │
├───────────────────────────┼───────────────┼───────────────────────────────┼──────────────┤
│ Bloco 1: Abertura & CNN   │ Integrante 1  │ Contexto Clínico, Auditoria   │ 00:00 - 11:30│
│ (Tumores Cerebrais UFCSPA)│               │ Figshare, AlexNet, Grad-CAM   │ (11 min 30s) │
├───────────────────────────┼───────────────┼───────────────────────────────┼──────────────┤
│ Bloco 2: ViTs Dinâmicos   │ Integrante 2  │ Citologia Bethesda, CRIC,     │ 11:30 - 23:00│
│ (Lâminas PUC Minas/UFMG)  │               │ Split Paciente, 5 Dinâmicos   │ (11 min 30s) │
├───────────────────────────┼───────────────┼───────────────────────────────┼──────────────┤
│ Bloco 3: Comparação &     │ Integrante 3  │ Causa-Raiz, Duelo Viés/ViT,   │ 23:00 - 34:30│
│ Discussão Crítica         │               │ Matriz 16 Eixos, Decisão      │ (11 min 30s) │
├───────────────────────────┼───────────────┼───────────────────────────────┼──────────────┤
│ Bloco 4: Encerramento     │ Trio Coletivo │ Resposta às perguntas do      │ 34:30 - 40:00│
│ e Sabatina da Banca       │               │ Prof. Dr. José Denes          │ (05 min 30s) │
└───────────────────────────┴───────────────┴───────────────────────────────┴──────────────┘
```

---

## 2. Bloco 1: Abertura Institucional e Artigo 1 (UFCSPA — CNN)
**Orador:** Integrante 1 (Aluno 1)  
**Tempo Total:** 00:00 a 11:30 (11 minutos e 30 segundos)  
**Slides:** 01 ao 10

---

### [00:00 - 01:00] Slide 01: Capa Institucional e Apresentação do Grupo
> **Slide Exibido:** *Convoluções Clássicas vs. Vision Transformers na Saúde — Grupo 4*

**Fala Exata do Aluno 1:**
> *"Bom dia/boa tarde a todos os presentes. Cumprimento cordialmente o Prof. Dr. José Denes Lima Araújo e os colegas de curso. Sou o [Nome do Aluno 1] e, juntamente com meus colegas [Nome do Aluno 2] e [Nome do Aluno 3], compomos o Grupo 4 da disciplina de Tópicos Especiais em Visão Computacional.  
> Hoje apresentaremos nossa análise comparativa multidimensional e discussão crítica a respeito de dois artigos completos publicados nos anais da Sociedade Brasileira de Computação (SBC). O primeiro trabalho, publicado no BRACIS 2023 por pesquisadores da UFCSPA, propõe uma rede neural convolucional sob medida para o diagnóstico diferencial de tumores cerebrais em ressonância magnética. O segundo trabalho, publicado em 2025 pela PUC Minas e UFMG, investiga o comportamento dos Vision Transformers acoplados a cinco métodos dinâmicos de extração de patches na citopatologia do colo uterino. Nosso objetivo não é apenas resumir os artigos, mas dissecar suas escolhas de engenharia, confrontar seus dados empíricos e debater a teoria de viés indutivo frente à autoatenção global."*

---

### [01:00 - 02:00] Slide 02: Estrutura do Seminário e Cronograma Oral
> **Slide Exibido:** *Estrutura do Seminário e Cronograma Oral (Meta: 34 a 36 Minutos)*

**Fala Exata do Aluno 1:**
> *"Para garantirmos máxima profundidade analítica em estrita consonância com a janela regulamentar de 30 a 40 minutos estipulada pelo edital, planejamos nossa explanação em três blocos balanceados.  
> No primeiro bloco, que conduzirei pelos próximos dez minutos, apresentarei os desafios singulares da IA médica e a desconstrução técnica completa do Artigo 1, detalhando a higienização de rótulos com o Figshare, a arquitetura convolucional adaptada da AlexNet, o protocolo K-Fold e os mapas de explicabilidade Grad-CAM.  
> Em seguida, o colega [Aluno 2] assumirá a palavra no Bloco 2 para apresentar o Artigo 2, abordando a citologia de Papanicolau no Sistema Bethesda, a blindagem contra vazamento de dados por paciente e os cinco métodos de amostragem dinâmica de patches.  
> Por fim, o colega [Aluno 3] liderará o Bloco 3 com a discussão crítica de causa-raiz do paradoxo do grid, o duelo teórico entre viés indutivo e fome de dados, a matriz comparativa em 16 dimensões e as conclusões, abrindo para a arguição do professor."*

---

### [02:00 - 03:30] Slide 03: Desafios Singulares da Visão Computacional Médica
> **Slide Exibido:** *Desafios Singulares da Visão Computacional Médica*

**Fala Exata do Aluno 1:**
> *"Antes de adentrarmos nas redes, é mandatório compreender por que a visão computacional na saúde não pode ser tratada como a classificação de imagens do cotidiano. Em bancos como a ImageNet, temos milhões de fotos comuns e o erro tem custo desprezível. Na medicina, enfrentamos quatro restrições críticas:  
> Primeiro, a escassez extrema de dados rotulados, pois cada segmentação exige horas de especialistas seniores.  
> Segundo, o desbalanceamento intrínseco: patologias altamente letais, como carcinomas invasivos, representam frações minúsculas da rotina de triagem.  
> Terceiro, o custo assimétrico do erro: classificar um exame normal como suspeito gera ansiedade e repetição de teste; porém, classificar um tumor maligno letal como sadio — um falso-negativo — pode custar a vida do paciente.  
> E quarto, a exigência de explicabilidade clínica: conselhos médicos e órgãos reguladores não aceitam caixas-pretas que não justifiquem espacialmente onde concentraram a atenção.  
> Observamos ainda duas escalas geométricas distintas nesta apresentação: a macroestrutura encefálica em ressonância magnética do Artigo 1 e a microestrutura celular citológica do Artigo 2."*

---

### [03:30 - 05:00] Slide 04: Artigo 1 (UFCSPA) — Contexto Clínico e Neoplasias Encefálicas
> **Slide Exibido:** *Contexto Clínico: Neoplasias Encefálicas (BRACIS 2023)*

**Fala Exata do Aluno 1:**
> *"Iniciando a desconstrução do Artigo 1, de autoria de Felipe, Pianoschi Alva, Winck e Becker, da Universidade Federal de Ciências da Saúde de Porto Alegre, o problema clínico abordado é a classificação diferencial de quatro condições em exames de ressonância magnética encefálica.  
> O Glioma é uma neoplasia com origem nas células gliais, altamente infiltrativa, com bordas indistintas e taxa de letalidade severa, exigindo ressecção cirúrgica emergencial.  
> O Meningioma desenvolve-se nas meninges aracnoides, sendo predominantemente benigno, encapsulado e de crescimento lento, apresentando o sinal clássico de 'cauda dural'.  
> A classe 'Sem Tumor' representa o tecido cerebral sadio, indispensável para calibrar algoritmos de triagem sem disparar falsos alarmes em hospitais.  
> E o Adenoma de Hipófise localiza-se na sela túrcica, provocando graves distúrbios neuroendócrinos e compressão do quiasma óptico.  
> O propósito dos autores foi desenhar um modelo convolucional leve e computacionalmente parcimonioso, capaz de operar em computadores convencionais de hospitais públicos sem a necessidade de clusters caros de GPU."*

---

### [05:00 - 06:30] Slide 05: Auditoria Crítica da Base e Substituição com Figshare
> **Slide Exibido:** *Auditoria Crítica da Base: Descoberta de Label Noise*

**Fala Exata do Aluno 1:**
> *"Aqui chegamos a uma das maiores contribuições metodológicas do artigo, alinhada à moderna filosofia de Data-Centric AI.  
> Os autores recorreram inicialmente ao popular benchmark público Brain Tumor MRI Dataset do Kaggle, curado por Nickparvar e Bhuvaji, que conta com mais de 7 mil imagens fatiadas em 2D.  
> Contudo, ao realizarem uma rigorosa auditoria exploratória visual, os pesquisadores descobriram que a pasta da classe Glioma continha diversas imagens com rotulagem incorreta — o chamado label noise. Havia ali cortes com meningiomas evidentes e até exames completamente normais catalogados como gliomas.  
> Se a rede fosse treinada com essa base contaminada, os gradientes aprenderiam correlações espúrias. Em vez de prosseguir com o ruído, os autores expurgaram cirurgicamente as imagens corrompidas e as substituíram por instâncias auditadas e validadas por radiologistas do repositório Figshare.  
> A partição final consolidou-se em 5.531 imagens para treinamento e validação interna e 1.297 imagens isoladas estritamente para o teste cego final."*

---

### [06:30 - 07:45] Slide 06: Pré-Processamento, Ponderação e Anti-Leakage
> **Slide Exibido:** *Pré-Processamento, Ponderação e Anti-Leakage*

**Fala Exata do Aluno 1:**
> *"No pipeline de pré-processamento, todas as fatias de ressonância magnética foram redimensionadas para uma matriz enxuta de 64 por 64 pixels e normalizadas dividindo-se o valor dos pixels por 255, estabelecendo o intervalo contínuo entre 0.0 e 1.0. Essa compressão espacial foi deliberada para reduzir exponencialmente a contagem de pesos da rede e viabilizar inferência instantânea.  
> Para mitigar o desbalanceamento intrínseco — onde gliomas representavam apenas 20,4% da base de treino contra quase 29% de casos normais —, os pesquisadores evitaram gerar dados artificiais e injetaram pesos inversamente proporcionais diretamente na função Sparse Categorical Cross-Entropy. O peso atribuído ao glioma foi de 1.21, ao passo que o caso sem tumor recebeu 0.86. Ou seja: errar um glioma gerava uma penalidade matemática 40% superior.  
> Crucial sublinhar: a partição de teste foi isolada antes da normalização, eliminando contaminação estatística, e os lotes foram reembaralhados a cada época para impedir vícios de memorização da ordem das classes."*

---

### [07:45 - 09:00] Slide 07: Arquitetura da Rede Convolucional Proposta
> **Slide Exibido:** *Rede Neural Convolucional Inspirada na AlexNet*

**Fala Exata do Aluno 1:**
> *"A arquitetura proposta foi concebida a partir dos princípios clássicos da AlexNet, porém adaptada e miniaturizada para processar entradas de 64 por 64 pixels.  
> Trata-se de uma rede modular composta por três blocos convolucionais em sequência. Cada bloco possui filtros convolucionais 3 por 3 com ativação ReLU, max-pooling 2 por 2 com stride 2 e uma taxa de Dropout progressivo. A contagem de canais dobra a cada bloco: 16 filtros no primeiro, 32 no segundo e 64 no terceiro, capturando sucessivamente bordas primitivas, texturas encefálicas e padrões tumorais complexos.  
> Chamo especial atenção para a estratégia de regularização progressiva: o Dropout inicia em 20% no primeiro bloco, para evitar que filtros de borda sejam destruídos; sobe para 25% no segundo; e atinge 30% no terceiro bloco, impedindo que feições abstratas coadaptem-se em sobreajuste.  
> Na transição para o classificador, após a vetorização com Flatten, uma camada densa compacta com apenas 32 neurônios conta com penalização de norma L2, culminando em 4 neurônios com ativação Softmax para fornecer a distribuição de probabilidades das quatro classes."*

---

### [09:00 - 10:15] Slide 08: Pipeline de Treinamento e Callbacks Inteligentes
> **Slide Exibido:** *Pipeline de Treinamento e Callbacks Inteligentes*

**Fala Exata do Aluno 1:**
> *"Para assegurar confiabilidade estatística e garantir que as métricas não fossem fruto de um particionamento conveniente, os autores adotaram validação cruzada K-Fold com 5 dobras estratificadas sobre as 5.531 amostras. Em cada rodada, 80% dos dados calibraram os gradientes sob o otimizador Adam e 20% serviram como validação interna cega.  
> O treinamento foi governado por uma trindade de callbacks inteligentes:  
> Primeiro, um Early Stopping monitorando a perda de validação com paciência de 18 épocas, encerrando o treinamento preventivamente caso o modelo entrasse em platô.  
> Segundo, o callback ReduceLROnPlateau, que reduzia a taxa de aprendizado em 80% (fator 0.2) caso a perda de validação estagnasse por 5 épocas seguidas, permitindo que os gradientes fizessem ajustes micrométricos no vale da função de perda.  
> E terceiro, o ModelCheckpoint, que gravava em disco apenas a matriz de pesos que atingisse o menor valor histórico de perda de validação, descartando qualquer época posterior com tendência a sobreajuste."*

---

### [10:15 - 11:30] Slide 09: Resultados Quantitativos (Acurácia de 99%)
> **Slide Exibido:** *Resultados Quantitativos: 99% de Acurácia Global*

**Fala Exata do Aluno 1:**
> *"Ao avaliarem o modelo sobre o conjunto de teste independente com 1.311 imagens nunca vistas durante o treinamento, o resultado foi impressionante: acurácia global consolidada de 99,0%.  
> Do ponto de vista clínico-oncológico, o dado mais contundente da Tabela de Classificação reside na classe Glioma: a rede alcançou precisão de 1,00, revocação de 1,00 e F1-score de 1,00 em todas as 286 amostras de teste.  
> Isto significa que o modelo produziu exatamente zero falso-negativo para a neoplasia mais letal e agressiva do encéfalo. Em um ambiente hospitalar, nenhum paciente portador de glioma deixaria de ser diagnosticado por este algoritmo.  
> Para as demais patologias, o desempenho manteve o mesmo padrão de excelência: Meningioma com F1 de 0,98, Hipófise com 0,99 e a classe Normal com 0,99, refletindo curvas ROC com áreas sob a curva virtualmente unitárias para todas as classes."*

---

### [11:30 - 12:30] Slide 10: Explicabilidade (XAI) com Grad-CAM e Validação Externa
> **Slide Exibido:** *Explicabilidade com Grad-CAM e Validação Externa*

**Fala Exata do Aluno 1:**
> *"Em inteligência artificial médica, um modelo de 99% de acurácia que não seja explicável é prontamente descartado pelos corpos clínicos. Para garantir que a rede não estava decidindo com base em marcas do scanner, ossos do crânio ou ruídos de borda, os autores aplicaram a técnica Grad-CAM sobre o último bloco convolucional.  
> O Grad-CAM calcula o gradiente da classe prevista em relação aos mapas de feição e aplica uma função retificadora linear ReLU, destacando apenas os sinais que corroboram o diagnóstico. Os mapas térmicos provam que a ativação da rede coincide com exatidão cirúrgica sobre o epicentro da massa tumoral e bordas de edema.  
> Mais rigoroso ainda: os pesquisadores executaram o Grad-CAM em imagens de uma base de ressonância externa completamente inédita (Bhuvaji et al.), onde a rede manteve o foco correto na lesão, comprovando que a explicabilidade visual generaliza além do hospital de origem."*

---

### Frase de Transição Formal (Aluno 1 ➔ Aluno 2):
> **[Aluno 1 olhando para a câmera e dirigindo-se ao colega]:**  
> *"Com estes resultados promissores no domínio convolucional de tumores cerebrais, encerro o primeiro bloco de nossa apresentação e passo a palavra ao colega [Nome do Aluno 2], que nos guiará pela desconstrução do Artigo 2, abordando o paradigma emergente dos Vision Transformers com extração dinâmica de patches na citopatologia cervical."*

---

## 3. Bloco 2: Artigo 2 (PUC Minas / UFMG — Vision Transformers)
**Orador:** Integrante 2 (Aluno 2)  
**Tempo Total:** 12:30 a 23:00 (10 minutos e 30 segundos)  
**Slides:** 11 ao 18

---

### [12:30 - 14:00] Slide 11: Artigo 2 — Citologia Cervical e Sistema Bethesda
> **Slide Exibido:** *Citopatologia Cervical e o Sistema Bethesda (SBC 2025)*

**Fala Exata do Aluno 2:**
> *"Muito obrigado, [Aluno 1]. Cumprimento o Professor José Denes e a todos os presentes.  
> Assumo o segundo bloco para analisarmos o Artigo 2, publicado em 2025 nos anais da SBC por Vinícius Giovanini e pelo Professor Alexei Machado, da PUC Minas e da Faculdade de Medicina da UFMG.  
> O problema enfrentado é o rastreamento citopatológico precoce do câncer de colo de útero, a quarta neoplasia com maior mortalidade feminina no mundo, diagnosticada por meio do preventivo de Papanicolau.  
> O diagnóstico foi modelado segundo o padrão internacional do Sistema Bethesda, composto por seis categorias celulares:  
> Células completamente sadias (NFIL);  
> Atipias de significado indeterminado em células escamosas (ASC-US e ASC-H);  
> Lesões intraepiteliais de baixo grau (LSIL) e de alto grau (HSIL), que representam estados pré-malignos;  
> E o Carcinoma Escamoso Invasivo (SCC), onde as células neoplásicas romperam a membrana basal epitelial.  
> A triagem manual de lâminas microscópicas é um trabalho minucioso e exaustivo: citotécnicos analisam centenas de milhares de células por lâmina, sofrendo com severa fadiga ocular e variabilidade diagnóstica. O objetivo dos autores foi investigar se os Vision Transformers poderiam automatizar essa triagem com alta fidelidade."*

---

### [14:00 - 15:15] Slide 12: Dataset CRIC e Blindagem Anti-Leakage por Paciente
> **Slide Exibido:** *Dataset CRIC e Blindagem Anti-Leakage por Paciente*

**Fala Exata do Aluno 2:**
> *"Os experimentos foram fundamentados sobre a base pública CRIC, desenvolvida pelo Centro de Reconhecimento e Inspeção de Células da Universidade Federal de Ouro Preto (UFOP). A base é composta por 400 imagens de campos microscópicos contendo 11.534 núcleos de células anotados e recortados.  
> Quero aqui enfatizar o padrão-ouro metodológico adotado no Artigo 2: o particionamento entre treino, validação e teste foi realizado estritamente pelo código identificador de cada paciente — 64% das pacientes para treino, 20% para validação e 16% para o teste independente.  
> Isso significa que nenhuma paciente teve células presentes simultaneamente no treino e no teste. Na citopatologia, essa blindagem é mandatória: cada lâmina possui variações únicas de pH, tempo de exposição ao corante de hematoxilina e espessura do esfregaço. Se o particionamento fosse aleatório no nível de células, a rede memorizaria o tom de fundo da lâmina de determinada paciente, gerando uma acurácia fictícia.  
> Notem também na tabela o desbalanceamento brutal da rotina laboratorial: havia mais de 6.700 células normais contra apenas 161 células de carcinoma invasivo em toda a base!"*

---

### [15:15 - 16:30] Slide 13: Estratégia Híbrida de Balanceamento de Dados
> **Slide Exibido:** *Estratégia Híbrida de Balanceamento de Dados*

**Fala Exata do Aluno 2:**
> *"Para impedir que o Transformer colapsasse prevendo apenas a classe majoritária NFIL, os autores formularam uma estratégia híbrida de balanceamento, fixando exatamente 1.000 amostras por classe no conjunto de treinamento, totalizando 6.000 imagens balanceadas.  
> Para as classes minoritárias — em especial o carcinoma SCC, que contava com apenas 103 amostras originais no treino —, aplicou-se oversampling através da biblioteca Albumentations. Utilizaram-se transformações afins que preservam a integridade morfológica da célula: rotações angulares aleatórias, reflexões horizontais e verticais e discretos ajustes de escala.  
> Por outro lado, para as classes abundantes como NFIL, aplicou-se undersampling aleatório, reduzindo de mais de 4.300 para exatamente 1.000 imagens.  
> É fundamental destacar: os subconjuntos de validação e teste permaneceram completamente intactos em suas distribuições naturais da clínica, garantindo uma avaliação de teste justa e desprovida de dados sintéticos."*

---

### [16:30 - 17:45] Slide 14: Fundamentos dos Vision Transformers (ViT)
> **Slide Exibido:** *Fundamentos dos Vision Transformers (ViT)*

**Fala Exata do Aluno 2:**
> *"Entrando no mecanismo do Vision Transformer, formulado por Dosovitskiy em 2020: enquanto a convolução do Artigo 1 opera deslizando filtros locais sobre tensores 2D, o ViT descarta matrizes bidimensionais e processa a imagem como uma sequência unidimensional de tokens, transpondo o mecanismo dos Transformers de NLP para a visão computacional.  
> A imagem celular de 224 por 224 pixels é particionada em uma grade de 196 patches de 16 por 16 pixels.  
> Cada patch passa por uma projeção para gerar um vetor de dimensão D. Ao início dessa sequência, concatena-se o token especial [CLS], responsável por agregar a informação diagnóstica final, e soma-se um vetor de Positional Embeddings 1D para que o modelo tenha noção da ordem espacial dos patches.  
> A sequência passa por 12 blocos de codificador com camadas de Normalização, Feed-Forward e o mecanismo de Autoatenção Multi-Head. A complexidade do ViT é quadrática: para 196 patches, o modelo calcula 196 vezes 196 — ou seja, mais de 38 mil correlações contextuais de autoatenção por cabeça em cada camada!"*

---

### [17:45 - 19:00] Slide 15: Projeção Linear vs. Projeção Convolucional
> **Slide Exibido:** *Projeção Linear vs. Projeção Convolucional*

**Fala Exata do Aluno 2:**
> *"Um dos pontos mais ricos do Artigo 2 foi a investigação sobre a camada de entrada do Transformer: a comparação entre Projeção Linear pura e Projeção Convolucional.  
> Na Projeção Linear original do ViT, os 768 pixels de cada patch de 16 por 16 são vetorizados e multiplicados diretamente por uma matriz densa linear E. Sob essa abordagem, o modelo não possui qualquer premissa sobre vizinhança geométrica interna do patch.  
> Como alternativa, os autores avaliaram a Projeção Convolucional, onde se aplica uma camada Conv2D com kernel 16 por 16, stride de 16 pixels e D canais de saída.  
> Qual a relevância dessa convolução inicial? Ela atua como um extrator contínuo suave de bordas e gradientes celulares locais antes de enviar os vetores para o codificador de atenção.  
> Como veremos nos resultados da Tabela 2, a projeção convolucional superou a projeção linear pura em absolutamente todas as configurações testadas, com saltos de até 11% na acurácia!"*

---

### [19:00 - 20:30] Slide 16: A Hipótese Central: As 5 Técnicas Dinâmicas
> **Slide Exibido:** *As 5 Técnicas de Extração Dinâmica de Patches*

**Fala Exata do Aluno 2:**
> *"Chegamos à grande hipótese de pesquisa formulada por Giovanini e Machado:  
> Nos recortes da base CRIC, o núcleo da célula ocupa comumente apenas a área central de 90 por 90 pixels, enquanto o restante da imagem é composto por citoplasma homogêneo ou pelo fundo branco vazio da lâmina microscópica.  
> A hipótese formulada foi: 'Por que desperdiçar patches de 16 por 16 e computação quadrática de autoatenção em áreas vazias de lâmina? Se concentrarmos os 196 patches dinamicamente sobre a célula, o ViT aumentará seu poder discriminativo?'  
> Os autores desenharam cinco técnicas dinâmicas de extração:  
> 1. Seleção Randômica (SR): centros sorteados de forma uniformemente aleatória.  
> 2. Randômica Aprimorada (RA): sorteio com restrição de distância euclidiana mínima entre centros, reduzindo sobreposições idênticas.  
> 3. Segmentação GrabCut (SS): o algoritmo GrabCut extrai uma máscara binária da célula e os patches são centrados estritamente na célula ativa. Implementou-se um fallback inteligente: se a máscara ocupar menos de 10% da imagem, reverte-se para o grid regular para evitar colapso.  
> 4. Zigue-Zague (ZZ): varredura diagonal contínua cobrindo a região nuclear.  
> 5. Espiral (ES): amostragem concêntrica que parte do centro do núcleo e expande em órbitas crescentes para a periferia."*

---

### [20:30 - 21:45] Slide 17: Infraestrutura de Hardware e Descongelamento Seletivo
> **Slide Exibido:** *Infraestrutura Computacional e Descongelamento*

**Fala Exata do Aluno 2:**
> *"O treinamento de Vision Transformers impôs custos de hardware muito superiores aos da CNN do Artigo 1.  
> Os autores trabalharam em dois ambientes: localmente em uma estação com GPU RTX 2060 de 6 GB de VRAM para processar o ViT-Tiny e ViT-Small; e em nuvem através do Google Colab PRO com GPU Tesla T4 de 15 GB para comportar o ViT-Base com seus 86 milhões de parâmetros.  
> Todos os modelos foram inicializados com pesos pré-treinados na ImageNet-21k, com taxa de aprendizado de 1e-5 sob o otimizador Adam.  
> No ViT-Small, com 22 milhões de parâmetros, os autores adotaram um descongelamento seletivo elegante: descongelaram as 2 primeiras camadas do codificador para ajustar filtros de textura à citologia e as 3 últimas camadas para calibrar a classificação das 6 classes Bethesda, mantendo o meio congelado.  
> Já no ViT-Base, devido ao limite de memória da GPU T4, apenas o último bloco MLP pôde ser descongelado, gerando um severo subajuste decorrente da restrição de recursos."*

---

### [21:45 - 23:00] Slide 18: Resultados (Tabela 2) e o Paradoxo do Grid
> **Slide Exibido:** *Resultados (Tabela 2) e o 'Paradoxo do Grid'*

**Fala Exata do Aluno 2:**
> *"Apresento agora os resultados consolidados na Tabela 2 do artigo, revelando o que chamamos de 'Paradoxo do Grid'.  
> O resultado mais marcante foi: o modelo ViT-Small baseline convencional — utilizando a grade estática uniforme de 14 por 14 patches com projeção convolucional, sem nenhuma modificação dinâmica — alcançou 79% de acurácia no teste e 81% na validação, superando todas as cinco abordagens dinâmicas formuladas!  
> Dentre as abordagens dinâmicas, a extração em Espiral com projeção Conv2D foi a melhor colocada com 78%, seguida pela Randômica Aprimorada com 77% e pelo GrabCut com 76%. Além disso, a Projeção Convolucional superou a Projeção Linear pura em todas as configurações, com ganhos entre 5% e 11%.  
> Por que uma proposta teoricamente tão intuitiva perdeu para a grade estática convencional?"*

---

### Frase de Transição Formal (Aluno 2 ➔ Aluno 3):
> **[Aluno 2 olhando para a câmera e dirigindo-se ao colega]:**  
> *"Para responder a essa questão fundamental, desvendar as causas matemáticas do Paradoxo do Grid e conduzir a análise comparativa aprofundada entre os dois artigos, passo a palavra ao colega [Nome do Aluno 3]."*

---

## 4. Bloco 3: Análise Comparativa e Discussão Crítica
**Orador:** Integrante 3 (Aluno 3)  
**Tempo Total:** 23:00 a 34:30 (11 minutos e 30 segundos)  
**Slides:** 19 ao 26

---

### [23:00 - 24:30] Slide 19: Análise de Causa-Raiz: Por Que o Grid Venceu?
> **Slide Exibido:** *Análise de Causa-Raiz: Por Que o Grid Venceu?*

**Fala Exata do Aluno 3:**
> *"Muito obrigado, [Aluno 2]. Cumprimento o Professor José Denes e todos os colegas.  
> Assumo o terceiro bloco com uma reflexão epistemológica: o trabalho de Giovanini e Machado é um exemplo clássico e valiosíssimo de 'resultado negativo na ciência', onde uma hipótese intuitivamente atraente é refutada pelo método experimental.  
> Por que os métodos dinâmicos falharam frente ao grid regular? Nossa desconstrução analítica identificou três causas-raiz interligadas:  
> Primeira: Super-Aglomeração Espacial (Over-Clustering). Ao forçar a extração de 196 patches de 16 por 16 pixels dentro de uma região nuclear de 90 por 90, os patches sobrepuseram-se em mais de 80%. Em vez de prover mais informação, múltiplos patches capturavam o mesmo grupo de pixels. Os vetores de Consulta (Q) e Chave (K) da autoatenção tornaram-se quase idênticos, colapsando as matrizes de atenção em pura redundância.  
> Segunda: Ruptura dos Positional Embeddings pré-treinados. O ViT foi pré-treinado na ImageNet para entender coordenadas em uma grade cartesiana 14 por 14. Quando alteramos os centros dos patches para uma espiral ou sorteio aleatório mantendo os mesmos índices 1D, destruímos o mapa espacial pré-treinado.  
> E terceira: a Biologia Celular do Sistema Bethesda. Patologistas diferenciam lesões de alto e baixo grau avaliando a relação núcleo-citoplasma. Ao concentrar todos os patches no núcleo, o modelo ficou cego quanto à extensão e formato do citoplasma periférico, contexto que a grade convencional preserva perfeitamente."*

---

### [24:30 - 26:00] Slide 20: Duelo Teórico: Viés Indutivo vs. Fome de Dados (Data-Hunger)
> **Slide Exibido:** *Duelo Teórico: Viés Indutivo vs. Fome de Dados*

**Fala Exata do Aluno 3:**
> *"Ao confrontarmos os dois artigos, deparamo-nos com o grande duelo conceitual da Visão Computacional contemporânea: Viés Indutivo versus Autoatenção Global e Fome de Dados.  
> A convolução do Artigo 1 possui operadores matemáticos rígidos: ela assume localidade espacial — pixels vizinhos compartilham semântica — e equivariância à translação — um tumor é identificado com os mesmos filtros em qualquer hemisfério do cérebro. Graças a isso, a CNN da UFCSPA precisou de apenas 5.500 fatias para convergir para 99% de acurácia treinando do zero.  
> Em contrapartida, o Vision Transformer do Artigo 2 não assume absolutamente nada a priori sobre o espaço 2D. Ele enxerga os patches como uma lista desordenada e precisa aprender as leis da visão por força bruta de retropropagação. Por isso, os Transformers sofrem do fenômeno de Fome de Dados (Data-Hunger).  
> Quando confrontamos o ViT com o estado da arte na base CRIC — alcançado por Diniz et al. em 2021 através de um Ensemble de CNNs clássicas que atingiu 95% de acurácia —, vemos que o ViT estagnou em 79%. O pré-treinamento na ImageNet com carros e animais transfere pouca semântica útil para cromatinas microscópicas, provando que em bases médicas de pequeno porte, o viés indutivo da convolução ainda é insubstituível."*

---

### [26:00 - 27:45] Slide 21: Matriz Comparativa Sistemática (16 Dimensões)
> **Slide Exibido:** *Matriz Comparativa Sistemática: Artigo 1 vs. Artigo 2*

**Fala Exata do Aluno 3:**
> *"Esta matriz comparativa consolida sistematicamente a desconstrução técnica de ambos os trabalhos sob 16 dimensões analíticas fundamentais de engenharia de visão computacional.  
> No Artigo 1, vemos um projeto cirúrgico de parcimônia: uma CNN customizada extremamente enxuta, treinada do zero em imagens compactas de 64 por 64 pixels, que alcançou 99% de acurácia global com custo computacional mínimo e alta transparência via Grad-CAM.  
> No Artigo 2, temos uma incursão investigativa na fronteira dos Transformers, trabalhando em 224 por 224 com modelos de dezenas de milhões de parâmetros, fine-tuning na ImageNet-21k e GPUs de grande porte como a Tesla T4, alcançando 79% no teste independente.  
> Dois domínios de saúde pública de altíssima relevância nacional — neuro-oncologia e saúde da mulher —, abordados por duas escolas metodológicas distintas com trade-offs de engenharia claramente opostos."*

---

### [27:45 - 29:15] Slide 22: Auditoria de Protocolos: Slice Leakage vs. Patient Split
> **Slide Exibido:** *Auditoria de Protocolos: Slice Leakage vs. Patient Split*

**Fala Exata do Aluno 3:**
> *"Exercendo nossa capacidade de avaliação crítica independente, devemos auditar a integridade metodológica de validação de ambos os trabalhos.  
> O Artigo 2 recebe nota máxima no protocolo de particionamento: a divisão estrita por paciente elimina o risco de memorização de artefatos de lâmina. Seus 79% de acurácia refletem uma capacidade de generalização autêntica para novos indivíduos clínicos.  
> Já no Artigo 1, embora os 99% de acurácia sejam formidáveis, apontamos uma vulnerabilidade latente em datasets públicos de ressonância 2D: o risco de slice leakage. Caso fatias axiais contíguas do mesmo crânio tenham sido distribuídas entre treino e teste, o modelo pode ter se beneficiado de redundância visual entre fatias.  
> Os autores da UFCSPA contornaram parcialmente essa desconfiança de forma elegante ao demonstrar que os mapas Grad-CAM mantiveram a ativação centrada na massa tumoral em uma base externa completamente inédita de outro hospital. Contudo, para futuros trabalhos clínicos, a divisão por volume tridimensional de paciente é mandatória."*

---

### [29:15 - 30:45] Slide 23: Árvore de Decisão: Quando Usar CNN ou ViT na Saúde?
> **Slide Exibido:** *Árvore de Decisão: Quando Usar CNN ou ViT na Saúde?*

**Fala Exata do Aluno 3:**
> *"Como futuros bacharéis em Sistemas de Informação, sintetizamos as lições dos dois artigos em uma árvore de decisão prescritiva de engenharia para projetos biomédicos:  
> Se o projeto possui menos de 10 mil exames anotados e opera sob infraestrutura de hardware restrita — como em postos de saúde ou hospitais regionais —, a escolha mandatória deve ser uma Rede Neural Convolucional especializada e fortemente regularizada, assim como fez a UFCSPA. Ela é barata, eficiente, possui inferência instantânea e viés indutivo adequado.  
> Vision Transformers só devem ser adotados quando houver dezenas ou centenas de milhares de imagens — como na análise de lâminas inteiras em Whole Slide Imaging —, e mesmo assim, a recomendação categórica é manter a extração em Grid Regular uniforme associada à projeção convolucional Conv2D, evitando a fragmentação dinâmica descontrolada de patches."*

---

### [30:45 - 32:00] Slide 24: O Valor Epistemológico do Resultado Negativo
> **Slide Exibido:** *O Valor Epistemológico do Resultado Negativo*

**Fala Exata do Aluno 3:**
> *"Queremos destacar o imenso valor epistemológico do 'resultado negativo' trazido pelo Artigo 2.  
> Na academia e na indústria de aprendizado de máquina, existe um vício crônico de publicação (publication bias): artigos só são aceitos quando quebram recordes de acurácia com números inflados.  
> A publicação de Giovanini e Machado nos anais da SBC é um ato de maturidade e rigor científico: formularam uma hipótese plausível, projetaram 5 métodos, executaram testes cegos e provaram matematicamente por que a amostragem dinâmica degrada a autoatenção. Isso economiza centenas de horas de GPU para a comunidade científica internacional.  
> Sintetizamos três lições eternas:  
> 1. Curadoria de dados supera hiperparâmetros (como provou a higienização do Figshare no Artigo 1).  
> 2. O hype dos Transformers não anula a convolução em pequenos volumes de dados.  
> 3. A abordagem híbrida — unindo convolução local e atenção global — é o futuro da disciplina."*

---

### [32:00 - 33:30] Slide 25: Conclusões Finais e Perspectivas Futuras
> **Slide Exibido:** *Conclusões Finais e Perspectivas Futuras*

**Fala Exata do Aluno 3:**
> *"Concluímos nosso estudo com uma síntese clara:  
> O Artigo 1 validou a eficácia da simplicidade e da parcimônia convolucional em ressonância magnética, garantindo 100% de sensibilidade no diagnóstico do glioma e explicabilidade sólida via Grad-CAM.  
> O Artigo 2 descortinou as limitações dos Vision Transformers em datasets celulares modestos, demonstrando a superioridade da grade uniforme e o papel redentor da projeção convolucional.  
> Para o futuro da citopatologia digital, propomos três direções de pesquisa:  
> 1. Adotar arquiteturas hierárquicas como o Swin Transformer, que calcula atenção em janelas locais deslocadas, unindo o viés de localidade com a autoatenção.  
> 2. Modelar embeddings posicionais radiais contínuos baseados na distância euclidiana até o núcleo para geometrias em espiral.  
> 3. Explorar modelos generativos de difusão para sintetizar carcinomas invasivos raros, saciando a fome de dados dos transformadores em bases médicas balanceadas."*

---

### [33:30 - 34:30] Slide 26: Referências Bibliográficas e Agradecimentos
> **Slide Exibido:** *Muito Obrigado pela Atenção! — Encerramento Regulamentar*

**Fala Exata do Aluno 3:**
> *"Registramos na tela as referências bibliográficas primárias da SBC e os marcos teóricos de Dosovitskiy, Chollet, Selvaraju e Diniz et al. que subsidiaram nosso trabalho.  
> Agradecemos imensamente a atenção do Professor Doutor José Denes Lima Araújo e de todos os nossos colegas de turma.  
> Encerramos nossa explanação rigorosamente dentro do prazo regulamentar, aos 34 minutos e 30 segundos, em pleno cumprimento do edital e preservando o tempo reservado para a arguição técnica.  
> Todo o trio está a postos e à inteira disposição para as perguntas e considerações da banca examinadora. Muito obrigado!"*

---

## 5. Bloco 4: Estratégia de Arguição da Banca (34:30 a 40:00)

### Protocolo de Distribuição de Perguntas no Trio
Para garantir nota máxima no critério *"Participação, postura e envolvimento"* (1,0 pt) e demonstrar união técnica:
1. **Perguntas sobre o Artigo 1 (UFCSPA / CNN / MRI / Grad-CAM / K-Fold):**  
   - Resposta prioritária: **Integrante 1 (Aluno 1)**.  
   - Complemento voluntário: Integrante 3 (conectando com o viés indutivo) ou Integrante 2.
2. **Perguntas sobre o Artigo 2 (PUC Minas / UFMG / ViT / Citologia / GrabCut / Bethesda):**  
   - Resposta prioritária: **Integrante 2 (Aluno 2)**.  
   - Complemento voluntário: Integrante 3 (detalhando a sobreposição dos patches) ou Integrante 1.
3. **Perguntas Conceituais de Confronto (Viés Indutivo, Data-Hunger, Leakage, Arquiteturas Futuras):**  
   - Resposta prioritária: **Integrante 3 (Aluno 3)**.  
   - Apoio técnico imediato: Integrante 1 e Integrante 2.

### Recomendações de Postura em Câmera
- Mantenha a câmera ligada durante todos os 40 minutos de sessão, mesmo enquanto o colega estiver falando.
- Olhe diretamente para a lente da câmera durante sua fala, mantendo tom acadêmico seguro e postura ereta.
- Durante a fala dos outros membros, balance a cabeça sutilmente em concordância, demonstrando domínio integrado do conteúdo.
- Ao responder uma pergunta do professor, inicie com civilidade acadêmica: *"Excelente colocação, Professor Denes..."*, formule a resposta técnica em até 90 segundos e conclua com firmeza.
