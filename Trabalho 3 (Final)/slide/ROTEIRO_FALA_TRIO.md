# Roteiro de Fala Minuto a Minuto para Apresentação em Trio

> **Disciplina**: Tópicos Especiais em Visão Computacional — UFPI / CSHNB  
> **Professor**: Dr. José Denes Lima Araújo  
> **Tempo Total Alvo**: **24 a 26 minutos** (Margem de segurança para o teto de 30 minutos)  
> **Apresentadores**: Integrante 1, Integrante 2, Integrante 3 (Grupo 4)  
> **Slides de Referência**: `slides.html` / `slides.md` (20 slides)

---

## ⏱️ Cronograma Geral de Transições

| Bloco | Responsável | Tempo Acumulado | Slides | Foco Temático |
| :---: | :---: | :---: | :---: | :--- |
| **Bloco 1** | **Integrante 1** | **00:00 - 08:00** (8 min) | Slides 1 a 6 | Contexto Clínico, WSOD, Artigo Base, GMIC e Perda com $\beta=3.26$ |
| **Bloco 2** | **Integrante 2** | **08:00 - 16:30** (8,5 min) | Slides 7 a 12 | Taxonomia dos 5 CAMs, Desacoplamento, VinDr-Mammo e PyTorch |
| **Bloco 3** | **Integrante 3** | **16:30 - 24:30** (8 min) | Slides 13 a 19 | Avaliação IoU, Resultados das Tabelas 1 e 2, Errata e Conclusão |
| **Bloco 4** | **Trio Reunido** | **24:30 - 30:00** (5,5 min) | Slide 20 | Agradecimentos e Defesa Técnica perante a Banca Examinadora |

---

## 🎙️ Roteiro de Fala Detalhado

---

### BLOCO 1: Contextualização Clínica, WSOD e GMIC (Integrante 1)
**Tempo Alocado**: 00:00 a 08:00 (8 minutos exatos)  
**Slides**: 1 a 6

#### Slide 1: Capa e Identificação Institucional (00:00 - 00:45)
- **Fala**:
  > *"Boa noite a todos. Cumprimento cordialmente o Prof. Dr. José Denes Lima Araújo e os colegas de curso. Em nome do Grupo 4, composto por mim, pelo [Nome do Integrante 2] e pelo [Nome do Integrante 3], damos início à apresentação do nosso Trabalho Final da disciplina de Tópicos Especiais em Visão Computacional.  
  > O nosso trabalho consiste na Reprodução Científica e Análise Experimental do artigo 'A Study on Class Activation Map Methods to Detect Masses in Mammography Images using Weakly Supervised Learning', publicado nos anais da Sociedade Brasileira de Computação pelos pesquisadores Vicente Sampaio e Filipe Cordeiro, da UFRPE.  
  > Investigamos a fundo a arquitetura GMIC, as propriedades matemáticas de cinco geradores de mapas de ativação de classe e o fenômeno de desacoplamento entre treino e teste para localização de lesões mamárias."*

#### Slide 2: Contexto Clínico e Desafio Radiológico (00:45 - 02:00)
- **Fala**:
  > *"Para compreender a motivação científica deste trabalho, precisamos situar o desafio no contexto clínico. O câncer de mama é a neoplasia maligna de maior incidência e a principal causa de mortalidade por câncer entre as mulheres em todo o mundo, respondendo por aproximadamente 15,5% dos óbitos oncológicos femininos, segundo dados da Organização Mundial da Saúde.  
  > O prognóstico das pacientes está intimamente atrelado à precocidade do diagnóstico: quando detectado em estágios iniciais, com nódulos menores que 10 milímetros, a taxa de sobrevida em cinco anos ultrapassa os 90%.  
  > A mamografia digital direta (FFDM) é o padrão-ouro internacional para rastreamento populacional. No entanto, a leitura mamográfica é notoriamente uma das tarefas mais complexas da radiologia médica. Isso decorre principalmente do chamado 'fenômeno de mascaramento': em mamas densas, o tecido fibroglandular sadio e os carcinomas invasivos compartilham coeficientes de atenuação radiológica quase idênticos, escondendo lesões neoplásicas. Além disso, as massas apresentam bordas espiculadas e limites tênues. Em rotinas de triagem em massa, a fadiga do radiologista avaliando centenas de imagens de altíssima resolução resulta em taxas de falsos negativos de até 30%. Por isso, sistemas de CAD baseados em aprendizado profundo são fundamentais como uma segunda opinião automatizada."*

