# Roteiro de Apresentação e Divisão de Falas (23 Slides)

**Título do Trabalho:** Um Estudo sobre Mapas de Ativação de Classe (CAM) para Detecção de Massas em Mamografias via Aprendizado Fracamente Supervisionado  
**Artigo Base Reproduzido:** Sampaio, V.; Cordeiro, F. R. *A Study on Class Activation Map Methods to Detect Masses in Mammography Images using Weakly Supervised Learning* (UFRPE, 2022)  
**Integrantes:** Walison Weudes, Hermeson Alves e Marcos Willian (`UFPI | CSHNB — Visão Computacional`)  
**Template Canva Utilizado:** *Apresentação genérica minimalista cinza* (`DAHbBE7J4gk`)

---

## Divisão Equilibrada entre os 3 Integrantes

| Integrante | Parte da Apresentação | Slides | Tempo Sugerido |
| :--- | :--- | :---: | :---: |
| **1. Walison Weudes** | **Parte 1 — Contexto do Artigo:** Capa, Sumário, Introdução & Problema Clínico, Gargalo da Anotação (Supervisão Total vs. WSOD), O Artigo Base (Sampaio & Cordeiro, 2022) e Resumo da Solução Proposta (Desacoplamento). | **Slides 01 a 06** (6 slides) | ~5 min |
| **2. Hermeson Alves** | **Parte 2 — Explicação do Modelo e Como Funciona:** Visão Geral do Modelo GMIC (Figura 2), Módulo Global ResNet-22 & Seleção Gulosa de Patches, Módulo Local ResNet-18 (MIL) & Fusão & Loss (Equação 2), Fundamentos do CAM (Figura 1 e Equação 1), Evolução dos 4 CAMs de Gradiente e A Teoria do Desacoplamento Treino vs. Teste. | **Slides 07 a 13** (7 slides) | ~6 min |
| **3. Marcos Willian** | **Parte 3 — Resultados Comparativos, Auditoria e Conclusão:** Base VinDr-Mammo (Figura 3), Implementação PyTorch & Protocolo WSOD ($\text{IoU} \ge 0{,}3$), Resultados de Classificação Global (Tabela 1), Auditoria Crítica da Errata na Tabela 1 ($\text{FNR}$ vs. $\text{TNR}$), Matriz $\text{TPR}@\text{FPPI}$ (Tabela 2), Comparação Visual Qualitativa (Figura 4), Trade-off Clínico FROC e Conclusões Gerais. | **Slides 14 a 23** (10 slides, sendo 2 divisores/encerramento) | ~6 min |

---

## Parte 1 — Contexto do Artigo (Walison Weudes — Slides 01 a 06)

### Slide 01 — Capa (`Pág. 01/23`)
- **Fala sugerida:**
  > "Olá a todos, somos o grupo formado por Walison Weudes, Hermeson Alves e Marcos Willian. Neste trabalho final de Visão Computacional na UFPI/CSHNB, realizamos a reprodução científica, implementação em PyTorch e auditoria crítica do artigo de Vicente Sampaio e Filipe Cordeiro (2022), que investiga métodos de Mapas de Ativação de Classe (CAMs) para detecção de massas em mamografias utilizando aprendizado fracamente supervisionado (WSOD)."

### Slide 02 — Sumário (`Pág. 02/23`)
- **Fala sugerida:**
  > "Organizamos nossa apresentação em três grandes blocos: na Parte 1, apresentarei o contexto clínico, o problema da anotação em mamografia, o artigo base e o resumo da solução proposta. Na Parte 2, o Hermeson explicará em detalhes como funciona a arquitetura híbrida GMIC, sua função de perda e a matemática dos 5 mapas de ativação. Por fim, na Parte 3, o Marcos apresentará a base VinDr-Mammo, nossa reprodução em PyTorch, as tabelas e figuras comparativas do artigo, uma errata matemática inédita que identificamos na Tabela 1 original e as conclusões gerais."

