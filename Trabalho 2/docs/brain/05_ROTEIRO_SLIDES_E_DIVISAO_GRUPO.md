# 05. Planejamento Estruturado da Apresentação e Divisão do Grupo
## Roteiro de Slides, Alocação de Tempo e Scripts de Transição para o Trio (Grupo 4)

---

## 1. Estratégia Geral e Gestão Rigorosa do Tempo (30 a 40 Minutos)

Para atender perfeitamente aos critérios de avaliação da UFPI:
- **Tempo Mínimo Exigido:** 30 minutos (menos de 30 acarreta perda de nota por falta de aprofundamento).
- **Tempo Máximo Permitido:** 40 minutos (interrupção obrigatória pela banca avaliadora).
- **Tempo Alvo do Grupo 4:** **34 a 36 minutos** (zona de segurança ideal com margem de 4 minutos).

```mermaid
gantt
    title Cronograma de Apresentação Oral (Janela de 36 Minutos)
    dateFormat  m
    axisFormat %M min
    
    section Aluno 1
    Abertura e Contextualização           :0, 2
    Artigo 1: Problema, Dados e Auditoria :2, 6
    Artigo 1: CNN, Treino e Grad-CAM      :6, 12
    
    section Aluno 2
    Artigo 2: Citopatologia e Bethesda    :12, 15
    Artigo 2: ViT e Patches Dinâmicos     :15, 20
    Artigo 2: Resultados e Grid vs Dinâmico:20, 24
    
    section Aluno 3
    Matriz Comparativa e Trade-offs       :24, 28
    Duelo Teórico: Viés Indutivo vs ViT   :28, 32
    Árvore Decisória e Conclusão          :32, 35
    
    section Coletivo
    Encerramento e Abertura para Banca    :35, 36
```

---

## 2. Divisão de Responsabilidades no Trio

| Integrante | Bloco Temático | Tempo Estimado | Foco Técnico Principal |
| :--- | :--- | :---: | :--- |
| **Aluno 1** | **Abertura & Artigo 1 (CNN Brain Tumor)** | **11 a 12 min** | Contexto clínico de MRI, auditoria de dados com Figshare, arquitetura convolucional adaptada da AlexNet, 5-Fold Cross Validation, acurácia de 99% e mapas Grad-CAM com validação externa. |
| **Aluno 2** | **Artigo 2 (ViT Patches Dinâmicos)** | **11 a 12 min** | Citopatologia cervical Bethesda, dataset CRIC, divisão estrita por paciente, balanceamento híbrido com Albumentations, os 5 métodos dinâmicos (GrabCut, Espiral...), projeção Conv2d vs Linear e resultados da Tabela 2. |
| **Aluno 3** | **Análise Comparativa & Discussão Crítica** | **11 a 12 min** | Matriz multidimensional comparativa, debate de viés indutivo vs atenção global, fenômeno de *data-hunger*, análise de causa-raiz da sobreposição de patches, comparação com ensemble de CNNs (95%) e síntese final. |

---

## 3. Decomposição Slide a Slide (Estrutura Completa de 24 Slides)

### BLOCO 1: INTRODUÇÃO E ARTIGO 1 (Apresentador: Aluno 1)

#### Slide 01: Capa Institucional e Apresentação do Grupo
- **Elementos Visuais:** Brasão da UFPI, identificação da disciplina (Tópicos Especiais em Visão Computacional), Prof. Dr. José Denes Lima Araújo, Grupo 4, nomes completos dos 3 integrantes, títulos oficiais dos dois artigos com logotipos da SBC/BRACIS.
- **Roteiro de Fala (Aluno 1):**  
  *"Bom dia/boa tarde a todos. Sou o [Aluno 1] e, juntamente com meus colegas [Aluno 2] e [Aluno 3], compomos o Grupo 4. Hoje apresentaremos nossa pesquisa e análise crítica comparativa sobre dois artigos completos da Sociedade Brasileira de Computação na área de classificação em imagens médicas. O primeiro artigo propõe uma rede neural convolucional para classificação de tumores cerebrais em ressonância magnética, publicado no BRACIS 2023 pela UFCSPA. O segundo artigo, publicado em 2025 pela PUC Minas e UFMG, investiga o uso de Vision Transformers com técnicas dinâmicas de extração de patches para o diagnóstico citopatológico de câncer de colo uterino."*