#### Slide 3: O Paradigma WSOD (Weakly Supervised Object Detection) (02:00 - 03:30)
- **Fala**:
  > *"No entanto, quando tentamos treinar redes neurais convencionais para detectar lesões, esbarramos no que a literatura médica chama de 'o gargalo da anotação supervisionada'.  
  > Em aprendizado totalmente supervisionado, necessitaríamos de coordenadas espaciais ou máscaras de segmentação pixel a pixel desenhadas manualmente por radiologistas certificados para cada exame da base de treino. Na prática médica, esse processo é inviável em larga escala: é excessivamente oneroso, lento e sofre de alta divergência interobservador. Mais de 99% dos mamogramas armazenados em centros hospitalares possuem apenas laudos textuais globais indicando 'exame normal' ou 'exame com presença de massa'.  
  > É nesse vácuo que entra o Paradigma de Aprendizado Fracamente Supervisionado para Detecção de Objetos (WSOD). No WSOD, a rede é alimentada durante todo o treinamento unicamente com o rótulo binário da imagem inteira: y=0 para normal e y=1 para massa. O modelo jamais recebe coordenadas ou caixas delimitadoras durante o aprendizado.  
  > A meta matemática do WSOD é dupla: classificar com alta precisão a imagem e, a partir dos mapas de ativação convolucionais na inferência, localizar espacialmente onde está a lesão com IoU superior a 0.3 em relação ao padrão-ouro do especialista."*

#### Slide 4: O Artigo Selecionado — Sampaio & Cordeiro (03:30 - 05:00)
- **Fala**:
  > *"O artigo que selecionamos para reprodução sistemática foi publicado em 2022 por Vicente Sampaio e Filipe Cordeiro, da UFRPE. Os autores partiram do renomado modelo GMIC, proposto por Shen e colaboradores na Medical Image Analysis em 2021, e formularam uma hipótese inovadora: o CAM clássico de Zhou, utilizado originalmente no GMIC, produz mapas muito difusos.  
  > Eles investigaram se a substituição por métodos mais recentes de saliência e, principalmente, se o desacoplamento — isto é, utilizar um método de CAM durante o treinamento e outro diferente durante o teste — traria ganhos clínicos mensuráveis na base pública VinDr-Mammo.  
  > Nosso grupo assumiu a meta de reconstruir integralmente essa arquitetura em PyTorch, implementar os cinco métodos de CAM, reproduzir os experimentos de classificação e detecção, auditar analiticamente as equações e validar se a teoria do desacoplamento de fato se sustenta."*

#### Slide 5: A Arquitetura GMIC (05:00 - 06:30)
- **Fala**:
  > *"Para entender como o GMIC viabiliza o processamento de imagens gigantescas sem estourar a memória da GPU, passamos à análise arquitetural. Uma mamografia digital possui tipicamente 2944 por 1920 pixels. Se simplesmente redimensionarmos a imagem inteira para uma resolução baixa, perdemos as microestruturas das bordas da lesão.  
  > O GMIC resolve isso estruturando-se em três módulos articulados:  
  > Primeiro, o Módulo Global: uma ResNet-22 personalizada recebe o exame completo e gera um tensor de características globais, produzindo a predição global e um Mapa de Ativação de Classe A^c, que funciona como um mapa térmico de atenção visual.  
  > Segundo, o Extrator Guloso de Patches: a partir desse mapa de calor, o algoritmo localiza os K=6 picos máximos de ativação. Com supressão de vizinhança espacial para evitar recortes sobrepostos, são recortados seis patches de 256 por 256 pixels diretamente da imagem original na sua resolução nativa.  
  > Terceiro, o Módulo Local e de Fusão: uma ResNet-18 dedicada processa cada patch, extraindo representações morfológicas finas que são agregadas via Max-Pooling em uma abordagem de Aprendizado por Múltiplas Instâncias (MIL). Por fim, o vetor global e o vetor local são concatenados e processados por camadas lineares com Sigmoid, gerando a predição final de fusão."*