### Slide 03 — 1. Introdução e Problema Clínico na Mamografia (`Pág. 03/23`)
- **Fala sugerida:**
  > "O câncer de mama é a principal causa de morte por neoplasias em mulheres no mundo, e a mamografia digital (FFDM) é o exame padrão-ouro para triagem precoce. Do ponto de vista de Visão Computacional, contudo, a mamografia impõe dois desafios severos: primeiro, a resolução nativa extrema (2944 por 1920 pixels), onde um nódulo maligno inicial ocupa menos de 2% da área total do exame; segundo, o baixo contraste em mamas densas, onde o parênquima fibroglandular saudável possui radiopacidade muito semelhante à da massa tumoral."

### Slide 04 — 2. Gargalo da Anotação: Supervisão Total vs. WSOD (`Pág. 04/23`)
- **Fala sugerida:**
  > "Detectores clássicos totalmente supervisionados, como Faster R-CNN, YOLO ou U-Net, exigem milhares de caixas delimitadoras (bounding boxes) desenhadas manualmente por radiologistas. Na prática hospitalar (sistemas PACS), esse tipo de anotação pixel a pixel é raríssimo e caro; o que existe em abundância são laudos globais dizendo apenas se o exame é Normal ou possui Massa. É aqui que entra o paradigma WSOD (*Weakly Supervised Object Detection*): treinamos a rede neural usando exclusivamente o rótulo binário global da imagem ($y \in \{0, 1\}$), sem nenhuma bounding box no treino, e usamos Mapas de Ativação de Classe (CAMs) na inferência para localizar espacialmente a lesão."

### Slide 05 — 3. O Artigo Base: Sampaio & Cordeiro (UFRPE, 2022) (`Pág. 05/23`)
- **Elemento Visual no Slide:** Print real do título, autores e *Abstract* do artigo original.
- **Fala sugerida:**
  > "Como vemos no print do artigo original ao lado, Sampaio e Cordeiro observaram uma lacuna importante na literatura: até então, os modelos WSOD para mamografia — incluindo o estado-da-arte GMIC de Shen et al. (2021) — utilizavam exclusivamente o método CAM clássico de 2016. O problema é que o CAM clássico gera mapas de calor muito espalhados ao redor da massa, produzindo uma taxa alta de Falsos Positivos por Imagem ($\text{FPPI} = 1{,}55$). O artigo propõe então substituir e comparar 5 famílias de mapas de ativação dentro da arquitetura GMIC na base pública VinDr-Mammo."

### Slide 06 — 4. Resumo da Solução: Desacoplamento Treino vs. Teste (`Pág. 06/23`)
- **Elemento Visual no Slide:** Diagrama arquitetural do Desacoplamento Treino (`XGrad-CAM`) vs. Teste (`Grad-CAM++`).
- **Fala sugerida:**
  > "Para fechar a Parte 1 com o resumo da solução: o grande insight de Sampaio e Cordeiro foi perceber que o mapa de ativação usado durante o TREINAMENTO (para guiar quais recortes a rede deve observar) não precisa ser o mesmo mapa usado no TESTE (para desenhar a caixa delimitadora da lesão). Ao usar o XGrad-CAM no treinamento como um filtro seletivo livre de ruído e o Grad-CAM++ no teste para expandir o mapa até as bordas completas do tumor, o modelo eleva a sensibilidade para 70% e reduz os falsos positivos por imagem em 43,2% (caindo de 1,55 para 0,88). Passo agora a palavra ao Hermeson para explicar como o modelo funciona."

---

## Parte 2 — Explicação do Modelo e Como Funciona (Hermeson Alves — Slides 07 a 13)

### Slide 07 — Divisor Parte 2: Modelo GMIC e Mapas de Ativação (`Pág. 07/23`)
- **Fala sugerida:**
  > "Obrigado, Walison. Nesta segunda parte, vamos abrir a caixa-preta do modelo GMIC (*Globally-Aware Multiple Instance Classifier*) e entender matematicamente como ele processa imagens de quase 6 megapixels e como cada um dos 5 métodos de mapas de ativação opera."