#### Slide 02: Motivação Clínica e o Desafio da Classificação em Imagens Médicas
- **Elementos Visuais:** Comparação lado a lado de uma fatia de ressonância magnética (macroestrutura encefálica) e uma micrografia citológica de Papanicolau (microestrutura celular).
- **Roteiro de Fala (Aluno 1):**  
  *"A visão computacional aplicada à saúde enfrenta desafios singulares: a escassez de dados rotulados por especialistas, o severo desbalanceamento de classes onde patologias graves são minoritárias e a exigência mandatória de explicabilidade clínica. Ao longo desta apresentação, veremos como dois grupos de pesquisadores brasileiros abordaram problemas de classificação através de dois paradigmas distintos: o paradigma convolucional clássico e o paradigma emergente dos mecanismos de autoatenção em Vision Transformers."*

#### Slide 03: Artigo 1 (UFCSPA) – Contexto Clínico e as 4 Classes de Tumor Cerebral
- **Elementos Visuais:** Quatro imagens representativas das classes diagnósticas: Glioma, Meningioma, Sem Tumor (Normal) e Adenoma de Hipófise (Pituitary).
- **Roteiro de Fala (Aluno 1):**  
  *"Iniciando a desconstrução do Artigo 1, o objetivo dos pesquisadores da UFCSPA foi o diagnóstico diferencial de quatro condições em exames de ressonância magnética. O Glioma é um tumor maligno altamente infiltrativo que exige intervenção cirúrgica urgente. O Meningioma é tipicamente benigno e de crescimento dural. A classe Sem Tumor valida a triagem para evitar falsos alarmes, e os tumores de Hipófise originam-se na base do crânio com impacto endócrino e óptico. A diferenciação precisa entre essas quatro condições dita o plano cirúrgico e o prognóstico de sobrevida do paciente."*

#### Slide 04: Base de Dados, Descoberta de Erros de Rótulo e Higienização
- **Elementos Visuais:** Fluxograma mostrando a auditoria do *Brain Tumor MRI Dataset* (Kaggle, 7.023 imagens), o isolamento de amostras corrompidas de glioma e a substituição cirúrgica com o dataset auditado *Figshare*. Gráfico de distribuição com as 5.531 imagens de treino e 1.297 de teste.
- **Roteiro de Fala (Aluno 1):**  
  *"Um dos pontos de maior destaque metodológico deste trabalho foi o rigor na curadoria de dados. Ao analisarem o popular benchmark público do Kaggle com mais de 7 mil imagens, os autores identificaram inconsistências graves de rotulagem na pasta de gliomas. Em vez de treinar a rede sobre dados ruidosos, substituíram essas amostras por instâncias validadas da base Figshare. O conjunto de treino ajustado ficou com 5.531 imagens e o teste independente com 1.297 imagens."*

#### Slide 05: Pré-Processamento, Balanceamento e Prevenção de Data Leakage
- **Elementos Visuais:** Pipeline gráfico: Redimensionamento $64 \times 64 \to$ Normalização $[0.0, 1.0] \to$ Aplicação de Pesos de Classe ($w_{\text{glioma}} = 1.21$, $w_{\text{meningioma}} = 1.03$, $w_{\text{notumor}} = 0.86$, $w_{\text{pituitary}} = 0.94$) $\to$ Shuffling por época.
- **Roteiro de Fala (Aluno 1):**  
  *"As imagens foram redimensionadas para matrizes compactas de 64 por 64 pixels e normalizadas dividindo-se por 255. Para mitigar o desbalanceamento sem introduzir artefatos, aplicaram pesos inversamente proporcionais diretamente na função de perda. Fundamental destacar: para impedir o vazamento de dados (data leakage), a segregação entre treino e teste ocorreu estritamente antes da normalização, e as amostras foram reembaralhadas a cada época de treinamento."*