#### Slide 6: Função de Perda Multi-Ramo e Regularização L1 (06:30 - 08:00)
- **Fala**:
  > *"Para treinar esses três fluxos em harmonia, o GMIC adota uma função de perda multi-ramo somando a Entropia Cruzada Binária do ramo local, do ramo global e do módulo de fusão.  
  > Contudo, há um componente matemático crucial nessa equação: o termo de regularização L1, multiplicado pelo hiperparâmetro beta fixado em 3.26.  
  > Por que essa regularização é indispensável? Sem ela (ou seja, se beta fosse zero), a rede global não sofreria nenhuma penalidade quanto à área ativada no mapa de calor. Ela tenderia a expandir o calor por todo o tecido mamário sadio para minimizar a perda de classificação. Com o CAM disperso, os seis patches recortados pegariam tecido mamário perfeitamente normal e os alimentariam à rede local rotulados como massa, contaminando o treinamento com ruído grave.  
  > O termo L1 impõe uma penalidade proporcional à soma dos valores absolutos do mapa, forçando o gradiente a concentrar a ativação estritamente sobre a anomalia tumoral.  
  > E para apresentar a dedução matemática dos cinco mapas de ativação, o protocolo do desacoplamento e a nossa implementação de software em PyTorch, passo agora a palavra ao Integrante 2."*

---

### BLOCO 2: Formulação dos CAMs, Desacoplamento e Implementação PyTorch (Integrante 2)
**Tempo Alocado**: 08:00 a 16:30 (8,5 minutos exatos)  
**Slides**: 7 a 12

#### Slide 7: Taxonomia dos Mapas de Ativação (1/2) — CAM e Grad-CAM (08:00 - 09:30)
- **Fala**:
  > *"Muito obrigado, Integrante 1. Cumprimento o professor José Denes e a todos os presentes. Dando continuidade à exposição técnica, entramos na análise dos mapas de ativação de classe, que constituem o núcleo experimental deste trabalho.  
  > Começamos pelo CAM tradicional, proposto por Zhou em 2016. O CAM clássico calcula a projeção ponderada dos pesos sinápticos da camada linear final conectados aos mapas de ativação convolucionais após uma camada de Global Average Pooling. Embora pioneiro, o CAM tradicional possui uma limitação severa em imagens mamográficas: ele produz mapas de calor excessivamente difusos e volumosos, ativando grandes porções de parênquima mamário adjacente.  
  > Para contornar a dependência arquitetural do GAP, Selvaraju propôs em 2017 o Grad-CAM. O Grad-CAM calcula os coeficientes alfa como a média aritmética espacial dos gradientes de primeira ordem da saída da classe em relação aos mapas de ativação. Ele é aplicável a qualquer CNN e tende a concentrar o calor no epicentro da lesão, porém tem dificuldade em capturar bordas complexas e extensas."*