### Slide 08 — 5. Visão Geral do Modelo GMIC (Figura 2 do Artigo) (`Pág. 08/23`)
- **Elemento Visual no Slide:** Print real da **Figura 2** do artigo original (*Modelo GMIC*).
- **Fala sugerida:**
  > "Se reduzirmos uma mamografia de $2944 \times 1920$ para $224 \times 224$ pixels, perdemos as margens espiculadas da lesão; mas se passarmos a imagem inteira em uma CNN densa tradicional, estouramos a memória de vídeo (VRAM). Como mostra a Figura 2 do artigo ao lado, o GMIC resolve esse dilema imitando o radiologista em duas etapas: primeiro, uma rede global lê a imagem inteira e gera um mapa de saliência $A$ de baixa resolução; segundo, o modelo recorta os $K=6$ patches mais brilhantes diretamente da imagem de alta resolução original e funde o diagnóstico global com o diagnóstico local."

### Slide 09 — 6. Módulo Global (ResNet-22) e Seleção Gulosa de Patches (`Pág. 09/23`)
- **Elemento Visual no Slide:** Print real da **Figura 2** do artigo original.
- **Fala sugerida:**
  > "Detalhando o Módulo Global: a mamografia completa entra em uma ResNet-22 customizada com stride total 32, produzindo um tensor convolucional $S_g$ de 512 canais por $92 \times 60$. Aplicamos Global Average Pooling para obter o vetor $\mathbf{h}_{\text{global}} \in \mathbb{R}^{512}$ e a predição $\hat{y}_{\text{global}}$. Em paralelo, o método CAM ativo projeta os 512 canais no mapa de calor $A^c$ ($92 \times 60$). Em seguida, entra o algoritmo guloso (*Retrieve ROI Crops*): em $K=6$ iterações, ele acha o pico de maior energia em $A^c$, converte a coordenada para a escala original ($2944 \times 1920$), recorta um patch de $256 \times 256$ pixels e zera aquela vizinhança no mapa $A^c$ para garantir 6 recortes sem sobreposição."

### Slide 10 — 7. Módulo Local (ResNet-18 MIL), Fusão e Função de Perda (Eq. 2) (`Pág. 10/23`)
- **Elemento Visual no Slide:** Print real da **Equação 2** do artigo original (*Função de perda do GMIC*).
- **Fala sugerida:**
  > "Os $K=6$ patches de $256 \times 256$ passam então por um backbone local ResNet-18, gerando 6 vetores de características. Sob a premissa de *Multiple Instance Learning* (MIL) — onde basta um patch conter tumor para o exame ser positivo — aplicamos Max-Pooling instância a instância para obter $\mathbf{h}_{\text{local}}$ e $\hat{y}_{\text{local}}$. O Módulo de Fusão concatena $[\mathbf{h}_{\text{global}} ; \mathbf{h}_{\text{local}}] \in \mathbb{R}^{1024}$ e gera a predição final $\hat{y}_{\text{fusao}}$. Todo o sistema é treinado de ponta a ponta pela Equação 2 do artigo mostrada abaixo: somamos a Entropia Cruzada Binária (BCE) dos 3 ramos (local, global e fusão) mais uma regularização L1 de esparsidade sobre o mapa de ativação ($L_{\text{reg}}(A^c) = \|A^c\|_1$) com peso $\beta = 3{,}26$, que força o mapa térmico a apagar o fundo e iluminar apenas a lesão."

### Slide 11 — 8. Fundamentos dos Mapas de Ativação (CAM — Figura 1 e Eq. 1) (`Pág. 11/23`)
- **Elemento Visual no Slide:** Print real da **Figura 1** e da **Equação 1** do artigo original.
- **Fala sugerida:**
  > "Mas como o mapa $A^c$ é construído? A Equação 1 e a Figura 1 do artigo, exibidas à esquerda, definem a estrutura geral: combinamos linearmente os $N_l = 512$ canais convolucionais $A_k$ ponderados pelos pesos de importância $\alpha_k$, aplicando a função ReLU para descartar influências negativas. No método CAM clássico de Zhou et al. (2016), os coeficientes $\alpha_k$ são simplesmente os pesos estáticos da camada totalmente conectada final. Como esses pesos são fixos para todo o canal espacial, o CAM clássico tende a espalhar calor além das fronteiras reais da massa."