#### Slide 06: Arquitetura da Rede Neural Convolucional Proposta
- **Elementos Visuais:** Diagrama arquitetural completo: 3 Blocos Convolucionais (Conv2D $3 \times 3$, ReLU, MaxPool $2 \times 2$) com perfil de Dropout progressivo ($20\% \to 25\% \to 30\%$) $\to$ Flatten (4.096) $\to$ Dense (32 com regularização $L_2$) $\to$ Dense (4 com Softmax).
- **Roteiro de Fala (Aluno 1):**  
  *"A arquitetura foi adaptada e otimizada a partir dos fundamentos da AlexNet. Trata-se de uma rede enxuta composta por três blocos convolucionais com filtros crescentes de 16, 32 e 64, todos com kernels 3 por 3 e ativação ReLU. Observem a estratégia de regularização progressiva: o Dropout inicia em 20% no primeiro bloco, sobe para 25% no segundo e atinge 30% no terceiro. A camada densa intermediária de 32 neurônios conta ainda com penalização por decaimento de pesos L2, garantindo contenção máxima contra o sobreajuste."*

#### Slide 07: Pipeline de Treinamento: K-Fold (5 Folds) e Callbacks Inteligentes
- **Elementos Visuais:** Diagrama do 5-Fold Cross Validation com 60 épocas por dobra. Linha do tempo dos Callbacks: Early Stopping (paciência = 18 épocas), ReduceLROnPlateau (fator 0.2 com paciência 5) e ModelCheckpoint.
- **Roteiro de Fala (Aluno 1):**  
  *"O treinamento utilizou o otimizador Adam e a função Sparse Categorical Cross-Entropy. Para assegurar confiabilidade estatística, os autores empregaram validação cruzada K-Fold com 5 dobras independentes. O controle de convergência foi governado por callbacks inteligentes: um Early Stopping com paciência de 18 épocas e um agendador de taxa de aprendizado que reduzia o passo em 80% caso a perda de validação estagnasse por 5 épocas, salvando sempre o estado ótimo de pesos sinápticos."*

#### Slide 08: Resultados Quantitativos (Acurácia de 99%) e Relatório por Classe
- **Elementos Visuais:** Tabela do relatório de classificação no conjunto de teste independente (1.311 imagens) destacando: Glioma (P: 1.00, R: 1.00, F1: 1.00), Meningioma (F1: 0.98), No Tumor (F1: 0.99), Pituitary (F1: 0.99) e Acurácia Global de 99%. Curva ROC/AUC.
- **Roteiro de Fala (Aluno 1):**  
  *"No conjunto de teste cego com 1.311 imagens, o modelo alcançou uma acurácia global de 99%. Do ponto de vista médico, o resultado mais notável reside na classe Glioma, que obteve precisão de 100%, revocação de 100% e F1-score de 1,00 em 286 casos. Isso comprova que a rede não produziu um único falso-negativo para a neoplasia mais letal. As demais classes também demonstraram desempenho próximo à perfeição, consolidando uma área sob a curva ROC quase unitária."*

#### Slide 09: Explicabilidade (XAI) com Grad-CAM e Validação Externa
- **Elementos Visuais:** Imagens de ressonância com sobreposição dos mapas de calor Grad-CAM sobre as camadas convolucionais. Destaque para o teste cego de validação na base externa de Bhuvaji et al.
- **Roteiro de Fala (Aluno 1):**  
  *"Para certificar que a rede não estava tomando decisões com base em ruídos ou ossos cranianos, aplicou-se o Grad-CAM nas últimas camadas convolucionais. Os mapas térmicos provam que o modelo foca com exatidão anatômica sobre o epicentro da lesão tumoral. Mais relevante ainda: os pesquisadores testaram o Grad-CAM em imagens de uma base de dados externa nunca vista durante os treinos, confirmando a generalização clínica da explicabilidade.*  
  *Passo agora a palavra ao colega [Aluno 2], que nos apresentará o segundo artigo, focado no uso de Vision Transformers com patches dinâmicos."*