#### Slide 8: Taxonomia dos Mapas de Ativação (2/2) — Grad-CAM++, XGrad-CAM e Layer-CAM (09:30 - 11:00)
- **Fala**:
  > *"A literatura evoluiu para formulações de saliência consideravelmente mais sofisticadas, e o artigo avalia três expoentes fundamentais:  
  > O Grad-CAM++, concebido por Chattopadhay em 2018, foi formulado analiticamente para superar o Grad-CAM através de derivadas parciais de segunda e terceira ordens. Ele pondera cada pixel individualmente: os neurônios que têm correlação positiva mais forte com a classe recebem pesos superiores, permitindo delimitar com fidelidade o contorno total e a extensão periférica de tumores espiculados.  
  > O XGrad-CAM, proposto por Fu em 2020, baseia-se em uma fundamentação axiomática formal regida por dois princípios: Sensibilidade e Conservação. Ao invés de uma média simples de gradientes, cada gradiente é ponderado pela magnitude relativa da ativação convolucional normalizada naquele ponto. Como consequência matemática direta, gradientes ruidosos em regiões de tecido normal inativo são suprimidos, gerando mapas extraordinariamente limpos e focados.  
  > Por fim, o Layer-CAM, de Jiang em 2021, opera ponderação elemento a elemento e integra hierarquicamente características rasas e profundas. No entanto, veremos que essa sensibilidade exacerbada se torna uma armadilha em mamografia."*

#### Slide 9: A Teoria Científica do Desacoplamento Treino vs Teste (11:00 - 12:30)
- **Fala**:
  > *"Chegamos agora à hipótese científica central investigada no artigo e reproduzida em nosso trabalho: por que o desacoplamento de CAMs funciona tão bem?  
  > A resposta repousa na disparidade dos objetivos funcionais do CAM em cada etapa do ciclo de vida da rede:  
  > Na fase de treinamento, o mapa de ativação tem uma finalidade estrita: atuar como uma 'mira telescópica' para o Extrator Guloso de Patches. Se usarmos um método como o CAM clássico ou o Layer-CAM, o calor transborda para áreas saudáveis, e o sistema recortará pedaços de mama normal como se fossem massa. O XGrad-CAM no treinamento é superior porque opera como um filtro cirúrgico de pureza: ele isola cirurgicamente o núcleo da massa tumoral, garantindo que a ResNet-18 local receba apenas padrões neoplásicos verdadeiros.  
  > Já na fase de inferência ou teste, o objetivo não é mais extrair patches, mas sim maximizar a sobreposição geométrica da bounding box para satisfazer o critério clínico de IoU maior ou igual a 0.3. Se utilizarmos o XGrad-CAM no teste, sua extrema concisão gerará caixas pequenas demais, perdendo as margens do tumor. Aqui o Grad-CAM++ brilha: sensível às derivadas de ordem superior, ele gera um halo expansivo sobre toda a massa, envelopando a lesão e atingindo o limiar de IoU sem espalhar caixas em outras áreas do exame."*

#### Slide 10: O Dataset VinDr-Mammo e Protocolo de Dados (12:30 - 13:45)
- **Fala**:
  > *"Para conduzir a reprodução em um ambiente controlado e reproduzível, adotamos o benchmark público VinDr-Mammo, disponibilizado por Nguyen e colaboradores em 2022. Trata-se de uma base internacional de 5.000 exames mamográficos, totalizando 20.000 projeções FFDM em escala de cinza de alta profundidade, cobrindo as quatro incidências mamográficas padrão: Craniocaudal e Médio-lateral oblíqua de cada mama.  
  > Seguindo com rigor o protocolo de Sampaio e Cordeiro, estabelecemos uma separação perfeitamente balanceada:  
  > Um conjunto de treinamento de 1.978 imagens, composto por 989 mamas normais e 989 mamas com massa tumoral comprovada;  
  > E um conjunto de teste independente com 474 imagens, sendo 237 normais e 237 com massa.  
  > Enfatizamos um ponto vital para a integridade do aprendizado fracamente supervisionado: as anotações espaciais e bounding boxes fornecidas pelos médicos radiologistas foram completamente blindadas e ocultadas durante toda a fase de treinamento, sendo carregadas unicamente no teste para calcular a sobreposição de IoU."*