### Slide 12 — 9. Evolução: Grad-CAM, Grad-CAM++, XGrad-CAM e Layer-CAM (`Pág. 12/23`)
- **Elemento Visual no Slide:** Painel comparativo dos 5 métodos de mapas de ativação.
- **Fala sugerida:**
  > "Para superar a rigidez do CAM clássico, o artigo investiga 4 variantes baseadas em gradiente:
  > 1) O **Grad-CAM** usa a média espacial simples dos gradientes da classe em relação ao mapa convolucional; ele foca apenas no miolo mais denso da lesão, sub-segmentando as bordas.
  > 2) O **Grad-CAM++** introduz derivadas parciais de 2ª e 3ª ordem sobre os gradientes positivos, conseguindo expandir a ativação por toda a geometria da massa.
  > 3) O **XGrad-CAM** parte de dois axiomas matemáticos (Sensibilidade e Conservação) e pondera cada gradiente pela ativação normalizada da própria célula, atuando como um filtro altamente seletivo contra picos falsos.
  > 4) Já o **Layer-CAM** multiplica ponto a ponto cada ativação pelo seu gradiente positivo; porém, em mamografias densas, isso amplifica ruídos de textura e explode os falsos positivos."

### Slide 13 — 10. Por que Desacoplar o CAM entre Treino e Teste? (`Pág. 13/23`)
- **Elemento Visual no Slide:** Diagrama do fluxo desacoplado Treino vs. Teste.
- **Fala sugerida:**
  > "Isso nos leva à explicação teórica central do artigo: por que desacoplar o CAM entre treino e teste? Durante o TREINAMENTO, o mapa de ativação serve apenas para achar os CENTROS dos 6 patches de $256 \times 256$ pixels. O XGrad-CAM é perfeito para o treino porque seus axiomas concentram energia no centro verdadeiro da massa e ignoram o parênquima mamário denso. Já no TESTE, precisamos que o mapa térmico cubra pelo menos 30% da área anotada pelo médico ($\text{IoU} \ge 0{,}3$). O XGrad-CAM no teste gera caixas pequenas demais ($\text{TPR} = 0{,}60$), enquanto o Grad-CAM++ expande as bordas até os limites reais do tumor ($\text{TPR} = 0{,}70$). E por que não treinar direto com Grad-CAM++? Porque derivadas de 2ª e 3ª ordem no início do treino, quando os pesos ainda estão aleatórios, são numericamente instáveis e enviam patches de ruído para a rede local! Passo agora a palavra ao Marcos para apresentar os experimentos e resultados."

---

## Parte 3 — Ambiente Experimental, Resultados Comparativos e Conclusão (Marcos Willian — Slides 14 a 23)

### Slide 14 — Divisor Parte 3: Base VinDr-Mammo, Resultados e Conclusão (`Pág. 14/23`)
- **Fala sugerida:**
  > "Obrigado, Hermeson. Nesta terceira parte, apresentarei o protocolo experimental na base VinDr-Mammo, nossa implementação em PyTorch, a análise comparativa das Tabelas 1 e 2 e da Figura 4 do artigo, a auditoria matemática que realizamos sobre a Tabela 1 e as conclusões do estudo."

### Slide 15 — 11. Base de Dados VinDr-Mammo e Pré-Processamento (Figura 3) (`Pág. 15/23`)
- **Elemento Visual no Slide:** Print real da **Figura 3** do artigo original (*Projeções MLO-D, CC-D, CC-E e MLO-E da VinDr-Mammo*).
- **Fala sugerida:**
  > "Os experimentos foram conduzidos na base pública VinDr-Mammo (Nguyen et al., 2022), composta por 5.000 exames mamográficos de 4 projeções (20.000 imagens DICOM), anotados por consenso de três radiologistas. A Figura 3 do artigo ao lado ilustra as 4 vistas padrão de um exame: Médio-Lateral Oblíqua Direita e Esquerda (MLO-D/E) e Crânio-Caudal Direita e Esquerda (CC-D/E). Seguindo o recorte balanceado do artigo entre imagens Normais (BI-RADS 1) e imagens com Massa, utilizam-se 2.252 imagens no treino (1.126 de cada classe) e 548 imagens no teste (274 de cada classe), redimensionadas para $2944 \times 1920$ pixels com flip horizontal, random crop e normalização."