---

### BLOCO 2: ARTIGO 2 – VISION TRANSFORMERS E PATCHES DINÂMICOS (Apresentador: Aluno 2)

#### Slide 10: Artigo 2 (PUC Minas / UFMG) – Citologia Cervical e o Sistema Bethesda
- **Elementos Visuais:** Esquema do exame de Papanicolau e tabela com as 6 categorias morfológicas do Sistema Bethesda: ASC-H, ASC-US, HSIL, LSIL, NFIL e SCC.
- **Roteiro de Fala (Aluno 2):**  
  *"Obrigado, [Aluno 1]. Entrando na análise do Artigo 2, publicado em 2025 por Giovanini e Machado, o desafio abordado é o diagnóstico precoce do câncer de colo uterino através de lâminas citológicas de Papanicolau. O problema foi modelado em seis classes celulares do Sistema Bethesda, variando desde células completamente sadias (NFIL), passando por atipias indeterminadas (ASC-US e ASC-H) e lesões pré-malignas de baixo e alto grau (LSIL e HSIL), até o carcinoma escamoso já invasivo (SCC). A leitura dessas lâminas é exaustiva e suscetível à fadiga do citotécnico."*

#### Slide 11: Dataset CRIC, Particionamento Anti-Leakage por Paciente e Balanceamento Híbrido
- **Elementos Visuais:** Tabela de dados antes e depois do balanceamento (Total de 11.534 núcleos). Destaque visual para o split por paciente (64% treino, 20% validação, 16% teste) e o oversampling com Albumentations (SCC de 103 para 1.000) vs undersampling (NFIL de 4.339 para 1.000).
- **Roteiro de Fala (Aluno 2):**  
  *"Os experimentos utilizaram o dataset CRIC da UFOP, com 11.534 núcleos segmentados. Ressalto aqui o extremo rigor contra o vazamento de dados: a divisão entre treino, validação e teste foi feita por paciente. Nenhuma paciente teve células compartilhadas entre conjuntos. O desbalanceamento original era crítico: tínhamos mais de 4.300 células sadias de treino contra apenas 103 de carcinoma invasivo. Os autores aplicaram balanceamento híbrido fixando 1.000 amostras por classe no treino: oversampling com rotações e flips via Albumentations para as minoritárias e undersampling para as majoritárias."*

#### Slide 12: Arquitetura Vision Transformer (ViT): Projeção Linear vs. Convolucional
- **Elementos Visuais:** Diagrama do fluxo do ViT: Imagem $224 \times 224 \to$ 196 patches $16 \times 16 \to$ Projeção Linear vs Conv2D $\to$ Concatenação do Token [CLS] $\to$ Positional Embeddings 1D $\to$ Blocos Encoder Transformer (Atenção Multi-Head e MLP).
- **Roteiro de Fala (Aluno 2):**  
  *"O artigo explorou modelos Vision Transformer pré-treinados na ImageNet-21k, avaliando as variantes Tiny, Small e Base. Em imagens de 224 por 224 pixels com patches de 16 por 16, geram-se 196 patches. Os autores investigaram duas formas de gerar os embeddings dos patches: a Projeção Linear direta dos pixels e a Projeção Convolucional, onde uma camada Conv2D de kernel 16 e stride 16 extrai feições locais antes de alimentar a sequência de atenção global."*