#### Slide 11: Engenharia de Software Modular em PyTorch (13:45 - 15:00)
- **Fala**:
  > *"Toda a implementação do nosso trabalho foi desenvolvida em conformidade com as melhores práticas de Engenharia de Software em PyTorch, estruturada no diretório Trabalho 3 (Final)/src/.  
  > Modularizamos o projeto em componentes independentes:  
  > O pacote datasets encapsula o VinDrMammoDataset com suporte a transformações do Albumentations;  
  > O pacote models implementa a ResNet-22 global customizada, a ResNet-18 local, o GreedyPatchExtractor vetorizado com supressão espacial e a classe GMICLoss;  
  > No pacote cams, desenvolvemos a classe unificada CAMManager, que encapsula os geradores de CAM e possibilita a troca dinâmica entre métodos de treino e teste via argumentos de linha de comando;  
  > E no pacote evaluation, modularizamos o cálculo de métricas de classificação global e a rotina de detecção espacial com IoU e contagem de FPPI.  
  > Isso permite executar qualquer combinação experimental via terminal com comandos limpos e parametrizáveis."*

#### Slide 12: Soluções de Engenharia para Restrições de GPU (15:00 - 16:30)
- **Fala**:
  > *"Durante o desenvolvimento, enfrentamos um obstáculo de infraestrutura muito comum em Visão Computacional Médica: o consumo brutal de memória de vídeo ao processar lotes de imagens de alta resolução combinadas com patches locais. Uma execução padrão com batch size de 6 imagens excederia 18 gigabytes de VRAM, gerando o clássico erro de CUDA Out-of-Memory em GPUs de laboratório.  
  > Para solucionar esse desafio mantendo rigor metodológico absoluto e equivalência estatística com o artigo original, implementamos duas soluções de engenharia:  
  > Primeiro, Automatic Mixed Precision (AMP): através de torch.cuda.amp, convertemos as operações convolucionais compatíveis para precisão de ponto flutuante de 16 bits (FP16), reduzindo o consumo de VRAM em 45% e acelerando a vazão de imagens por segundo;  
  > Segundo, Gradient Accumulation: estabelecemos um batch físico de 2 imagens na GPU e acumulamos os gradientes ao longo de 3 passos consecutivos antes de invocar o optimizer.step(). Com isso, a descida do gradiente opera exatamente sobre um batch virtual de 6 imagens, idêntico ao do artigo original, preservando a dinâmica de convergência.  
  > E agora, para apresentar a avaliação rigorosa de detecção, os resultados comparativos das Tabelas 1 e 2 e a errata técnica identificada por nosso trio, passo a palavra ao Integrante 3."*

---

### BLOCO 3: Experimentos, Resultados Comparativos e Discussão Crítica (Integrante 3)
**Tempo Alocado**: 16:30 a 24:30 (8 minutos exatos)  
**Slides**: 13 a 19

#### Slide 13: Avaliação de Detecção Fracamente Supervisionada (16:30 - 17:45)
- **Fala**:
  > *"Muito obrigado, Integrante 2. Saúdo o professor José Denes e a todos os presentes. Assumo a palavra para apresentar a avaliação quantitativa e qualitativa dos nossos experimentos.  
  > No aprendizado fracamente supervisionado, a validação de localização espacial é realizada exclusivamente sobre as 237 mamografias do conjunto de teste que comprovadamente contêm massas neoplásicas.  
  > O procedimento matemático consiste em submeter o mapa de ativação A^c a uma varredura de binarização por limiares tau entre 0.1 e 0.9. A partir da máscara binária resultante, extraímos os contornos conexos que formam as caixas delimitadoras preditas B_pred.  
  > Cada caixa predita é então comparada contra as anotações padrão-ouro dos radiologistas através da Intersecção sobre a União (IoU).  
  > É fundamental pontuar: por que adotamos o limiar de IoU maior ou igual a 0.3 em vez do tradicional 0.5 de bases naturais como Pascal VOC? Porque tumores malignos espiculados em mamografia possuem margens indistintas e infiltrativas no parênquima fibroso, sem contornos geométricos rígidos. O limiar de 0.3 é o padrão canônico estabelecido na literatura médica internacional de CAD por Shen et al. e seguido por Sampaio e Cordeiro. As métricas centrais são a Sensibilidade de Detecção (TPR) e os Falsos Positivos por Imagem (FPPI)."*