### Slide 16 — 12. Implementação PyTorch e Protocolo WSOD ($\text{IoU} \ge 0{,}3$) (`Pág. 16/23`)
- **Elemento Visual no Slide:** Saída real gerada pelo nosso pipeline PyTorch (`visual_gradcampp_wsod.png`).
- **Fala sugerida:**
  > "Em nossa implementação em PyTorch 2.x, reproduzimos fielmente a arquitetura GMIC e os 5 extratores CAM. Para viabilizar o treinamento de imagens de $2944 \times 1920$ pixels em GPUs de 8 GB de VRAM mantendo o batch efetivo igual a 6 do artigo, implementamos Precisão Mista Automática (AMP FP16) combinada com Acumulação de Gradientes em 6 passos. Na inferência WSOD, como mostra a saída real do nosso código ao lado, o mapa de ativação $92 \times 60$ sofre interpolação bilinear de volta para $2944 \times 1920$, normalização Min-Max, binarização por limiar $\tau = 0{,}25$ e extração de componentes conexos via OpenCV. Uma caixa predita (tracejada vermelha) é contabilizada como Verdadeiro Positivo (TP) se atingir $\text{IoU} \ge 0{,}3$ com a caixa do especialista (verde); caso contrário, incrementa o FPPI."

### Slide 17 — 13. Resultados de Classificação Global: Normal vs. Massa (Tabela 1) (`Pág. 17/23`)
- **Elemento Visual no Slide:** Print real da **Tabela 1** do artigo original.
- **Fala sugerida:**
  > "Avaliando primeiramente a classificação binária global no ramo de fusão ($\hat{y}_{\text{fusao}}$), a Tabela 1 do artigo abaixo mostra que o modelo GMIC atinge 80,12% de Acurácia, 87,22% de Área sob a Curva ROC (AUC) e 71,88% de Taxa de Verdadeiros Positivos (TPR / Sensibilidade). Contudo, ao auditarmos a quarta coluna da Tabela 1 — impressa no artigo como 'FNR = 88,52%' — detectamos uma inconsistência matemática importante, que detalhamos no próximo slide."

### Slide 18 — 14. Auditoria Crítica: Errata Matemática na Tabela 1 ($\text{FNR}$ vs. $\text{TNR}$) (`Pág. 18/23`)
- **Elemento Visual no Slide:** Print real da **Tabela 1** do artigo original com demonstração algébrica.
- **Fala sugerida:**
  > "Por definição estatística, a Taxa de Falsos Negativos ($\text{FNR}$) e a Taxa de Verdadeiros Positivos ($\text{TPR}$) são eventos complementares na classe positiva: $\text{FNR} + \text{TPR} = 100\%$. Portanto, se $\text{TPR} = 71{,}88\%$, o $\text{FNR}$ verdadeiro é obrigatoriamente $100\% - 71{,}88\% = 28{,}12\%$, sendo matematicamente impossível coexistir um FNR de 88,52%. O que é então o número 88,52%? Como o conjunto de teste é perfeitamente balanceado (50% Massa e 50% Normal), a Acurácia global é a média aritmética exata entre Sensibilidade ($\text{TPR}$) e Especificidade ($\text{TNR}$): somando $71{,}88\%$ com $88{,}52\%$ e dividindo por 2, obtemos exatamente $80{,}20\% \approx 80{,}12\%$! Provamos assim que os autores calcularam a Especificidade ($\text{TNR} = 88{,}52\%$, acerto nas imagens Normais), mas grafaram equivocadamente o cabeçalho da coluna como FNR na Tabela 1."