#### Slide 13: A Hipótese Central: As 5 Técnicas de Extração Dinâmica de Patches
- **Elementos Visuais:** Painel ilustrativo das 5 abordagens: 1. Seleção Randômica (SR); 2. Randômica Aprimorada com restrição de distância (RA); 3. Segmentação morfológica GrabCut (SS); 4. Percurso Zigue-Zague (ZZ); 5. Espiral partindo do núcleo (ES).
- **Roteiro de Fala (Aluno 2):**  
  *"A grande hipótese de inovação do artigo foi: como o núcleo atípico ocupa apenas uma fração central de 90 por 90 pixels, por que não concentrar os 196 patches sobre a região de interesse celular e evitar o fundo branco vazio da lâmina? Foram formulados cinco métodos dinâmicos: o sorteio puramente aleatório SR; a amostragem aprimorada RA com distância euclidiana mínima entre centros; a seleção por segmentação SS, que usa o algoritmo GrabCut para criar uma máscara e amostrar apenas sobre a célula; o percurso em zigue-zague ZZ; e a extração em espiral ES, que inicia no núcleo e expande concentricamente para fora."*

#### Slide 14: Infraestrutura de Hardware e Descongelamento Seletivo (*Fine-Tuning*)
- **Elementos Visuais:** Tabela comparando o ambiente local (GPU RTX 2060 6GB para Small) com o Google Colab PRO (GPU Tesla T4 15GB para Base). Esquema visual dos blocos do ViT-Small descongelados (2 primeiros e 3 últimos blocos do codificador). Hiperparâmetros: Learning rate $1 \times 10^{-5}$, batch 32.
- **Roteiro de Fala (Aluno 2):**  
  *"O treinamento do ViT impôs demandas computacionais severas. O modelo Small foi processado localmente em uma RTX 2060 de 6 GB, descongelando-se os dois primeiros blocos e os três últimos blocos do codificador de 12 camadas, com taxa de aprendizado de 1e-5. Já o modelo Base exigiu o Colab PRO com GPU Tesla T4 de 15 GB, e devido à complexidade massiva, apenas o último MLP pôde ser descongelado para evitar estouro de memória e sobreajuste."*

#### Slide 15: Resultados Experimentais (Tabela 2) e o Paradoxo do Grid
- **Elementos Visuais:** Tabela completa com os resultados de acurácia no teste: ViT-Small Grid Conv2D Baseline (**0,79 teste / 0,81 validação**) em contraste com Espiral Conv2D (**0,78**), RA Conv2D (**0,77**), SS Conv2D (**0,76**), e os resultados inferiores com projeção linear (0,60 a 0,71).
- **Roteiro de Fala (Aluno 2):**  
  *"Chegamos aos resultados cruciais da Tabela 2 do artigo. O achado mais surpreendente foi: o modelo ViT-Small convencional sem qualquer modificação dinâmica, usando o simples grid estático uniforme com projeção convolucional, obteve 79% de acurácia no teste e superou todas as cinco técnicas dinâmicas propostas! Dentre os métodos dinâmicos, a extração em Espiral com Conv2D foi a melhor colocada com 78%, e a projeção convolucional superou a linear em todas as configurações.*  
  *Transfiro a apresentação para o [Aluno 3], que conduzirá a discussão crítica sobre as causas desses achados e o confronto direto entre os dois artigos."*

---

### BLOCO 3: COMPARAÇÃO MULTIDIMENSIONAL E DISCUSSÃO CRÍTICA (Apresentador: Aluno 3)