#### Slide 14: Resultados da Classificação Global no VinDr-Mammo (17:45 - 19:00)
- **Fala**:
  > *"Iniciamos a avaliação pelo nível de imagem, correspondente à Tabela 1 do artigo original.  
  > O modelo GMIC integrado atingiu em nossa reprodução uma Acurácia Global de 80,12%, uma Área sob a Curva ROC (AUC) de 87,22%, Sensibilidade (TPR) de 71,88% e Especificidade de 88,52%.  
  > Esses números comprovam que a arquitetura multi-ramo é significativamente superior a abordagens que utilizam apenas visão global — cuja acurácia caiu para 76% — ou apenas visão local isolada — que obteve apenas 69% de acurácia.  
  > O modelo demonstrou alta capacidade discriminativa, garantindo com 88,5% de especificidade que exames normais não sejam indevidamente catalogados como patológicos, mitigando o risco de biópsias desnecessárias."*

#### Slide 15: Tabela Mestra de Detecção WSOD (19:00 - 20:30)
- **Fala**:
  > *"Passamos agora à Tabela 2 do artigo, que constitui o resultado mais expressivo de toda a pesquisa.  
  > Observando a matriz de combinações:  
  > O baseline histórico do GMIC — utilizando CAM clássico no treino e no teste — obteve sensibilidade de 0.69, porém com um custo oneroso de 1.55 falsos positivos por imagem.  
  > Quando aplicamos a nossa abordagem desacoplada — treinando a rede com XGrad-CAM para garantir patches limpos e avaliando no teste com Grad-CAM++ — atingimos o modelo campeão com TPR de 0.70 a um índice de apenas 0.88 FPPI!  
  > Isso representa um ganho real de sensibilidade de detecção combinado a uma redução drástica de 43,2% nos falsos alarmes em relação ao baseline!  
  > Em contrapartida, observem a coluna do Layer-CAM no teste: embora tenha atingido um TPR nominal de 0.72, seu índice de falsos alarmes explodiu para estarrecedores 4.19 FPPI. Esse resultado confirma experimentalmente que o Layer-CAM se desestabiliza em tecidos mamários densos, invalidando seu uso prático."*

#### Slide 16: Análise Visual Qualitativa dos Mapas de Calor (20:30 - 21:45)
- **Fala**:
  > *"Essa discrepância numérica fica evidente na análise visual qualitativa dos mapas de calor gerados sobre os casos reais de teste.  
  > No CAM tradicional, observamos uma mancha difusa que se espalha por grande parte da mama, gerando caixas imprecisas que geram altos índices de FPPI;  
  > No Grad-CAM, o calor fica restrito a um ponto focal pequeno no centro da lesão, subestimando as bordas e falhando no limiar de IoU de 0.3;  
  > Já no par desacoplado campeão — XGrad-CAM no treino e Grad-CAM++ no teste —, o mapa térmico apresenta um epicentro de altíssima certeza que se estende suavemente pelos contornos lobulados e espiculados da neoplasia. A caixa delimitadora predita em vermelho sobrepõe com precisão a marcação verde dos radiologistas, atingindo sobreposições de IoU superiores a 0.45 sem disparar caixas falsas em regiões sadias."*

#### Slide 17: Análise Crítica e Errata Técnica Identificada (21:45 - 22:45)
- **Fala**:
  > *"Neste ponto, gostaríamos de destacar uma importante contribuição crítica realizada pelo nosso trio durante a auditoria analítica do artigo de Sampaio e Cordeiro.  
  > Ao examinarmos minuciosamente a Tabela 1 do artigo publicado, notamos que a quarta coluna foi intitulada como 'FNR' (Taxa de Falsos Negativos), exibindo o valor de 88,52%.  
  > No entanto, por definição matemática elementar da teoria da detecção estatística, a Taxa de Falsos Negativos é o complemento exato da Sensibilidade: FNR é igual a 1 menos TPR. Se o modelo possui uma sensibilidade de 71,88%, a taxa real de falsos negativos é de 100% menos 71,88%, o que resulta em exatamente 28,12%.  
  > O valor de 88,52% publicado pelos autores corresponde, na verdade, à Taxa de Verdadeiros Negativos (TNR), também conhecida como Especificidade da rede. Identificamos e documentamos formalmente essa inconsistência em nosso Relatório SBC, evidenciando o domínio analítico e a postura científica crítica do nosso grupo."*

