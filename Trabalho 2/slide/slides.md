---
marp: true
theme: uncover
paginate: true
size: 16:9
backgroundColor: #090d16
color: #e2e8f0
header: "UFPI / CTT — Tópicos Especiais em Visão Computacional | Prof. Dr. José Denes Lima Araújo"
footer: "Grupo 4 — Seminário de Comparação Metodológica: CNN vs. Vision Transformers na Saúde"
style: |
  section {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    padding: 35px 55px;
    font-size: 19px;
    line-height: 1.45;
    background: radial-gradient(circle at 10% 10%, #131b2e 0%, #090d16 100%);
    color: #e2e8f0;
    text-align: left;
  }
  section.lead {
    text-align: center;
    background: radial-gradient(circle at 50% 30%, #1e1b4b 0%, #090d16 90%);
  }
  h1 {
    color: #38bdf8;
    font-size: 1.7em;
    margin-bottom: 0.2em;
    font-weight: 700;
    letter-spacing: -0.02em;
  }
  h2 {
    color: #818cf8;
    font-size: 1.25em;
    margin-top: 0.1em;
    margin-bottom: 0.4em;
    font-weight: 600;
  }
  h3 {
    color: #34d399;
    font-size: 1.0em;
    margin-top: 0.2em;
    margin-bottom: 0.2em;
  }
  p, li {
    font-size: 0.9em;
    color: #cbd5e1;
  }
  ul {
    margin-top: 0.3em;
    margin-bottom: 0.5em;
    padding-left: 1.2em;
  }
  li {
    margin-bottom: 0.3em;
  }
  strong {
    color: #f8fafc;
  }
  table {
    font-size: 0.68em;
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    background-color: #0f172a;
    border-radius: 6px;
    overflow: hidden;
  }
  th {
    background-color: #1e293b;
    color: #38bdf8;
    padding: 6px 9px;
    text-align: left;
    border: 1px solid #334155;
    font-weight: 600;
  }
  td {
    padding: 5px 9px;
    border: 1px solid #334155;
    color: #cbd5e1;
  }
  tr:nth-child(even) {
    background-color: #141e33;
  }
  code {
    background-color: #1e293b;
    color: #f472b6;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 0.85em;
  }
  pre {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 0.72em;
    line-height: 1.3;
    color: #94a3b8;
  }
  .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.7em;
    font-weight: 600;
    margin-right: 5px;
  }
  .badge-cyan { background: #0369a1; color: #e0f2fe; border: 1px solid #38bdf8; }
  .badge-purple { background: #5b21b6; color: #ede9fe; border: 1px solid #a78bfa; }
  .badge-green { background: #065f46; color: #d1fae5; border: 1px solid #34d399; }
  .badge-amber { background: #78350f; color: #fef3c7; border: 1px solid #f59e0b; }
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  .grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
  }
  .card {
    background-color: rgba(15, 23, 42, 0.7);
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 14px;
  }
  .card-highlight {
    background-color: rgba(30, 41, 59, 0.8);
    border: 1px solid #38bdf8;
    border-radius: 8px;
    padding: 10px 14px;
  }
  .card-purple {
    background-color: rgba(30, 27, 75, 0.7);
    border: 1px solid #818cf8;
    border-radius: 8px;
    padding: 10px 14px;
  }
  .stat-val {
    font-size: 1.4em;
    font-weight: 700;
    color: #38bdf8;
  }
  .stat-lbl {
    font-size: 0.75em;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->
# Análise Comparativa e Discussão Crítica de Visão Computacional Médica
## Convoluções Clássicas vs. Mecanismos de Atenção em Transformadores

<span class="badge badge-cyan">BRACIS 2023 (UFCSPA)</span>
<span class="badge badge-purple">SBC 2025 (PUC Minas / UFMG)</span>
<span class="badge badge-green">UFPI / CTT</span>

**Universidade Federal do Piauí — UFPI**  
Centro de Tecnologia — Departamento de Informática e Estatística  
Disciplina: Tópicos Especiais em Visão Computacional | **Prof. Dr. José Denes Lima Araújo**  
**Grupo 4:** Integrante 1 (Aluno 1) • Integrante 2 (Aluno 2) • Integrante 3 (Aluno 3)

<!-- notes:
[ALUNO 1] 00:00 - 01:00
Bom dia/boa tarde a todos. Sou o [Aluno 1] e, em conjunto com meus colegas [Aluno 2] e [Aluno 3], compomos o Grupo 4. Hoje apresentaremos nossa análise crítica comparativa sobre dois artigos científicos completos publicados nos anais da Sociedade Brasileira de Computação (SBC). O primeiro trabalho, do BRACIS 2023, propõe uma arquitetura convolucional customizada para diagnóstico de neoplasias cerebrais em ressonância magnética. O segundo trabalho, publicado em 2025 pela PUC Minas e UFMG, investiga o comportamento de Vision Transformers com técnicas dinâmicas de extração de patches na citopatologia do colo uterino. Ao longo de 35 minutos, desconstruiremos os dados, arquiteturas, resultados empíricos e confrontaremos a teoria de viés indutivo convolucional contra a autoatenção global.
-->

---

# Estrutura do Seminário e Cronograma de Apresentação
## Divisão Estratégica em Três Blocos Especializados (Meta: 34 a 36 Minutos)

<div class="grid-3">
  <div class="card-highlight">
    <span class="badge badge-cyan">Bloco 1 • 11:30 min</span>
    <h3>Aluno 1: Fundamentos & CNN</h3>
    <ul>
      <li>Desafios da IA na Saúde</li>
      <li>Artigo 1: UFCSPA (BRACIS 2023)</li>
      <li>Curadoria e Substituição Figshare</li>
      <li>CNN Adaptada e Dropout Progressivo</li>
      <li>K-Fold, 99% Acurácia e Grad-CAM</li>
    </ul>
  </div>
  <div class="card-purple">
    <span class="badge badge-purple">Bloco 2 • 11:30 min</span>
    <h3>Aluno 2: ViTs & Patches</h3>
    <ul>
      <li>Citologia Cervical (Bethesda)</li>
      <li>Artigo 2: PUC Minas / UFMG (2025)</li>
      <li>Dataset CRIC e Split por Paciente</li>
      <li>Autoatenção e Projeção Conv2D</li>
      <li>5 Métodos Dinâmicos e Tabela 2</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge badge-green">Bloco 3 • 11:30 min</span>
    <h3>Aluno 3: Crítica & Síntese</h3>
    <ul>
      <li>Causa-Raiz do Paradoxo do Grid</li>
      <li>Viés Indutivo vs. Data-Hunger</li>
      <li>Matriz Comparativa de 16 Eixos</li>
      <li>Auditoria de Leakage: Slice vs Paciente</li>
      <li>Árvore Decisória e Conclusões</li>
    </ul>
  </div>
</div>

<p style="text-align: center; margin-top: 15px; font-size: 0.8em; color: #94a3b8;">
<strong>Janela da Apresentação:</strong> Mínimo de 30 minutos | Máximo de 40 minutos | <strong>Arguição da Banca:</strong> 34:30 a 40:00
</p>

<!-- notes:
[ALUNO 1] 01:00 - 02:00
Para atender rigorosamente aos critérios de avaliação da UFPI, estruturamos nossa explanação em três blocos de aproximadamente 11 minutos e meio cada. No primeiro bloco, apresentarei o contexto clínico geral e a desconstrução completa do Artigo 1, cobrindo o problema dos tumores cerebrais, a auditoria na base de dados, a arquitetura convolucional proposta, os experimentos com 5-Fold Cross Validation e a explicabilidade via Grad-CAM. Em seguida, o colega [Aluno 2] assumirá para detalhar o Artigo 2, abordando o rastreamento citopatológico de colo uterino, os mecanismos do Vision Transformer, a partição anti-leakage por paciente e as 5 abordagens de patches dinâmicos. Por fim, o colega [Aluno 3] liderará a análise comparativa multidimensional, o debate teórico entre viés indutivo e fome de dados, a reflexão epistemológica sobre o resultado negativo e as conclusões finais, abrindo espaço para a sabatina do Prof. Dr. José Denes.
-->

---

# Desafios Singulares da Visão Computacional Médica
## A Fronteira entre Diagnóstico Automatizado e Segurança Clínica

<div class="grid-2">
  <div class="card">
    <h3>Restrições Críticas do Domínio Biomédico</h3>
    <ul>
      <li><strong>Escassez Extrema de Rótulos Confiáveis:</strong> Anotação médica exige tempo escasso de patologistas e radiologistas seniores.</li>
      <li><strong>Severo Desbalanceamento de Classes:</strong> Lesões malignas e raras (ex: carcinoma invasivo) representam frações minúsculas da amostra.</li>
      <li><strong>Custo Assimétrico do Erro:</strong> Falsos-negativos (não diagnosticar neoplasia letal) têm desfecho fatal para o paciente.</li>
      <li><strong>Mandato de Explicabilidade (XAI):</strong> Modelos "caixa-preta" são rejeitados por conselhos médicos e regulatórios (CFM/FDA).</li>
    </ul>
  </div>
  <div class="card">
    <h3>Duas Escalas Espaciais e Dois Paradigmas</h3>
    <table style="margin-top: 5px;">
      <tr><th>Dimensão</th><th>Macroestrutural (Artigo 1)</th><th>Microestrutural (Artigo 2)</th></tr>
      <tr><td><strong>Exame</strong></td><td>Ressonância Magnética (MRI)</td><td>Citopatologia (Papanicolau)</td></tr>
      <tr><td><strong>Alvo</strong></td><td>Massa tecidual encefálica (cm)</td><td>Atipia de núcleo celular (µm)</td></tr>
      <tr><td><strong>Entrada</strong></td><td>$64 \times 64$ fatias axiais</td><td>$224 \times 224$ (núcleos recortados)</td></tr>
      <tr><td><strong>Paradigma</strong></td><td><strong>CNN Customizada (AlexNet)</strong></td><td><strong>Vision Transformer (ViT)</strong></td></tr>
      <tr><td><strong>Abordagem</strong></td><td>Treinado do zero (Scratch)</td><td>Fine-Tuning (ImageNet-21k)</td></tr>
    </table>
  </div>
</div>

<!-- notes:
[ALUNO 1] 02:00 - 03:30
Diferente do processamento de imagens do mundo natural — como classificar cães, gatos ou veículos —, a Visão Computacional Médica opera sob restrições severas. A primeira é a escassez de dados rotulados por especialistas, pois cada máscara ou diagnóstico demanda horas de médicos especialistas. A segunda é o desbalanceamento estatístico natural: em exames de rotina, a imensa maioria dos casos é benigna ou normal, enquanto patologias críticas constituem frações ínfimas da base. Além disso, existe o custo assimétrico do erro: cometer um falso-positivo gera ansiedade e exames complementares, mas cometer um falso-negativo em oncologia atrasa o tratamento e reduz drasticamente a chance de sobrevida do paciente. Por fim, a inteligência artificial médica não pode ser uma caixa-preta; ela precisa justificar visualmente a decisão. Ao longo deste seminário, confrontaremos duas escalas: a macroestrutura encefálica via CNN do Artigo 1 e a microestrutura celular via Vision Transformers do Artigo 2.
-->

---

# Artigo 1 (UFCSPA) — Contexto Clínico e Classes Diagnósticas
## *An Approach in Brain Tumor Classification: Development of a New CNN Model* (BRACIS 2023)

<div class="grid-2">
  <div class="card">
    <h3>As 4 Classes Diagnósticas de Tumores Cerebrais</h3>
    <ul>
      <li><strong>Glioma (Classe 0):</strong> Neoplasia de células gliais. Altamente infiltrativa, margens difusas e malignidade agressiva (ex: glioblastoma). Exige intervenção cirúrgica imediata.</li>
      <li><strong>Meningioma (Classe 1):</strong> Origina-se nas meninges durais. Tipicamente benigno, circunscrito, de crescimento lento, apresentando "cauda dural".</li>
      <li><strong>No Tumor / Normal (Classe 2):</strong> Fatias encefálicas sem evidência de massa expansiva. Essencial para validação de triagem sem falso alarme.</li>
      <li><strong>Pituitary / Adenoma Hipofisário (Classe 3):</strong> Lesão na sela túrcica. Causa disfunção endócrina e compressão do quiasma óptico.</li>
    </ul>
  </div>
  <div class="card-highlight">
    <h3>Metadados e Objetivos dos Pesquisadores</h3>
    <p><strong>Autores:</strong> Caio dos Santos Felipe, Thatiane Alves Pianoschi Alva, Ana Trindade Winck, Carla Diniz Lopes Becker (UFCSPA - Porto Alegre, RS).</p>
    <p><strong>Problema Central:</strong> Desenvolver um modelo convolucional leve, com baixo custo computacional e alta explicabilidade visual (Grad-CAM), capaz de rodar em equipamentos hospitalares modestos sem depender de clusters de alta performance.</p>
    <p><strong>Diferencial Metodológico:</strong> Auditoria visual preventiva para expurgar rótulos ruidosos de benchmarks públicos abertos.</p>
  </div>
</div>

<!-- notes:
[ALUNO 1] 03:30 - 05:00
Iniciando a análise profunda do Artigo 1, publicado no BRACIS 2023 por pesquisadores da Universidade Federal de Ciências da Saúde de Porto Alegre, o problema consiste no diagnóstico diferencial de quatro condições em exames de ressonância magnética cerebral. O Glioma é uma neoplasia com origem nas células gliais, altamente infiltrativa e maligna, onde o tempo de intervenção define o prognóstico. O Meningioma, por sua vez, origina-se nas membranas meningóeas, sendo na maioria dos casos benigno e de margem bem delimitada. A classe "Sem Tumor" valida a triagem automática para descartar exames normais, e os tumores de Hipófise ocorrem na base encefálica, gerando alterações hormonais e compressão visual. A meta da UFCSPA foi construir um modelo de aprendizado profundo leve, rápido e parcimonioso, que pudesse operar em ambientes clínicos com computadores convencionais e entregar confiabilidade diagnóstica irretocável.
-->

---

# Curadoria Sanitária da Base: A Descoberta de Label Noise
## Auditoria Crítica do Kaggle e Substituição Cirúrgica com o Figshare

<div class="grid-2">
  <div class="card">
    <span class="badge badge-amber">Problema Detectado</span>
    <h3>Contaminação no Benchmark Kaggle</h3>
    <ul>
      <li><strong>Base Original:</strong> <em>Brain Tumor MRI Dataset</em> (7.023 imagens curadas por Nickparvar / Bhuvaji).</li>
      <li><strong>Vício Sanitário Encontrado:</strong> Durante a inspeção visual preliminar, os autores detectaram que a pasta de <strong>Gliomas</strong> continha imagens erroneamente rotuladas (incluindo meningiomas evidentes e crânios sadios).</li>
      <li><strong>Risco Clínico:</strong> Treinar sobre rótulos corrompidos (<em>label noise</em>) induziria a rede a aprender correlações espúrias e gerar predições catastróficas.</li>
    </ul>
  </div>
  <div class="card-highlight">
    <span class="badge badge-green">Solução Metodológica</span>
    <h3>Higienização Cirúrgica com Figshare</h3>
    <ul>
      <li>Os autores expurgaram as amostras ruidosas e as substituíram por instâncias auditadas do repositório <strong>Figshare</strong> (Cheng et al.).</li>
      <li><strong>Conjunto de Treinamento/Validação Ajustado (5.531 fatias):</strong>
        <ul>
          <li>Glioma: 1.126 (20,4%) | Meningioma: 1.339 (24,3%)</li>
          <li>No Tumor: 1.595 (28,9%) | Pituitary: 1.457 (26,4%)</li>
        </ul>
      </li>
      <li><strong>Conjunto de Teste Cego Independente:</strong> 1.297 a 1.311 imagens isoladas estritamente antes do treino.</li>
    </ul>
  </div>
</div>

<p style="margin-top: 10px; font-size: 0.82em; color: #38bdf8;">
<strong>Lição de Data-Centric AI:</strong> Antes de calibrar hiperparâmetros ou aumentar redes, a prioridade máxima é garantir a fidedignidade clínica dos dados de entrada.
</p>

<!-- notes:
[ALUNO 1] 05:00 - 06:30
Um dos pontos mais notáveis e maduros do trabalho da UFCSPA foi o rigor na curadoria dos dados. O dataset público mais utilizado no Kaggle para tumores cerebrais possui mais de 7 mil imagens. Contudo, ao realizarem uma auditoria exploratória visual criteriosa, os pesquisadores descobriram que a pasta da classe Glioma estava severamente contaminada com rótulos incorretos — havia imagens de meningiomas e até cortes normais catalogados como gliomas! Em vez de ignorar o ruído e deixar a rede memorizar erros, os autores agiram sob a filosofia de Data-Centric AI: expurgaram cirurgicamente as amostras corrompidas e as substituíram por instâncias validadas por radiologistas do dataset Figshare. A base de trabalho consolidou-se em 5.531 imagens de treino e 1.297 fatias mantidas totalmente cegas no teste independente.
-->

---

# Pré-Processamento, Ponderação e Blindagem Anti-Leakage
## Preparação dos Tensores e Mitigação do Desbalanceamento

<div class="grid-2">
  <div class="card">
    <h3>Pipeline de Transformação Matemática</h3>
    <ul>
      <li><strong>Redimensionamento Espacial ($64 \times 64$ pixels):</strong> Compressão agressiva para reduzir a contagem de parâmetros treináveis e permitir convergência célere.</li>
      <li><strong>Normalização Min-Max $[0.0, 1.0]$:</strong>
        $$I_{\text{norm}}(x, y) = \frac{I(x, y)}{255.0}$$
        Linearização dos gradientes e aceleração da descida estocástica.</li>
      <li><strong>Shuffling Contínuo por Época:</strong> Reembaralhamento dos lotes a cada passagem para evitar vícios na ordem estocástica dos gradientes.</li>
    </ul>
  </div>
  <div class="card">
    <h3>Pesos de Classe na Perda (Class Weights)</h3>
    <p>Para compensar a disparidade de classes (Glioma com 20,4% vs No Tumor com 28,9%) sem fabricar artefatos sintéticos:</p>
    <table>
      <tr><th>Classe Diagnóstica</th><th>Fração Original</th><th>Peso Injetado ($w_c$)</th></tr>
      <tr><td><strong>Glioma</strong> (minoritária)</td><td>20,41%</td><td><strong>1.21</strong></td></tr>
      <tr><td><strong>Meningioma</strong></td><td>24,27%</td><td><strong>1.03</strong></td></tr>
      <tr><td><strong>Pituitary</strong></td><td>26,41%</td><td><strong>0.94</strong></td></tr>
      <tr><td><strong>No Tumor</strong> (majoritária)</td><td>28,91%</td><td><strong>0.86</strong></td></tr>
    </table>
    <p style="font-size: 0.75em; color: #94a3b8;">
    <strong>Garantia Anti-Leakage:</strong> Partição de teste isolada antes do cálculo de pesos e da normalização.
    </p>
  </div>
</div>

<!-- notes:
[ALUNO 1] 06:30 - 07:45
No pré-processamento, as imagens foram redimensionadas para matrizes compactas de 64 por 64 pixels e normalizadas dividindo-se por 255, estabelecendo valores entre 0.0 e 1.0. Para lidar com o desbalanceamento intrínseco — onde a classe Glioma possuía apenas 20% das fatias contra 29% da classe Sem Tumor —, os autores evitaram técnicas cegas de geração sintética e optaram por ponderar a função de perda. Injetaram pesos inversamente proporcionais: o erro em um glioma foi penalizado com peso 1.21, enquanto o erro em um exame normal teve peso atenuado para 0.86. Vale frisar a blindagem metodológica: a partição entre treino e teste ocorreu estritamente antes do pré-processamento, impedindo que estatísticas globais vazassem para o modelo durante o treinamento.
-->

---

# Arquitetura da Rede Convolucional Proposta
## Estrutura Inspirada na AlexNet com Perfil de Regularização Progressiva

<div class="grid-2">
  <div class="card">
    <h3>Diagrama de Fluxo e Blocos Convolucionais</h3>
    <pre>
[Entrada: 64x64x3] Normalizada
       │
       ▼
[Bloco 1] Conv2D (16 filtros 3x3) ➔ ReLU ➔ MaxPool (2x2) ➔ Dropout (20%)
       │  Mapa: 31x31x16
       ▼
[Bloco 2] Conv2D (32 filtros 3x3) ➔ ReLU ➔ MaxPool (2x2) ➔ Dropout (25%)
       │  Mapa: 14x14x32
       ▼
[Bloco 3] Conv2D (64 filtros 3x3) ➔ ReLU ➔ MaxPool (2x2) ➔ Dropout (30%)
       │  Mapa: 6x6x64
       ▼
[Camadas Densas]
  • Flatten: 6 x 6 x 64 = 2.304 neurônios
  • Dense 1: 32 neurônios + ReLU + Regularização L2
  • Dense 2 (Saída): 4 neurônios + Ativação Softmax
    </pre>
  </div>
  <div class="card-highlight">
    <h3>Mecanismo de Regularização Progressiva</h3>
    <ul>
      <li><strong>Filtros Convolucionais em Escala ($16 \to 32 \to 64$):</strong> Captura progressiva de bordas primitivas, texturas teciduais e padrões morfológicos complexos de lesão.</li>
      <li><strong>Dropout Escalonado ($20\% \to 25\% \to 30\%$):</strong>
        <ul>
          <li>Camadas iniciais: descarte baixo (20%) para preservar feições anatômicas primárias.</li>
          <li>Camadas profundas: descarte severo (30%) para impedir coadaptação espúria de neurônios.</li>
        </ul>
      </li>
      <li><strong>Penalização por Decaimento de Pesos $L_2$:</strong> Restringe a magnitude dos vetores na camada densa, prevenindo sobreajuste sobre fatias repetidas.</li>
    </ul>
  </div>
</div>

<!-- notes:
[ALUNO 1] 07:45 - 09:00
A arquitetura convolucional foi desenhada sob medida para aliar eficiência e regularização extrema. Inspirada nos princípios da AlexNet, ela emprega três blocos convolucionais sucessivos com kernels 3 por 3 e contagem crescente de filtros: 16, 32 e 64. Notem a elegância da estratégia de regularização: o Dropout é escalonado progressivamente. No primeiro bloco convolucional, o dropout é de 20%, garantindo que bordas e contrastes básicos não sejam destruídos; no segundo bloco sobe para 25%; e no terceiro atinge 30%, quebrando correlações complexas de alto nível. Na transição para o classificador denso, após o achatamento vetorial, uma camada intermediária de apenas 32 neurônios conta com penalização de norma L2, seguida pela camada final de 4 saídas com ativação Softmax para fornecer a probabilidade de cada uma das neoplasias.
-->

---

# Pipeline Experimental: K-Fold e Callbacks Inteligentes
## Protocolo Rigoroso de Otimização e Prevenção de Sobreajuste

<div class="grid-2">
  <div class="card">
    <h3>5-Fold Cross Validation Estratificado</h3>
    <ul>
      <li>O conjunto de 5.531 imagens foi particionado em <strong>5 dobras disjuntas</strong> mantendo a proporção de classes.</li>
      <li>Em cada iteração: 4 dobras (80%) para calibrar pesos sinápticos e 1 dobra (20%) para validação interna cega.</li>
      <li>Convergência e métricas reportadas refletem o comportamento médio robusto, livre da flutuação de um split aleatório conveniente.</li>
      <li><strong>Otimizador:</strong> Adam ($\beta_1=0.9, \beta_2=0.999$) com tamanho de lote de 32 imagens e teto de 60 épocas.</li>
    </ul>
  </div>
  <div class="card">
    <h3>Trindade de Callbacks Inteligentes</h3>
    <ul>
      <li><strong>Early Stopping (Paciência = 18 épocas):</strong> Monitoramento constante da perda de validação; encerra o treinamento preventivamente caso não ocorra melhora em 18 épocas consecutivas.</li>
      <li><strong>ReduceLROnPlateau (Fator 0.2):</strong> Se a perda de validação estagnar por 5 épocas consecutivas, a taxa de aprendizado é contraída em 80% ($\text{LR} \leftarrow \text{LR} \times 0.2$), permitindo ajustes milimétricos no gradiente.</li>
      <li><strong>Model Checkpoint:</strong> Gravação contínua no disco estritamente do melhor estado de pesos da história da rede.</li>
    </ul>
  </div>
</div>

<!-- notes:
[ALUNO 1] 09:00 - 10:15
O protocolo de treinamento foi estruturado com validação cruzada K-Fold de 5 dobras sobre as 5.531 imagens. Em cada uma das 5 rodadas, 80% dos dados treinaram a rede e 20% serviram como validação independente. A convergência foi governada pelo otimizador Adam e por três callbacks inteligentes essenciais: um Early Stopping com tolerância de 18 épocas para abortar o treino em caso de superajuste; um agendador ReduceLROnPlateau que reduzia o passo de aprendizado em um fator de 0.2 caso a perda de validação estagnasse por 5 épocas; e um Model Checkpoint que salvava no disco unicamente o conjunto de pesos sinápticos que alcançou a menor perda mínima histórica.
-->

---

# Resultados Quantitativos: Acurácia Global de 99%
## Desempenho Excepcional no Teste Cego com 1.311 Imagens

<div class="grid-2">
  <div class="card">
    <h3>Relatório de Classificação por Categoria</h3>
    <table>
      <tr><th>Classe Diagnóstica</th><th>Precisão</th><th>Revocação</th><th>F1-Score</th><th>Suporte</th></tr>
      <tr style="background-color: #1e3a5f;"><td><strong>Glioma</strong> (Neoplasia Letal)</td><td><strong>1,00</strong></td><td><strong>1,00</strong></td><td><strong>1,00</strong></td><td>286</td></tr>
      <tr><td><strong>Meningioma</strong></td><td>0,98</td><td>0,97</td><td>0,98</td><td>306</td></tr>
      <tr><td><strong>No Tumor</strong> (Triagem Normal)</td><td>0,99</td><td>1,00</td><td>0,99</td><td>405</td></tr>
      <tr><td><strong>Pituitary</strong> (Adenoma)</td><td>0,99</td><td>0,99</td><td>0,99</td><td>300</td></tr>
      <tr style="font-weight: bold; background-color: #0c4a6e;"><td>Acurácia Global</td><td colspan="2">Consolidada no Teste</td><td><strong>0,99 (99,0%)</strong></td><td>1.311</td></tr>
      <tr><td>Média Macro (Macro Avg)</td><td>0,99</td><td>0,99</td><td>0,99</td><td>1.311</td></tr>
      <tr><td>Média Ponderada (Weighted)</td><td>0,99</td><td>0,99</td><td>0,99</td><td>1.311</td></tr>
    </table>
  </div>
  <div class="card-highlight">
    <span class="badge badge-green">Impacto Médico Decisivo</span>
    <h3>Zero Falso-Negativo para Glioma</h3>
    <ul>
      <li><strong>Revocação de 100% (1,00) em Glioma:</strong> O modelo identificou todas as 286 amostras da neoplasia mais letal sem cometer um único erro falso-negativo.</li>
      <li><strong>Meningioma e Hipófise com F1 $\ge 0,98$:</strong> Quase nula confusão entre massas extra-axiais e tumores selares.</li>
      <li><strong>Curvas ROC/AUC Unitárias:</strong> Área sob a curva discriminativa ROC próxima de 1,0 em todos os limiares de sensibilidade.</li>
    </ul>
  </div>
</div>

<!-- notes:
[ALUNO 1] 10:15 - 11:30
Na avaliação final sobre o conjunto de teste cego com 1.311 imagens nunca vistas durante o treinamento, o modelo atingiu acurácia global de 99,0%. O achado de maior envergadura clínica reside na classe Glioma: a rede obteve precisão de 1,00, revocação de 1,00 e F1-score de 1,00 em todos os 286 casos testados. Em termos médicos, isso significa que o algoritmo não produziu um único falso-negativo para o tumor mais maligno e agressivo do sistema nervoso central. A classe Meningioma obteve F1 de 0,98, Hipófise 0,99 e Sem Tumor 0,99. A área sob a curva ROC situou-se praticamente colada na unidade para todas as categorias diagnósticas.
-->

---

# Explicabilidade Clínica (XAI) com Grad-CAM
## Localização Anatômica Real e Validação Externa Inédita

<div class="grid-2">
  <div class="card">
    <h3>Fundamento Matemático do Grad-CAM</h3>
    <p>Cálculo dos gradientes da classe predita $y^c$ sobre a terceira camada convolucional $A^k$ via Global Average Pooling:</p>
    $$\alpha_k^c = \frac{1}{Z} \sum_{i} \sum_{j} \frac{\partial y^c}{\partial A_{i,j}^k}$$
    <p>Combinação retificada retendo apenas sinais positivos:</p>
    $$L_{\text{Grad-CAM}}^c = \text{ReLU}\left(\sum_{k} \alpha_k^c \cdot A^k\right)$$
    <p style="font-size: 0.78em; color: #94a3b8;">
    O mapa térmico resultante é interpolado bilinearmente e sobreposto à ressonância magnética em escala de calor pseudo-colorida.
    </p>
  </div>
  <div class="card-highlight">
    <span class="badge badge-cyan">Prova de Generalização</span>
    <h3>Auditoria em Base Externa (Bhuvaji et al.)</h3>
    <ul>
      <li><strong>Inspeção Visual:</strong> O calor térmico concentra-se com precisão sobre o núcleo da massa tumoral e bordas de edema.</li>
      <li><strong>Ausência de Vício Periférico:</strong> Nenhum mapa focou em ossos do crânio, texto radiológico ou fundo escuro.</li>
      <li><strong>Teste Cego Externo:</strong> Os autores testaram o Grad-CAM em imagens de uma base de ressonância externa completamente inédita; o modelo manteve o foco correto na lesão, descartando memorização espúria.</li>
    </ul>
  </div>
</div>

<p style="text-align: right; margin-top: 15px; font-size: 0.82em; color: #818cf8;">
<em>Passo agora a palavra ao colega <strong>[Aluno 2]</strong> para a análise do Artigo 2 e dos Vision Transformers.</em>
</p>

<!-- notes:
[ALUNO 1] 11:30 - 12:30
Para garantir que a rede não estava decidindo com base em ruídos de fundo, texto do aparelho ou ossos cranianos, aplicou-se o Grad-CAM sobre o último bloco convolucional. Os mapas de ativação provam que a energia dos gradientes converge com precisão cirúrgica sobre a massa tumoral e o edema perilesional. Mais admirável ainda: os pesquisadores realizaram uma validação externa cega em exames de ressonância de outro repositório público (Bhuvaji et al.) nunca visto pela rede, comprovando que a explicabilidade generalizou para outros equipamentos e centros de imagem.
Encerro aqui o Bloco 1 e passo a palavra ao colega [Aluno 2], que nos conduzirá pela análise do Artigo 2, focado em citopatologia cervical e Vision Transformers com patches dinâmicos.
-->

---

# Artigo 2 (PUC Minas / UFMG) — Citologia Cervical e Bethesda
## *Vision Transformers com Patches Dinâmicos para a Análise de Lâminas Histológicas* (SBC 2025)

<div class="grid-2">
  <div class="card">
    <h3>O Desafio Clínico do Câncer de Colo Uterino</h3>
    <ul>
      <li><strong>Epidemiologia:</strong> Quarta neoplasia mais letal entre mulheres no mundo; rastreado pelo exame citopatológico preventivo de <strong>Papanicolau</strong>.</li>
      <li><strong>Gargalo Humano:</strong> Análise microscópica manual de centenas de milhares de células em lâmina única gera severa fadiga visual e variabilidade entre citotécnicos.</li>
      <li><strong>Objetivo do Estudo:</strong> Automatizar a triagem celular classificando núcleos isolados através de <strong>Vision Transformers (ViT)</strong> e propondo <strong>5 métodos dinâmicos de extração de patches</strong>.</li>
    </ul>
  </div>
  <div class="card-purple">
    <h3>As 6 Classes do Sistema Bethesda</h3>
    <table style="font-size: 0.65em;">
      <tr><th>Classe</th><th>Significado Clínico</th><th>Gravidade</th></tr>
      <tr><td><strong>NFIL</strong></td><td>Negativo para Lesão Intraepitelial (Sadio)</td><td>Triagem normal</td></tr>
      <tr><td><strong>ASC-US</strong></td><td>Células Escamosas Atípicas de Sig. Indeterminado</td><td>Atipia leve (HPV)</td></tr>
      <tr><td><strong>ASC-H</strong></td><td>Células Atípicas — não exclui Alto Grau</td><td>Suspeita alta</td></tr>
      <tr><td><strong>LSIL</strong></td><td>Lesão Intraepitelial de Baixo Grau</td><td>Pré-maligna leve</td></tr>
      <tr><td><strong>HSIL</strong></td><td>Lesão Intraepitelial de Alto Grau</td><td>Pré-maligna severa</td></tr>
      <tr><td><strong>SCC</strong></td><td>Carcinoma Escamoso Invasivo</td><td>Câncer invasor</td></tr>
    </table>
  </div>
</div>

<!-- notes:
[ALUNO 2] 12:30 - 14:00
Obrigado, [Aluno 1]. Iniciando o Bloco 2 com a análise do Artigo 2, publicado em 2025 pelos pesquisadores Vinícius Giovanini e Alexei Machado, da PUC Minas e da Faculdade de Medicina da UFMG. O cenário clínico é o câncer de colo de útero, diagnosticado via esfregaço citopatológico de Papanicolau. O problema foi modelado em seis categorias citológicas do Sistema Bethesda: desde células completamente sadias (NFIL), passando por atipias indeterminadas (ASC-US e ASC-H), lesões pré-neoplásicas de baixo e alto grau (LSIL e HSIL), até o temido Carcinoma Escamoso Invasor (SCC). O escrutínio manual de lâminas é extenuante e suscetível ao cansaço dos patologistas. Os autores investigaram a aplicação de Vision Transformers e questionaram a forma padrão com que os patches da imagem são alimentados no modelo.
-->

---

# Dataset CRIC e Blindagem Anti-Leakage por Paciente
## O Padrão-Ouro de Validação Metodológica em Citopatologia

<div class="grid-2">
  <div class="card">
    <span class="badge badge-green">Estratificação por Paciente</span>
    <h3>Particionamento Estrito (Patient-Level Split)</h3>
    <ul>
      <li><strong>Base CRIC (UFOP):</strong> 400 imagens microscópicas com <strong>11.534 núcleos celulares</strong> anotados e recortados ($90 \times 90 \to 224 \times 224$).</li>
      <li><strong>Divisão Estritamente por Paciente:</strong>
        <ul>
          <li>Treinamento: <strong>64%</strong> das pacientes</li>
          <li>Validação: <strong>20%</strong> das pacientes</li>
          <li>Teste Independente: <strong>16%</strong> das pacientes</li>
        </ul>
      </li>
      <li><strong>Blindagem Anti-Leakage Perfeita:</strong> Amostras de uma mesma paciente jamais transitam entre treino e teste.</li>
      <li>Elimina o viés de o modelo memorizar pH, corante ou espessura da lâmina de uma paciente específica.</li>
    </ul>
  </div>
  <div class="card">
    <h3>Distribuição Original Crítica</h3>
    <p>O desbalanceamento na rotina clínica é brutal:</p>
    <table style="font-size: 0.64em;">
      <tr><th>Classe</th><th>Treino</th><th>Validação</th><th>Teste</th><th>Total</th></tr>
      <tr><td>NFIL (Normal)</td><td>4.339</td><td>1.356</td><td>1.084</td><td><strong>6.779</strong></td></tr>
      <tr><td>HSIL (Alto Grau)</td><td>1.090</td><td>341</td><td>272</td><td><strong>1.703</strong></td></tr>
      <tr><td>LSIL (Baixo Grau)</td><td>871</td><td>272</td><td>217</td><td><strong>1.360</strong></td></tr>
      <tr><td>ASC-H (Atípico)</td><td>592</td><td>185</td><td>148</td><td><strong>925</strong></td></tr>
      <tr><td>ASC-US (Atípico)</td><td>388</td><td>122</td><td>96</td><td><strong>606</strong></td></tr>
      <tr style="color: #f472b6;"><td>SCC (Carcinoma)</td><td>103</td><td>33</td><td>25</td><td><strong>161</strong></td></tr>
    </table>
    <p style="font-size: 0.72em; color: #94a3b8;">Apenas 161 núcleos de carcinoma em toda a base de 11.534 amostras!</p>
  </div>
</div>

<!-- notes:
[ALUNO 2] 14:00 - 15:15
Os autores utilizaram a base de dados pública CRIC, desenvolvida pela Universidade Federal de Ouro Preto, contendo 11.534 núcleos celulares segmentados a partir de 400 lâminas reais. Aqui reside um dos maiores méritos metodológicos do Artigo 2: o particionamento dos subconjuntos foi feito estritamente por paciente — 64% das pacientes para treino, 20% para validação e 16% para teste. Nenhuma célula de uma paciente de teste apareceu no conjunto de treino. Isso é vital na patologia digital: cada lâmina possui variações microscópicas de pH, espessura e tonalidade de hematoxilina-eosina. Se o split fosse aleatório por células, o modelo memorizaria a tonalidade da lâmina de Maria e não as atipias do núcleo. Notem também a severidade do desbalanceamento original: havia mais de 6.700 células normais contra apenas 161 células de carcinoma invasivo.
-->

---

# Estratégia Híbrida de Balanceamento de Dados
## Calibração em 1.000 Amostras por Classe no Conjunto de Treino

<div class="grid-2">
  <div class="card">
    <span class="badge badge-purple">Técnica Híbrida de Balanceamento</span>
    <h3>Oversampling e Undersampling Combinados</h3>
    <ul>
      <li>Para impedir que o Transformer colapsasse prevendo apenas a classe NFIL, fixou-se o teto de <strong>1.000 amostras exatas por classe no treino</strong> (total: 6.000 imagens).</li>
      <li><strong>Oversampling com Albumentations:</strong>
        <ul>
          <li>Aplicado às classes raras (SCC de 103 $\to$ 1.000; ASC-US de 388 $\to$ 1.000; ASC-H de 592 $\to$ 1.000; LSIL de 871 $\to$ 1.000).</li>
          <li>Transformações afins seguras: rotações angulares, reflexões horizontais/verticais (flips) e ajustes de enquadramento.</li>
        </ul>
      </li>
      <li><strong>Undersampling Aleatório:</strong>
        <ul>
          <li>Redução de NFIL de 4.339 $\to$ 1.000 e HSIL de 1.090 $\to$ 1.000.</li>
        </ul>
      </li>
    </ul>
  </div>
  <div class="card">
    <h3>Tabela de Distribuição Pré e Pós-Balanceamento</h3>
    <table style="font-size: 0.65em;">
      <tr><th>Classe</th><th>Treino Antes</th><th>Treino Balanceado</th><th>Validação</th><th>Teste</th></tr>
      <tr><td>ASC-H</td><td>592</td><td><strong>1.000</strong> (Oversampling)</td><td>185</td><td>148</td></tr>
      <tr><td>ASC-US</td><td>388</td><td><strong>1.000</strong> (Oversampling)</td><td>122</td><td>96</td></tr>
      <tr><td>HSIL</td><td>1.090</td><td><strong>1.000</strong> (Undersampling)</td><td>341</td><td>272</td></tr>
      <tr><td>LSIL</td><td>871</td><td><strong>1.000</strong> (Oversampling)</td><td>272</td><td>217</td></tr>
      <tr><td>NFIL</td><td>4.339</td><td><strong>1.000</strong> (Undersampling)</td><td>1.356</td><td>1.084</td></tr>
      <tr style="color: #38bdf8;"><td>SCC</td><td>103</td><td><strong>1.000</strong> (Oversampling)</td><td>33</td><td>25</td></tr>
      <tr style="font-weight: bold; background-color: #1e293b;"><td>Total</td><td>7.383</td><td><strong>6.000</strong></td><td>2.309</td><td>1.842</td></tr>
    </table>
    <p style="font-size: 0.72em; color: #94a3b8;">
    Validação e teste permaneceram intactos com suas distribuições clínicas naturais!
    </p>
  </div>
</div>

<!-- notes:
[ALUNO 2] 15:15 - 16:30
Para equilibrar a capacidade de aprendizado do modelo sem distorcer os dados de avaliação, os autores calibraram o conjunto de treino exatamente em 1.000 amostras por classe, totalizando 6.000 imagens balanceadas. As classes raras — em especial o carcinoma SCC, que contava com apenas 103 instâncias — foram multiplicadas via oversampling utilizando a biblioteca Albumentations, aplicando transformações afins geometricamente coerentes, como rotações e inversões axiais. Por outro lado, as classes majoritárias como NFIL foram subamostradas aleatoriamente de mais de 4.300 para 1.000. Fundamental enfatizar: os conjuntos de validação e teste permaneceram totalmente intactos em suas proporções reais da rotina hospitalar.
-->

---

# Fundamentos dos Vision Transformers (ViT)
## Autoatenção Global Multi-Head e a Eliminação do Viés Convolucional

<div class="grid-2">
  <div class="card">
    <h3>Mecanismo de Atenção e Complexidade</h3>
    <ul>
      <li><strong>Divisão em Patches:</strong> Imagem $224 \times 224$ fatiada em $N = 196$ patches de dimensão $16 \times 16 \times 3$.</li>
      <li><strong>Autoatenção Multi-Head (MHSA):</strong>
        $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$
      </li>
      <li>Cada patch computa correlação contextual contra todos os outros 195 patches de forma simultânea.</li>
      <li><strong>Complexidade Quadrática $\mathcal{O}(N^2)$:</strong> Para 196 tokens, geram-se $196 \times 196 = 38.416$ interações de atenção por cabeça e por camada!</li>
      <li><strong>Token Especial [CLS]:</strong> Vetor agregado ao início da sequência para sintetizar a decisão final multiclasse.</li>
    </ul>
  </div>
  <div class="card-purple">
    <h3>Projeção Linear vs. Projeção Convolucional</h3>
    <ul>
      <li><strong>Projeção Linear Pura (Dosovitskiy):</strong>
        <ul>
          <li>Vetoriza os $16 \times 16 \times 3 = 768$ pixels de cada patch e multiplica por matriz de projeção linear $E \in \mathbb{R}^{768 \times D}$.</li>
          <li>Zero viés espacial intrínseco.</li>
        </ul>
      </li>
      <li><strong>Projeção Convolucional (Conv2D):</strong>
        <ul>
          <li>Aplica convolução 2D com kernel $16 \times 16$, stride 16 e $D$ filtros.</li>
          <li>Reintroduz viés indutivo de localidade e extração prévia de gradientes/bordas antes da atenção!</li>
        </ul>
      </li>
    </ul>
  </div>
</div>

<!-- notes:
[ALUNO 2] 16:30 - 17:45
Entrando na arquitetura dos Vision Transformers, formulada por Dosovitskiy em 2020: a imagem de 224 por 224 pixels é particionada em 196 patches de 16 por 16 pixels. Ao contrário das convoluções que operam em janelas locais deslizantes, o ViT calcula a autoatenção de cada patch em relação a todos os outros patches da imagem simultaneamente, com custo computacional quadrático O de N ao quadrado. Um token especial de classificação chamado CLS é adicionado ao início da sequência para consolidar as probabilidades. Os autores avaliaram duas formas de projetar os patches: a Projeção Linear pura, que achata os pixels sem qualquer viés prévio, e a Projeção Convolucional com Conv2D, que aplica um filtro 16 por 16 com stride 16, restaurando uma transição suave e capturando bordas locais antes da camada de atenção.
-->

---

# A Hipótese Central: 5 Técnicas de Extração Dinâmica
## Por Que Não Concentrar os Patches Sobre o Núcleo Atípico?

<div class="grid-2">
  <div class="card">
    <span class="badge badge-amber">A Hipótese de Inovação</span>
    <h3>O Raciocínio dos Pesquisadores</h3>
    <ul>
      <li>Na citologia cervical, o núcleo celular anômalo ocupa apenas a porção central de $90 \times 90$ pixels do recorte.</li>
      <li>A periferia da imagem é dominada por citoplasma homogêneo ou pelo fundo branco vazio da lâmina microscópica.</li>
      <li><strong>Pergunta Científica:</strong> <em>"Por que desperdiçar patches e capacidade de autoatenção em áreas vazias de fundo? Se concentrarmos os 196 patches dinamicamente sobre a célula, o ViT terá maior acurácia diagnóstica?"</em></li>
    </ul>
  </div>
  <div class="card-highlight">
    <h3>As 5 Técnicas Dinâmicas Formuladas</h3>
    <ol style="font-size: 0.85em;">
      <li><strong>Seleção Randômica (SR):</strong> Centros dos 196 patches sorteados de forma uniformemente aleatória na imagem.</li>
      <li><strong>Randômica Aprimorada (RA):</strong> Centros aleatórios com restrição espacial de distância euclidiana mínima para evitar sobreposição total.</li>
      <li><strong>Segmentação GrabCut (SS):</strong> Máscara celular gerada por corte em grafos. Patches centrados apenas na região da célula. <em>Fallback:</em> se área $< 10\%$, reverte para o grid regular.</li>
      <li><strong>Zigue-Zague (ZZ):</strong> Varredura diagonal alternada contínua cobrindo a região de interesse celular.</li>
      <li><strong>Espiral (ES):</strong> Amostragem concêntrica iniciando no centro do núcleo e expandindo em raios crescentes para a periferia.</li>
    </ol>
  </div>
</div>

<!-- notes:
[ALUNO 2] 17:45 - 19:15
Aqui reside a grande hipótese de inovação proposta por Giovanini e Machado: nas imagens do dataset CRIC, o núcleo da célula ocupa frequentemente um quadrado central de cerca de 90 por 90 pixels, enquanto o restante é citoplasma uniforme ou fundo branco da lâmina. A pergunta foi: por que gastar patches de 16 por 16 e computação quadrática de atenção sobre áreas vazias de vidro? Os autores propuseram cinco métodos dinâmicos de extração: a amostragem puramente aleatória SR; a aleatória com restrição de distância mínima RA; a segmentação por GrabCut SS, que gera uma máscara da célula via cortes em grafos com fallback caso a máscara ocupe menos de 10% da imagem; a varredura em zigue-zague ZZ; e a extração em espiral ES, que inicia no núcleo e expande em órbitas crescentes.
-->

---

# Infraestrutura de Hardware e Descongelamento Seletivo
## Fine-Tuning de Modelos Pré-Treinados na ImageNet-21k

<div class="grid-2">
  <div class="card">
    <h3>Infraestrutura Computacional Contrastante</h3>
    <ul>
      <li><strong>Ambiente Local (PUC Minas):</strong>
        <ul>
          <li>GPU NVIDIA GeForce RTX 2060 (6 GB VRAM) | CPU Ryzen 5 3600X | 32 GB RAM.</li>
          <li>Suportou o treinamento de modelos <strong>ViT-Tiny</strong> e <strong>ViT-Small</strong>.</li>
        </ul>
      </li>
      <li><strong>Ambiente em Nuvem (Google Colab PRO):</strong>
        <ul>
          <li>GPU NVIDIA Tesla T4 (15 GB VRAM) | 13 GB RAM.</li>
          <li>Exigida para suportar os 86 milhões de parâmetros do <strong>ViT-Base</strong>.</li>
        </ul>
      </li>
      <li><strong>Hiperparâmetros:</strong> Learning rate calibrada em $1 \times 10^{-5}$ com Adam e batch de 32 (taxa de $1 \times 10^{-4}$ causava divergência).</li>
    </ul>
  </div>
  <div class="card-purple">
    <h3>Estratégia de Descongelamento (Unfreezing)</h3>
    <ul>
      <li><strong>ViT-Small (22M parâmetros - 12 blocos de codificador):</strong>
        <ul>
          <li>Descongelaram-se os <strong>2 primeiros blocos</strong> (feições visuais de baixo nível) e os <strong>3 últimos blocos</strong> (semântica celular abstrata).</li>
          <li>Blocos intermediários permaneceram congelados na ImageNet.</li>
        </ul>
      </li>
      <li><strong>ViT-Base (86M parâmetros):</strong>
        <ul>
          <li>Devido à saturação de memória na Tesla T4 e risco de overfitting, descongelou-se <strong>apenas o último bloco MLP</strong> e a cabeça linear.</li>
          <li>Subajuste estrutural decorrente da restrição de hardware!</li>
        </ul>
      </li>
    </ul>
  </div>
</div>

<!-- notes:
[ALUNO 2] 19:15 - 20:30
O treinamento de Vision Transformers impôs restrições computacionais muito maiores que a CNN do Artigo 1. O modelo ViT-Small pôde ser processado na estação local com uma GPU RTX 2060 de 6 GB, onde os pesquisadores aplicaram um descongelamento seletivo elegante: descongelaram as 2 primeiras camadas do codificador para ajustar filtros de textura à citologia e as 3 últimas camadas para calibrar a decisão entre as 6 classes, mantendo o miolo congelado. Já o modelo ViT-Base, com seus 86 milhões de parâmetros, exigiu o ambiente em nuvem com GPU Tesla T4 de 15 GB. Contudo, devido aos limites de memória, os autores só conseguiram descongelar o último bloco MLP, o que penalizou severamente a adaptação do modelo aos padrões do Sistema Bethesda.
-->

---

# Resultados Experimentais e o "Paradoxo do Grid"
## O Modelo Baseline Convencional Superou Todos os Métodos Dinâmicos!

<div class="card" style="margin-bottom: 12px;">
  <h3>Tabela 2 do Artigo: Acurácia Final no Conjunto de Teste</h3>
  <table>
    <tr><th>Modelo ViT</th><th>Tipo de Projeção</th><th>SR (Rand.)</th><th>RA (Aprim.)</th><th>SS (GrabCut)</th><th>ZZ (Zigue-Z.)</th><th>ES (Espiral)</th></tr>
    <tr><td><strong>ViT-Base</strong></td><td>Linear</td><td>0,70</td><td>0,65</td><td>0,60</td><td>0,67</td><td>0,67</td></tr>
    <tr><td><strong>ViT-Small</strong></td><td>Linear</td><td>0,64</td><td>0,70</td><td>0,71</td><td>0,68</td><td>0,69</td></tr>
    <tr style="background-color: #1e3a5f;"><td><strong>ViT-Small</strong></td><td><strong>Conv2D</strong></td><td><strong>0,75</strong></td><td><strong>0,77</strong></td><td><strong>0,76</strong></td><td><strong>0,76</strong></td><td><strong>0,78</strong></td></tr>
    <tr style="background-color: #064e3b; font-weight: bold; color: #a7f3d0;">
      <td colspan="2">BASELINE GRID CONV2D (ViT-Small Convencional)</td>
      <td colspan="3">Acurácia de Validação: 0,81 (81%)</td>
      <td colspan="2">Acurácia de Teste: 0,79 (79%)</td>
    </tr>
  </table>
</div>

<div class="grid-3">
  <div class="card-highlight">
    <div class="stat-val">0,79</div>
    <div class="stat-lbl">Baseline Grid Regular</div>
    <p style="font-size: 0.72em; margin-top: 4px;">Superou todas as 5 abordagens dinâmicas no teste cego.</p>
  </div>
  <div class="card">
    <div class="stat-val">0,78</div>
    <div class="stat-lbl">Melhor Dinâmico: Espiral</div>
    <p style="font-size: 0.72em; margin-top: 4px;">Amostragem centrada com projeção convolucional Conv2D.</p>
  </div>
  <div class="card-purple">
    <div class="stat-val">+5% a +11%</div>
    <div class="stat-lbl">Ganho com Conv2D</div>
    <p style="font-size: 0.72em; margin-top: 4px;">A convolução superou a projeção linear em todos os casos.</p>
  </div>
</div>

<p style="text-align: right; margin-top: 10px; font-size: 0.82em; color: #34d399;">
<em>Passo a palavra ao colega <strong>[Aluno 3]</strong> para desvendar as causas desse resultado e conduzir a análise crítica comparativa.</em>
</p>

<!-- notes:
[ALUNO 2] 20:30 - 22:00
Chegamos aos resultados cruciais da Tabela 2 do artigo, revelando o que chamamos de "Paradoxo do Grid": o modelo ViT-Small baseline convencional — utilizando a grade estática uniforme de 14 por 14 patches com projeção convolucional — obteve 79% de acurácia no teste e 81% na validação, superando todas as cinco abordagens dinâmicas propostas! Dentre os métodos dinâmicos, a extração em Espiral com Conv2D foi a melhor colocada com 78%, e a projeção convolucional superou a projeção linear pura em absolutamente todas as configurações com ganhos de até 11%.
Transfiro a apresentação agora para o colega [Aluno 3], que explicará a causa-raiz desse fracasso aparente, confrontará os dois artigos teoricamente e apresentará a síntese comparativa multidimensional.
-->

---

# Análise de Causa-Raiz: Por Que o Grid Venceu?
## Desconstrução Geométrica e Matemática do Fracasso dos Patches Dinâmicos

<div class="grid-3">
  <div class="card-highlight">
    <span class="badge badge-amber">Causa 1 • Redundância</span>
    <h3>Super-Aglomeração (Over-Clustering)</h3>
    <p>Forçar <strong>196 patches</strong> de $16 \times 16$ sobre uma região central de $90 \times 90$ gerou <strong>sobreposição $> 80\%$</strong>.</p>
    <p style="font-size: 0.78em; color: #94a3b8;">
    Vetores de Query ($Q$) e Key ($K$) tornaram-se quase idênticos, colapsando a matriz de autoatenção em entropia redundante sem informação nova.
    </p>
  </div>
  <div class="card-purple">
    <span class="badge badge-purple">Causa 2 • Geometria</span>
    <h3>Quebra dos Positional Embeddings</h3>
    <p>Os embeddings de posição 1D foram pré-treinados na ImageNet sobre uma grade cartesiana rígida $14 \times 14$.</p>
    <p style="font-size: 0.78em; color: #94a3b8;">
    Coordenadas aleatórias ou em espiral injetadas nos mesmos índices destorceram a topologia aprendida, forçando a rede a reaprender geometria espacial sem dados suficientes.
    </p>
  </div>
  <div class="card">
    <span class="badge badge-cyan">Causa 3 • Biologia</span>
    <h3>Cegueira da Relação Núcleo-Citoplasma</h3>
    <p>No Sistema Bethesda, atipias como ASC-US e HSIL dependem da <strong>relação de área núcleo/citoplasma (N/C)</strong>.</p>
    <p style="font-size: 0.78em; color: #94a3b8;">
    Concentrar os patches dinamicamente apenas no núcleo privou o ViT de enxergar a borda e o formato do citoplasma periférico, que o grid convencional captura perfeitamente.
    </p>
  </div>
</div>

<p style="margin-top: 15px; font-size: 0.82em; color: #38bdf8;">
<strong>O Resgate da Convolução:</strong> A projeção Conv2D superou a linear porque funcionou como uma camada de suavização espacial contínua, reintroduzindo gradientes de vizinhança local antes do colapso da atenção.
</p>

<!-- notes:
[ALUNO 3] 22:00 - 23:30
Obrigado, [Aluno 2]. O desfecho experimental do Artigo 2 nos ensina lições epistemológicas profundas sobre a visão computacional. A hipótese dos patches dinâmicos parecia intuitiva e elegante, mas foi refutada por três causas fundamentais:
Primeiro, a Super-Aglomeração Espacial. Ao comprimir 196 patches de 16 por 16 pixels dentro de um núcleo de apenas 90 por 90, os patches sobrepuseram-se em mais de 80%. Múltiplos patches capturavam o mesmo grupo de pixels; os tensores de consulta e chave da autoatenção tornaram-se quase cópias idênticas, desperdiçando a capacidade do modelo em pura redundância.
Segundo, a quebra dos Positional Embeddings. O ViT foi pré-treinado na ImageNet para entender uma grade cartesiana 14 por 14. Quando alteramos os centros dos patches para uma espiral ou sorteio aleatório mas injetamos os mesmos índices posicionais, destruímos o mapa espacial pré-treinado.
E terceiro, a biologia celular do Sistema Bethesda. Patologistas diferenciam lesões de alto e baixo grau avaliando a proporção de área entre o núcleo e o citoplasma. Ao concentrar todos os patches no núcleo, o modelo ficou cego quanto à periferia celular, contexto que o grid convencional retém com perfeição.
-->

---

# Duelo Teórico: Viés Indutivo vs. Fome de Dados (Data-Hunger)
## Por Que o Ensemble de CNNs Atingiu 95% e o ViT Ficou em 79% na Mesma Base?

<div class="grid-2">
  <div class="card">
    <h3>Rede Convolucional (CNN) — Artigo 1</h3>
    <ul>
      <li><strong>Viés Indutivo Rígido embutido na matemática:</strong>
        <ul>
          <li><em>Localidade:</em> pixels vizinhos compartilham forte correlação semântica.</li>
          <li><em>Equivariância Translacional:</em> uma lesão no hemisfério esquerdo é reconhecida com os mesmos pesos no hemisfério direito.</li>
        </ul>
      </li>
      <li><strong>Baixíssima Fome de Dados:</strong> Converge e generaliza com <strong>apenas 5.500 amostras</strong> de ressonância treinadas do zero!</li>
      <li><strong>Complexidade Linear $\mathcal{O}(H \cdot W \cdot K^2)$</strong> no tamanho da imagem.</li>
    </ul>
  </div>
  <div class="card-purple">
    <h3>Vision Transformer (ViT) — Artigo 2</h3>
    <ul>
      <li><strong>Ausência de Viés Indutivo Prévio:</strong>
        <ul>
          <li>Atenção global $all-to-all$ desprovida de premissas espaciais.</li>
          <li>O modelo precisa descobrir as leis da geometria visual a partir da força bruta dos gradientes.</li>
        </ul>
      </li>
      <li><strong>Fome Massiva de Dados (Data-Hunger):</strong> Mesmo com pré-treino na ImageNet-21k (14 milhões de imagens), 6.000 amostras celulares médicas são insuficientes para calibrar a atenção fina.</li>
      <li><strong>Estado da Arte no CRIC (Diniz et al., 2021):</strong> Um Ensemble de CNNs atingiu <strong>95% de acurácia</strong>, superando com folga o ViT (79%).</li>
    </ul>
  </div>
</div>

<!-- notes:
[ALUNO 3] 23:30 - 25:00
Ao confrontarmos os dois paradigmas, deparamo-nos com o núcleo teórico da Visão Computacional moderna: o duelo entre Viés Indutivo e Fome de Dados (Data-Hunger).
As Redes Neurais Convolucionais do Artigo 1 trazem em sua formulação matemática os pressupostos físicos de localidade espacial e invariância à translação. Por isso, a CNN da UFCSPA necessitou de apenas 5.500 imagens de ressonância magnética para atingir 99% de acurácia treinando do zero.
Por outro lado, o Vision Transformer do Artigo 2 trata os patches como uma lista desordenada de tokens, precisando deduzir as relações espaciais por meio da autoatenção global. Quando confrontamos o ViT com o estado da arte na base CRIC — estabelecido por Diniz et al. em 2021 através de um Ensemble de CNNs clássicas que atingiu 95% de acurácia —, vemos que o ViT estagnou em 79%. O pré-treinamento da ImageNet com carros, animais e móveis transfere pouca semântica útil para distinguir granulações microscópicas de cromatina, e bases médicas pequenas sofrem para saciar a fome de dados dos Transformers.
-->

---

# Matriz Comparativa Sistemática: Artigo 1 vs. Artigo 2
## Desconstrução Rigorosa dos Dois Trabalhos em 16 Dimensões Técnicas

<table style="font-size: 0.62em;">
  <tr><th>Dimensão de Análise</th><th>Artigo 1: UFCSPA (BRACIS 2023)</th><th>Artigo 2: PUC Minas / UFMG (SBC 2025)</th></tr>
  <tr><td><strong>Problema Clínico</strong></td><td>Diagnóstico diferencial de neoplasias encefálicas</td><td>Rastreamento citológico de câncer do colo do útero</td></tr>
  <tr><td><strong>Modalidade de Imagem</strong></td><td>Ressonância Magnética (MRI) 2D axial/sagital</td><td>Microscopia óptica citopatológica (Papanicolau)</td></tr>
  <tr><td><strong>Granularidade</strong></td><td>Macroestrutural (crânio, ventrículos, massa tumoral)</td><td>Microestrutural (núcleos celulares isolados e atipias)</td></tr>
  <tr><td><strong>Classes Diagnósticas</strong></td><td>4 classes: Glioma, Meningioma, No Tumor, Pituitary</td><td>6 classes (Bethesda): ASC-H, ASC-US, HSIL, LSIL, NFIL, SCC</td></tr>
  <tr><td><strong>Bases de Dados</strong></td><td>Kaggle Brain Tumor MRI + Figshare auditado</td><td>Base CRIC (Universidade Federal de Ouro Preto - UFOP)</td></tr>
  <tr><td><strong>Volume de Amostras</strong></td><td>7.023 imagens (5.531 treino e 1.297 teste)</td><td>11.534 núcleos celulares de 400 imagens de lâminas</td></tr>
  <tr><td><strong>Resolução de Entrada</strong></td><td>$64 \times 64$ pixels (3 canais, escala $[0, 1]$)</td><td>$224 \times 224$ pixels (recortes nativos de $90 \times 90$)</td></tr>
  <tr><td><strong>Auditoria de Dados</strong></td><td>Substituição cirúrgica de rótulos errados de Glioma</td><td>Segmentação morfológica e descarte de debris</td></tr>
  <tr><td><strong>Prevenção de Leakage</strong></td><td>Separação antes de normalizar; K-Fold 5 dobras</td><td><strong>Estratificação estrita por paciente (64% / 20% / 16%)</strong></td></tr>
  <tr><td><strong>Balanceamento</strong></td><td>Pesos de classe na perda ($w_c \in [0.86, 1.21]$)</td><td>Híbrido: Oversampling (Albumentations) + Undersampling</td></tr>
  <tr><td><strong>Paradigma Arquitetural</strong></td><td><strong>Rede Neural Convolucional (CNN) adaptada</strong></td><td><strong>Vision Transformer (ViT) com Autoatenção</strong></td></tr>
  <tr><td><strong>Origem dos Pesos</strong></td><td><strong>Treinado do zero (from scratch)</strong></td><td><strong>Fine-Tuning com pré-treino na ImageNet-21k</strong></td></tr>
  <tr><td><strong>Extração Espacial</strong></td><td>Convoluções contínuas $3 \times 3$ em toda a imagem</td><td>Grid Regular convencional vs. 5 Métodos Dinâmicos</td></tr>
  <tr><td><strong>Projeção de Entrada</strong></td><td>Convolucional pura contínua</td><td>Projeção Linear pura vs. Projeção Convolucional (Conv2D)</td></tr>
  <tr><td><strong>Pegada Computacional</strong></td><td>Muito leve: 3 blocos Conv, rápida em CPU/GPU modesta</td><td>Pesada: ViT-Small (RTX 2060 6GB) e ViT-Base (Colab T4 15GB)</td></tr>
  <tr><td><strong>Explicabilidade (XAI)</strong></td><td><strong>Grad-CAM</strong> com validação cruzada em base externa</td><td>Rastreamento geométrico da distribuição dos patches</td></tr>
  <tr><td><strong>Desempenho Final</strong></td><td><strong>Acurácia Global: 99,0%</strong> (F1: 1,00 em Glioma)</td><td><strong>Acurácia: 79,0%</strong> (Baseline) / <strong>78,0%</strong> (Espiral Conv2D)</td></tr>
</table>

<!-- notes:
[ALUNO 3] 25:00 - 26:45
Esta matriz comparativa consolida sistematicamente a desconstrução técnica de ambos os trabalhos sob 16 dimensões analíticas.
No Artigo 1, vemos um projeto cirúrgico de engenharia: uma CNN customizada extremamente enxuta, treinada do zero em imagens compactas de 64 por 64 pixels, que alcançou 99% de acurácia global com custo computacional mínimo e alta transparência via Grad-CAM.
No Artigo 2, temos uma incursão investigativa na fronteira dos Vision Transformers, trabalhando em 224 por 224 com modelos de dezenas de milhões de parâmetros, fine-tuning na ImageNet-21k e GPUs de grande capacidade como a Tesla T4.
Dois domínios de saúde pública de altíssima relevância nacional — neuro-oncologia e saúde da mulher —, abordados por duas escolas metodológicas distintas.
-->

---

# Auditoria Metodológica: Slice Leakage vs. Patient Split
## Avaliação Crítica da Integridade Científica dos Protocolos

<div class="grid-2">
  <div class="card-highlight">
    <span class="badge badge-green">Mérito Absoluto do Artigo 2</span>
    <h3>Estratificação Estrita por Paciente</h3>
    <ul>
      <li>O particionamento por código de paciente é a <strong>blindagem metodológica perfeita</strong> na citopatologia.</li>
      <li>Impede que características idiossincráticas de coloração da lâmina, intensidade do esfregaço e tempo de fixação sejam aprendidas como atalhos espúrios.</li>
      <li>Se a acurácia é 79%, trata-se de um <strong>79% honesto, clínico e auditável</strong> em pacientes que o algoritmo jamais viu.</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge badge-amber">Vulnerabilidade Potencial do Artigo 1</span>
    <h3>O Risco Latente de Slice Leakage</h3>
    <ul>
      <li>O benchmark público do Kaggle particionou as imagens fatiadas em nível de arquivo 2D.</li>
      <li><strong>Risco de Vazamento de Fatias (Slice Leakage):</strong> Fatias axiais contíguas do mesmo encéfalo ($z=14$ e $z=15$) podem ter caído simultaneamente no treino e no teste, inflando o desempenho para 99%.</li>
      <li><strong>O Fator Atenuante:</strong> Os autores da UFCSPA contornaram parcialmente essa dúvida ao validar o Grad-CAM em uma <strong>base externa inédita (Bhuvaji et al.)</strong>, onde o modelo manteve o foco correto na lesão.</li>
    </ul>
  </div>
</div>

<!-- notes:
[ALUNO 3] 26:45 - 28:15
Exercendo nossa capacidade de avaliação crítica independente, devemos auditar a integridade metodológica de validação de ambos os trabalhos.
O Artigo 2 recebe nota máxima no protocolo de particionamento: a divisão estrita por paciente elimina o risco de memorização de artefatos de lâmina. Seus 79% de acurácia refletem uma capacidade de generalização autêntica para novas pacientes.
Já no Artigo 1, embora os 99% de acurácia sejam impressionantes, existe uma vulnerabilidade inerente a datasets públicos de ressonância fatiada 2D: o risco de slice leakage. Caso fatias adjacentes do mesmo crânio tenham sido distribuídas entre treino e teste, o modelo pode ter se beneficiado de correlações visuais redundantes. A UFCSPA mitigou brilhantemente essa desconfiança ao demonstrar que os mapas Grad-CAM mantiveram a ativação na massa tumoral em uma base externa completamente inédita, mas para futuros trabalhos clínicos, a divisão por volume tridimensional de paciente é mandatória.
-->

---

# Árvore de Decisão: Quando Usar CNN ou ViT na Saúde?
## Diretrizes Prescritivas de Engenharia de Software e Visão Computacional

<div class="grid-2">
  <div class="card-highlight">
    <h3>Fluxo Decisório para Projetos Biomédicos</h3>
    <pre>
Novo Problema de Visão Computacional Médica
       │
       ▼
[Volume de Dados Anotados?]
  ├── &lt; 10.000 imagens ────────► <strong>CNN Especializada Leve</strong>
  │                              (ResNet, EfficientNet, Custom)
  └── &gt; 100.000 amostras
         │
         ▼
[Infraestrutura de Hardware?]
  ├── Restrita (1 GPU / Edge) ─► <strong>CNN Otimizada</strong> (MobileNet/ConvNeXt)
  └── Servidores / Nuvem
         │
         ▼
[Natureza do Contexto Espacial?]
  ├── Texturas e Bordas Locais ─► <strong>Modelos Híbridos</strong> (CoAtNet)
  └── Relações Globais Longas ─► <strong>Vision Transformer</strong> (Grid Regular + Conv2D)
    </pre>
  </div>
  <div class="card">
    <h3>Recomendações Práticas para Implantação</h3>
    <ul>
      <li><strong>Hospitais Regionais e Postos de Saúde (Edge):</strong> Modelos convolucionais leves (Artigo 1) operando em $64 \times 64$ ou $128 \times 128$ são imbatíveis: rodam em milissegundos sem conexão de nuvem e geram mapas Grad-CAM transparentes.</li>
      <li><strong>Lâminas Inteiras (Whole Slide Imaging - WSI):</strong> Vision Transformers hierárquicos (Swin Transformer) são promissores para integrar contexto tecidual de grande escala, desde que mantenham o <strong>Grid Regular com Projeção Convolucional</strong>.</li>
    </ul>
  </div>
</div>

<!-- notes:
[ALUNO 3] 28:15 - 29:45
Como futuros profissionais de computação, sintetizamos as lições dos dois artigos em uma árvore de decisão prescritiva de engenharia.
Se o projeto biomédico possui menos de 10 mil amostras rotuladas e restrição de hardware, a escolha mandatória deve ser uma Rede Convolucional especializada e fortemente regularizada, assim como fez a UFCSPA. Ela é barata, eficiente, possui convergência previsível e viés indutivo adequado.
Vision Transformers só devem ser adotados quando houver dezenas ou centenas de milhares de imagens — como na análise de lâminas inteiras em Whole Slide Imaging —, e mesmo assim, a recomendação categórica é manter a extração em Grid Regular uniforme associada à projeção convolucional Conv2D, evitando a fragmentação dinâmica descontrolada de patches.
-->

---

# O Valor Epistemológico do Resultado Negativo
## Superando o Viés de Publicação na Inteligência Artificial

<div class="grid-2">
  <div class="card-highlight">
    <span class="badge badge-purple">Contribuição Científica Real</span>
    <h3>A Relevância do Artigo 2</h3>
    <ul>
      <li>Na literatura de aprendizado de máquina, existe um vício crônico de publicação (<em>publication bias</em>): artigos só são aceitos quando superam o estado da arte com acurácias recordistas.</li>
      <li>O Artigo 2 (PUC Minas / UFMG) possui <strong>mérito científico exemplar</strong>: testou uma hipótese logicamente atraente (concentração dinâmica de patches) sob rigoroso controle experimental e demonstrou matematicamente por que ela falha.</li>
      <li><strong>Impacto na Comunidade:</strong> Evita que dezenas de outros grupos de pesquisa desperdicem meses de trabalho e poder de supercomputação em estratégias similares sem compensação topológica.</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge badge-green">Três Lições Eternas de IA Médica</span>
    <ol style="font-size: 0.88em;">
      <li><strong>Curadoria de Dados Supera Parâmetros:</strong> A higienização dos rótulos com o Figshare no Artigo 1 foi mais determinante para os 99% do que qualquer ajuste fino de hiperparâmetros.</li>
      <li><strong>O Hype do Transformer Não Anula a Convolução:</strong> Em dados biomédicos pequenos, o viés indutivo clássico ainda é o melhor aliado do cientista de dados.</li>
      <li><strong>A Hibridização é o Futuro:</strong> A projeção convolucional salvou os patches dinâmicos, provando que a união entre convoluções locais e atenção global é o caminho dominante.</li>
    </ol>
  </div>
</div>

<!-- notes:
[ALUNO 3] 29:45 - 31:15
Queremos destacar o imenso valor epistemológico do "resultado negativo" trazido pelo Artigo 2.
Na academia e na indústria de IA, existe uma tentação constante de esconder resultados que não bateram recordes de acurácia. A publicação de Giovanini e Machado nos anais da SBC é um ato de maturidade e rigor científico: eles formularam uma hipótese plausível, projetaram 5 métodos, executaram testes cegos e provaram que a amostragem dinâmica quebra a atenção e destrói os embeddings posicionais. Isso economiza centenas de horas de GPU para a comunidade científica internacional.
Junto a isso, o Artigo 1 reforça que curadoria cirúrgica de dados e explicabilidade clínica com Grad-CAM são pré-requisitos absolutos antes de qualquer homologação em saúde pública.
-->

---

# Conclusões Finais e Perspectivas Futuras
## Síntese do Grupo 4 e Próximos Passos na Fronteira da Pesquisa

<div class="grid-2">
  <div class="card-highlight">
    <h3>Síntese dos Achados pelo Grupo 4</h3>
    <ul>
      <li><strong>Artigo 1 (UFCSPA):</strong> Provou que uma CNN leve inspirada na AlexNet, combinada com auditoria de dados e Dropout progressivo, atinge <strong>99% de acurácia com 100% de sensibilidade para gliomas</strong> e custo computacional quase nulo.</li>
      <li><strong>Artigo 2 (PUC Minas/UFMG):</strong> Provou que o <strong>Grid Regular com Projeção Convolucional (79%)</strong> supera abordagens dinâmicas na citopatologia devido à redundância e ruptura de embeddings.</li>
      <li><strong>O Veredito Teórico:</strong> Redes Convolucionais continuam superiores em datasets médicos de pequeno porte graças ao viés de localidade e baixa fome de dados.</li>
    </ul>
  </div>
  <div class="card-purple">
    <h3>Propostas do Grupo para Pesquisas Futuras</h3>
    <ul>
      <li><strong>Swin Transformer na Citopatologia:</strong> Atenção em janelas locais deslocadas (<em>Shifted Windows</em>) para unir o viés local convolucional com a flexibilidade da autoatenção.</li>
      <li><strong>Positional Embeddings Deformáveis / 2D Radiais:</strong> Caso se utilize a extração em espiral, calcular embeddings senoidais contínuos baseados na distância radial euclidiana real até o núcleo.</li>
      <li><strong>Aumento Sintético com Modelos de Difusão:</strong> Sintetizar células atípicas raras (SCC) para saciar a fome de dados dos Transformers em bases médicas balanceadas.</li>
    </ul>
  </div>
</div>

<!-- notes:
[ALUNO 3] 31:15 - 33:00
Concluímos com uma síntese clara: o Artigo 1 validou a eficácia da simplicidade e da parcimônia convolucional em ressonância magnética, garantindo 100% de sensibilidade no diagnóstico do glioma e explicabilidade sólida. O Artigo 2 descortinou as limitações dos Vision Transformers em datasets celulares modestos, demonstrando a superioridade da grade uniforme e o papel redentor da projeção convolucional.
Para o futuro da citopatologia digital, propomos três direções: adotar arquiteturas hierárquicas como o Swin Transformer; modelar embeddings posicionais radiais contínuos para geometrias em espiral; e explorar modelos generativos de difusão para expandir a amostragem de carcinomas invasivos raros, saciando a fome de dados dos transformadores.
-->

---

# Referências Bibliográficas (Normas SBC / ABNT)
## Fontes Primárias e Literatura Fundamental de Suporte

<div class="grid-2" style="font-size: 0.75em;">
  <div class="card">
    <h3>Artigos Centrais Analisados</h3>
    <ul>
      <li><strong>Artigo 1:</strong> FELIPE, C. S.; PIANOSCHI ALVA, T. A.; WINCK, A. T.; BECKER, C. D. L. <em>An Approach in Brain Tumor Classification: The Development of a New Convolutional Neural Network Model</em>. In: Anais do Brazilian Conference on Intelligent Systems (BRACIS), SBC, 2023.</li>
      <li><strong>Artigo 2:</strong> GIOVANINI, V. H.; MACHADO, A. M. C. <em>Vision Transformers com Patches Dinâmicos para a Análise de Lâminas Histológicas</em>. In: Anais da Sociedade Brasileira de Computação (SBC), 2025.</li>
    </ul>
  </div>
  <div class="card">
    <h3>Bases de Dados e Literatura Teórica</h3>
    <ul>
      <li>CHENG, J. et al. <em>Brain Tumor Dataset</em>. Figshare, 2017.</li>
      <li>CRIC Searchable Image Database. Centro de Reconhecimento e Inspeção de Células, UFOP, 2021.</li>
      <li>DOSOVITSKIY, A. et al. <em>An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale</em>. ICLR, 2021.</li>
      <li>DINIZ, D. N. et al. <em>Deep Learning Ensemble for Cervical Cell Classification on CRIC Database</em>. IEEE Access, 2021.</li>
      <li>KRIZHEVSKY, A.; SUTSKEVER, I.; HINTON, G. E. <em>ImageNet Classification with Deep CNNs</em>. NeurIPS, 2012.</li>
      <li>SELVARAJU, R. R. et al. <em>Grad-CAM: Visual Explanations from Deep Networks</em>. ICCV, 2017.</li>
    </ul>
  </div>
</div>

<!-- notes:
[ALUNO 3] 33:00 - 34:00
Registramos aqui todas as fontes primárias e a literatura canônica que embasaram nossa análise crítica, em estrita observância às normas da Sociedade Brasileira de Computação e da ABNT.
-->

---

<!-- _class: lead -->
# Agradecimentos e Abertura para a Banca Avaliadora
## Muito obrigado pela atenção de todos!

<div class="card-highlight" style="display: inline-block; padding: 15px 35px; margin-top: 15px; text-align: center;">
  <p style="font-size: 1.1em; color: #38bdf8; margin: 0 0 8px 0;"><strong>Universidade Federal do Piauí — UFPI</strong></p>
  <p style="font-size: 0.9em; color: #cbd5e1; margin: 0 0 5px 0;">Disciplina: Tópicos Especiais em Visão Computacional</p>
  <p style="font-size: 0.85em; color: #94a3b8; margin: 0 0 10px 0;">Docente Avaliador: <strong>Prof. Dr. José Denes Lima Araújo</strong></p>
  <hr style="border: none; border-top: 1px solid #334155; margin: 8px 0;" />
  <p style="font-size: 0.85em; color: #f8fafc; margin: 0;">
  <strong>Grupo 4:</strong> Integrante 1 (Aluno 1) • Integrante 2 (Aluno 2) • Integrante 3 (Aluno 3)
  </p>
</div>

<p style="margin-top: 25px; font-size: 0.95em; color: #34d399; text-align: center;">
<em>Concluímos rigorosamente dentro do prazo regulamentar (~34 min) e estamos à disposição para a sabatina da banca.</em>
</p>

<!-- notes:
[TRIO / ALUNO 3] 34:00 - 35:00
Agradecemos a atenção do Prof. Dr. José Denes Lima Araújo e de todos os colegas presentes. Encerramos nossa apresentação rigorosamente na marca dos 34 minutos e 30 segundos, em pleno cumprimento do edital e preservando o tempo regulamentar para a arguição técnica. Todo o trio está a postos e à disposição para as perguntas e considerações da banca. Muito obrigado!
-->