#### Slide 16: Análise de Causa-Raiz: Por Que o Grid Venceu os Métodos Dinâmicos?
- **Elementos Visuais:** Diagrama geométrico ilustrando a superposição excessiva de patches de $16 \times 16$ concentrados no espaço reduzido de $90 \times 90$, a perda da relação núcleo-citoplasma e a quebra dos positional embeddings pré-treinados na ImageNet.
- **Roteiro de Fala (Aluno 3):**  
  *"Obrigado, [Aluno 2]. O resultado de Giovanini e Machado é um exemplo brilhante do valor de um resultado negativo na ciência. A hipótese dos patches dinâmicos foi refutada por três razões fundamentais: primeiro, ao espremer 196 patches em uma área central de 90 por 90 pixels, a taxa de sobreposição ultrapassou 80%, colapsando os tensores de atenção em pura redundância. Segundo, quebrou-se a estrutura dos positional embeddings aprendidos na ImageNet sobre uma grade cartesiana. E terceiro, na citologia, o diagnóstico depende da relação núcleo-citoplasma: concentrar tudo no núcleo cegou o modelo quanto ao citoplasma periférico."*

#### Slide 17: Por Que o Ensemble de CNNs (95%) Superou o Vision Transformer (79%)?
- **Elementos Visuais:** Gráfico comparativo de acurácia na base CRIC: Ensemble de CNNs de Diniz et al. (95%) vs ViT-Small Grid (79%) vs ViTs Dinâmicos (60% a 78%).
- **Roteiro de Fala (Aluno 3):**  
  *"Ao confrontarmos o ViT com o estado da arte na base CRIC estabelecido por Diniz et al. em 2021 com um Ensemble de CNNs, vemos uma disparidade contundente: 95% da CNN contra 79% do ViT. O motivo é estrutural: Redes Convolucionais trazem campos receptivos locais e equivariância translacional codificados em suas equações. Já os Vision Transformers não possuem esse viés indutivo e sofrem do fenômeno de fome de dados (data-hunger). Em bases médicas com poucos milhares de imagens, os Transformers simplesmente não dispõem de dados suficientes para aprender as leis espaciais da visão do zero."*

#### Slide 18: Matriz Comparativa Sistemática: Artigo 1 vs. Artigo 2
- **Elementos Visuais:** Tabela síntese dos 8 principais eixos comparativos: Domínio Clínico, Dados/Volume, Resolução, Particionamento e Leakage, Paradigma Arquitetural, Pre-treino vs Scratch, Desempenho e Custo Computacional.
- **Roteiro de Fala (Aluno 3):**  
  *"Esta matriz comparativa consolida os dois mundos. No Artigo 1, a UFCSPA utilizou uma CNN leve e desenhada sob medida, treinada do zero em imagens 64 por 64, alcançando 99% de acurácia com custo computacional quase nulo. No Artigo 2, a PUC Minas e a UFMG operaram na fronteira dos Transformers com fine-tuning na ImageNet em 224 por 224, demandando GPUs parrudas como a Tesla T4 e atingindo 79% no teste. Dois problemas biomédicos de alta relevância, mas com exigências de engenharia totalmente discrepantes."*

#### Slide 19: Análise Crítica dos Protocolos: *Slice Leakage* vs. *Patient Stratification*
- **Elementos Visuais:** Esquema ilustrativo comparando o risco de vazamento em cortes 2D adjacentes de MRI (Artigo 1) com a blindagem perfeita por código de paciente no CRIC (Artigo 2).
- **Roteiro de Fala (Aluno 3):**  
  *"Exercendo nosso papel de análise crítica, devemos apontar que o Artigo 2 foi impecável na estratificação por paciente, eliminando qualquer risco de o modelo memorizar tons de lâmina. No Artigo 1, embora a acurácia de 99% seja formidável, exames de ressonância 2D divididos aleatoriamente trazem o risco latente de slice leakage, onde fatias adjacentes do mesmo crânio podem ter ficado no treino e no teste. Os autores da UFCSPA contornaram parcialmente essa dúvida ao validar o Grad-CAM em uma base externa completamente inédita, mas o split por paciente permanece como a recomendação ideal para trabalhos futuros."*