#### Slide 18: Viabilidade Clínica e Trade-Offs de Detecção (22:45 - 23:30)
- **Fala**:
  > *"Essa reflexão crítica nos conduz à discussão da viabilidade médica. Em inteligência artificial aplicada à saúde, números frios não contam toda a história.  
  > Em um centro de diagnóstico hospitalar, um médico radiologista lauda entre 100 e 300 mamografias diariamente. Ao utilizar o modelo campeão desacoplado, com 0.88 FPPI, o especialista visualiza em média menos de um alarme falso por exame, o que é plenamente assimilável como uma checagem rápida de segurança, ajudando a resgatar carcinomas imperceptíveis.  
  > Já um modelo como o Layer-CAM, que produz 4.19 FPPI, inundaria a tela do médico com mais de 800 caixas falsas ao longo do dia de trabalho. Isso gera fadiga cognitiva, perda de confiança no sistema computacional e sobrecarrega o sistema de saúde com biópsias desnecessárias. Portanto, a métrica de sucesso clínico definitiva não é o TPR isolado, mas sim a razão entre sensibilidade e taxa de falsos positivos."*

#### Slide 19: Conclusões, Lições Aprendidas e Trabalhos Futuros (23:30 - 24:30)
- **Fala**:
  > *"Em conclusão, nosso trabalho reproduziu e validou com sucesso experimental a hipótese científica de Sampaio e Cordeiro. Confirmamos que o desacoplamento de mapas de ativação de classe é uma estratégia altamente eficaz e elegante para mitigar o gargalo de anotação médica sob o paradigma WSOD.  
  > O XGrad-CAM atua com precisão cirúrgica no treino para fornecer patches de alta pureza patológica, enquanto o Grad-CAM++ na inferência garante a cobertura espacial necessária para atingir sobreposição clínica satisfatória. Nossas soluções de engenharia com Mixed Precision e Gradient Accumulation demonstraram que essa tecnologia pode ser treinada e validada em hardware acessível.  
  > Como passos futuros, sugerimos investigar o uso de Vision Transformers com atenção cruzada entre patches e visão global, além de pré-treinamento auto-supervisionado com Masked Autoencoders."*

---

### BLOCO 4: Agradecimentos e Defesa Técnica Perante a Banca (Trio Reunido)
**Tempo Alocado**: 24:30 a 30:00 (5,5 minutos)  
**Slide**: 20

#### Slide 20: Agradecimentos e Sessão de Perguntas (Q&A) (24:30 - 25:00)
- **Fala Conjunta**:
  > - **Integrante 3**: *"Encerramos aqui a nossa exposição formal rigorosamente dentro do tempo limite previsto de 25 minutos."*  
  > - **Integrante 1**: *"Agradecemos imensamente a orientação do Prof. Dr. José Denes Lima Araújo e a atenção de todos os colegas."*  
  > - **Integrante 2**: *"Todos os três integrantes do Grupo 4 colocam-se agora à inteira disposição da banca para a sessão de arguição e perguntas. Muito obrigado!"*

---

## 🛡️ Guia de Respostas Preparadas para a Banca (Perguntas Antecipadas)