### Slide 19 — 15. Resultados de Detecção WSOD: Matriz $\text{TPR}@\text{FPPI}$ (Tabela 2) (`Pág. 19/23`)
- **Elemento Visual no Slide:** Print real da **Tabela 2** do artigo original.
- **Fala sugerida:**
  > "Passando ao resultado central do artigo — a localização fracamente supervisionada de massas sob $\text{IoU} \ge 0{,}3$ — a Tabela 2 abaixo apresenta a matriz cruzada $3 \times 5$ (3 métodos no treino vs. 5 métodos no teste), medida por $\text{TPR}@\text{FPPI}$. Destacamos três achados fundamentais:
  > 1) O baseline GMIC original (treino CAM e teste CAM, 1ª linha/1ª coluna) atinge $0{,}69@1{,}55$, gerando mais de um falso positivo e meio por imagem.
  > 2) Na 2ª linha, treinar com Grad-CAM++ mostra-se severamente instável, colapsando a sensibilidade para $0{,}13@0{,}06$ quando avaliado com Grad-CAM ou XGrad-CAM.
  > 3) Na 3ª linha, a combinação desacoplada campeã — treino com XGrad-CAM e teste com Grad-CAM++ (em negrito na Tabela 2) — atinge **$0{,}70@0{,}88$**, superando o baseline em sensibilidade e reduzindo os falsos positivos por imagem em **43,2%**!"

### Slide 20 — 16. Comparação Visual Qualitativa dos 5 CAMs (Figura 4 do Artigo) (`Pág. 20/23`)
- **Elemento Visual no Slide:** Print real da **Figura 4** do artigo original.
- **Fala sugerida:**
  > "A Figura 4 do artigo ao lado comprova visualmente os números da Tabela 2 para o modelo treinado com XGrad-CAM: na coluna (a), o CAM tradicional espalha calor por uma região muito maior que a caixa verde do especialista; nas colunas (b) Grad-CAM e (d) XGrad-CAM, o mapa térmico fica concentrado apenas no núcleo central da lesão, gerando caixas vermelhas pequenas que falham no limiar $\text{IoU} \ge 0{,}3$; na coluna (e), o Layer-CAM fragmenta o tecido mamário em várias caixas falsas ($\text{FPPI} = 4{,}19$); já na coluna (c), o Grad-CAM++ preenche toda a anatomia da massa, fazendo a caixa vermelha predita aderir com precisão à anotação verde do radiologista."

### Slide 21 — 17. Síntese Quantitativa: Trade-off Clínico $\text{TPR} \times \text{FPPI}$ e Ablação (`Pág. 21/23`)
- **Elemento Visual no Slide:** Gráfico duplo FROC (`fig4_froc_tradeoff.png`).
- **Fala sugerida:**
  > "Neste gráfico de síntese que construímos a partir dos dados da Tabela 2, visualizamos à esquerda a fronteira de eficiência clínica ($\text{TPR} \times \text{FPPI}$): a combinação desacoplada $\text{GMIC(XGrad-CAM)}\to\text{Grad-CAM++}$ (estrela verde) é a única a entrar na Zona Clínica Ideal (menos de 1 alarme falso por imagem com $\text{TPR} \ge 0{,}70$). À direita, o gráfico de ablação mostra a queda progressiva do FPPI: de $1{,}55$ no baseline para $1{,}43$ e $1{,}05$ ao trocar apenas o teste, chegando a $0{,}88$ ($-43{,}2\%$) com o desacoplamento completo."

### Slide 22 — 18. Conclusões Gerais, Contribuições e Trabalhos Futuros (`Pág. 22/23`)
- **Fala sugerida:**
  > "Concluindo nosso trabalho: (1) Validamos experimentalmente a eficácia do desacoplamento entre o mapa seletivo de treino (XGrad-CAM) e o mapa expansivo de teste (Grad-CAM++) na arquitetura GMIC; (2) Confirmamos o ganho clínico expressivo na base VinDr-Mammo, com $\text{TPR} = 0{,}70$ e redução de 43,2% no FPPI ($1{,}55 \to 0{,}88$); (3) Entregamos uma implementação completa e auditada em PyTorch com suporte a GPUs de 8 GB via AMP FP16 e acumulação de gradientes, além de formalizarmos a errata matemática da Tabela 1 ($\text{TNR} = 88{,}52\%$); e (4) Como trabalhos futuros, destacamos a extensão para microcalcificações e calibração adaptativa do limiar $\tau$ por densidade mamária BI-RADS."

### Slide 23 — Encerramento (`Pág. 23/23`)
- **Fala sugerida:**
  > "Muito obrigado pela atenção! Estamos à disposição da banca e dos colegas para perguntas."