#### Slide 20: Árvore de Decisão de Engenharia: Quando Escolher CNN ou ViT na Saúde?
- **Elementos Visuais:** Fluxograma decisório para cientistas de dados e engenheiros biomédicos (Volume de Dados $< 10k \to$ CNN; Volume massivo e contexto de longa distância $\to$ ViT com Grid Regular e Projeção Convolucional; Hardware restrito/Edge $\to$ CNN especializada).
- **Roteiro de Fala (Aluno 3):**  
  *"A partir da convergência desses dois artigos, estruturamos uma árvore de decisão para projetos reais de Visão Computacional Médica: para bancos de dados com menos de 10 mil exames e infraestrutura computacional restrita, CNNs convolucionais bem regularizadas continuam sendo a escolha mais robusta, econômica e precisa. Vision Transformers devem ser reservados para cenários de Whole Slide Imaging com centenas de milhares de amostras, sempre mantendo a grade uniforme e a projeção convolucional como extrator primário de características."*

#### Slide 21: Lições Aprendidas e Conclusões Finais do Grupo 4
- **Elementos Visuais:** 4 pontos-chave em cartões destacados: 1. A relevância epistemológica do resultado negativo; 2. O papel insubstituível da curadoria de dados e explicabilidade (XAI); 3. O viés indutivo como aliado em datasets pequenos; 4. A superioridade da projeção convolucional sobre a linear.
- **Roteiro de Fala (Aluno 3):**  
  *"Concluímos este seminário com quatro grandes lições: Primeiro, a inteligência artificial médica só avança quando aceitamos publicar resultados negativos bem fundamentados, como os patches dinâmicos. Segundo, auditar rótulos incorretos e gerar mapas Grad-CAM é indispensável para a aceitação clínica de qualquer modelo. Terceiro, o hype em torno dos Vision Transformers não anula a eficácia matemática das convoluções em dados biomédicos esparsos. E quarto, a abordagem híbrida convolucional-atenção desponta como o futuro mais promissor da área."*

#### Slide 22: Referências Bibliográficas (Normas SBC / ABNT)
- **Elementos Visuais:** Citações formais completas do Artigo 1 (BRACIS 2023), Artigo 2 (SBC 2025), datasets Figshare e CRIC, referências da AlexNet (Krizhevsky et al.), ViT (Dosovitskiy et al.) e Ensemble CNN (Diniz et al., 2021).
- **Roteiro de Fala (Aluno 3):**  
  *"Aqui constam todas as fontes bibliográficas primárias e secundárias que subsidiaram nossa análise crítica, respeitando as normas da SBC."*

#### Slide 23: Agradecimentos e Abertura para a Banca Avaliadora
- **Elementos Visuais:** Slide limpo com mensagem de agradecimento, e-mails dos três integrantes e do Prof. Dr. José Denes Lima Araújo.
- **Roteiro de Fala (Aluno 3 / Trio):**  
  *"Agradecemos a atenção do Professor José Denes e dos colegas de turma. Encerramos nossa explanação rigorosamente dentro do prazo estipulado e estamos à disposição para as perguntas e discussões da banca avaliadora."*

---

## 4. Dicas de Postura e Transição para Nota Máxima Individual

1. **Fluidez nas Transições Verbais:**  
   Nunca use silêncio ou pausas constrangedoras. Sempre use a deixa planejada no roteiro para passar a palavra ao colega pelo nome com cortesia acadêmica (*"Passo agora a palavra ao colega [Nome]..."*).
2. **Câmera Ligada e Engajamento Contínuo:**  
   Mesmo quando não estiver apresentando seu slide, mantenha a câmera ligada, olhe na direção da lente, balance a cabeça em concordância técnica e demonstre presença ativa. O critério individual *Participação, postura e envolvimento* vale **1,0 ponto integral**.
3. **Domínio Terminológico:**  
   Não utilize termos leigos como "o algoritmo chutou a classe" ou "ele juntou as fotos". Use sempre o jargão científico correto: *"o classificador inferiu as probabilidades a posteriori"*, *"realizou-se o particionamento estratificado"*, *"aplicou-se decaimento de pesos com penalização L2"*.