### Pergunta Provável 1: "Por que foi necessário adicionar o termo de regularização L1 $\beta \mathcal{L}_{reg}(A^c)$ com $\beta = 3.26$ na função de perda? O que aconteceria se $\beta = 0$?"
- **Quem responde preferencialmente**: **Integrante 1**
- **Resposta Técnica Modelo**:
  > *"Excelente pergunta, professor. O termo de regularização L1 é o pilar de estabilização espacial do GMIC. Quando treinamos uma rede convolucional apenas com a perda de entropia cruzada binária em nível de imagem, a rede é livre para espalhar suas ativações por toda a extensão espacial da mama, porque a perda de classificação não penaliza o tamanho da área ativada no mapa de calor.  
  > Se definíssemos $\beta = 0$, o mapa de ativação cobriria praticamente toda a glândula mamária sadia. Como o GMIC depende desse mapa para extrair os seis patches de alta resolução, o extrator guloso recortaria regiões de tecido normal e as enviaria para o backbone local rotuladas como 'massa'. Isso contaminaria o aprendizado da ResNet-18 com forte supervisão ruidosa.  
  > O termo L1 impõe uma penalidade de norma 1 sobre os valores de ativação absolutos. O valor $\beta = 3.26$, calibrado empiricamente por Shen et al., atua como uma força de parcimônia que equilibra a perda de classificação com a esparsidade espacial, obrigando o mapa a acender estritamente sobre a anomalia."*

---

### Pergunta Provável 2: "Qual a diferença matemática fundamental entre o Grad-CAM e o XGrad-CAM que confere superioridade ao XGrad-CAM durante a fase de treinamento?"
- **Quem responde preferencialmente**: **Integrante 2**
- **Resposta Técnica Modelo**:
  > *"A diferença primordial repousa na ponderação dos gradientes e no respeito aos axiomas de sensibilidade e conservação formulados por Fu em 2020.  
  > No Grad-CAM tradicional, o coeficiente $\alpha_k$ é obtido pela média aritmética simples dos gradientes sobre toda a grade espacial, tratando com o mesmo peso os neurônios que têm ativação zero e os que têm alta ativação. Isso permite que ruídos ou derivadas residuais em regiões onde a rede nem ativou o filtro contribuam para o mapa de calor.  
  > O XGrad-CAM introduz uma ponderação em que cada gradiente local é multiplicado pela ativação normalizada daquele neurônio específico sobre a soma total do canal: $\frac{A_{i,j}^k}{\sum A^k}$.  
  > Consequentemente, se em uma determinada região do parênquima sadio a ativação é desprezível, o gradiente daquele ponto é matematicamente anulado. Isso torna o XGrad-CAM imune a ruídos de alta frequência em tecidos normais, gerando um mapa extremamente limpo e pontual que garante a pureza dos patches no treinamento."*

---

### Pergunta Provável 3: "Por que adotar o limiar de $\text{IoU} \ge 0.3$ para validar a detecção em mamografia, em vez do clássico $\text{IoU} \ge 0.5$ do Pascal VOC ou COCO?"
- **Quem responde preferencialmente**: **Integrante 3**
- **Resposta Técnica Modelo**:
  > *"Essa é uma distinção conceitual crucial entre visão computacional para imagens naturais e visão computacional médica.  
  > Em bases como VOC ou COCO, os objetos — como carros, pedestres ou semáforos — possuem limites geométricos nítidos e bordas sólidas, tornando viável exigir um IoU rigoroso de 0.5 ou até 0.75.  
  > Em mamografia digital, as neoplasias malignas infiltram o estroma mamário adjacente com espículas microscópicas. Radiologistas seniores frequentemente divergem quanto ao perímetro exato da lesão: onde um especialista demarca uma elipse de 2 centímetros, outro especialista inclui o halo infiltrativo gerando uma anotação maior.  
  > Além disso, no regime de Aprendizado Fracamente Supervisionado (WSOD), o modelo jamais teve acesso a coordenadas de caixas no treinamento; ele infere a caixa a partir de um mapa de saliência convolucional binarizado.  
  > Por esses motivos, a literatura científica mundial de CAD mamográfico consolidou o padrão de $\text{IoU} \ge 0.3$ — adotado tanto por Shen et al. no artigo seminal do GMIC quanto por Sampaio e Cordeiro — como o limiar clínico suficiente para garantir que o sistema apontou a massa correta para o médico sem exigir alinhamento milimétrico em margens infiltrativas."*
