---
marp: true
theme: uncover
paginate: true
header: "UFPI / CSHNB • Tópicos Especiais em Visão Computacional • Prof. Dr. José Denes Araújo"
footer: "Grupo 4 • Reprodução Científica GMIC & WSOD em Mamografia • 2026"
style: |
  section {
    background-color: #0b1120;
    color: #f1f5f9;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    padding: 38px 50px;
    font-size: 21px;
    text-align: left;
    justify-content: flex-start;
  }
  h1 {
    color: #38bdf8;
    font-size: 34px;
    margin-bottom: 8px;
    font-weight: 700;
    letter-spacing: -0.5px;
  }
  h2 {
    color: #0284c7;
    font-size: 25px;
    margin-top: 0;
    margin-bottom: 16px;
    border-bottom: 2px solid #1e293b;
    padding-bottom: 6px;
  }
  h3 {
    color: #f43f5e;
    font-size: 20px;
    margin-bottom: 8px;
  }
  .highlight {
    color: #38bdf8;
    font-weight: bold;
  }
  .accent {
    color: #f43f5e;
    font-weight: bold;
  }
  .green {
    color: #10b981;
    font-weight: bold;
  }
  .badge {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 14px;
    color: #94a3b8;
    display: inline-block;
  }
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  .grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
  }
  .card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 8px;
    padding: 14px 18px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
  }
  .card-accent {
    background: #0f172a;
    border-left: 4px solid #38bdf8;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 10px 0;
  }
  .card-danger {
    background: #1e111a;
    border-left: 4px solid #f43f5e;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 10px 0;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 16px;
    margin-top: 10px;
  }
  th {
    background: #1e293b;
    color: #38bdf8;
    padding: 8px 12px;
    text-align: left;
    border: 1px solid #334155;
  }
  td {
    padding: 8px 12px;
    border: 1px solid #1f2937;
    background: #0f172a;
  }
  tr.highlight-row td {
    background: #064e3b;
    color: #ecfdf5;
    font-weight: bold;
  }
  code {
    background: #1e293b;
    color: #38bdf8;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 16px;
  }
  ul {
    margin-top: 6px;
    margin-bottom: 6px;
    padding-left: 22px;
  }
  li {
    margin-bottom: 6px;
    line-height: 1.4;
  }
  .speaker-badge {
    position: absolute;
    top: 24px;
    right: 40px;
    background: #0284c7;
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
---

<!-- Slide 1: Capa -->
<span class="speaker-badge">Abertura • Grupo 4</span>

# Reprodução Científica e Análise de Desacoplamento de CAMs
## Detecção Fracamente Supervisionada de Massas em Mamografia Digital

<div class="card-accent" style="margin-top: 24px;">
  <strong>Artigo Base:</strong> <em>"A Study on Class Activation Map Methods to Detect Masses in Mammography Images using Weakly Supervised Learning"</em> (Sampaio & Cordeiro — UFRPE, SBC 2022)
</div>

<div class="grid-2" style="margin-top: 24px;">
  <div class="card">
    <span class="badge">EQUIPE DE DESENVOLVIMENTO</span>
    <ul style="list-style: none; padding-left: 0; margin-top: 8px;">
      <li><strong>Integrante 1:</strong> Introdução Clínica & Arquitetura GMIC</li>
      <li><strong>Integrante 2:</strong> CAMs & Engenharia PyTorch</li>
      <li><strong>Integrante 3:</strong> Experimentos, Detecção WSOD & Errata</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge">INSTITUIÇÃO E DISCIPLINA</span>
    <p style="margin-top: 8px; margin-bottom: 4px; font-size: 16px;">
      <strong>Universidade Federal do Piauí (UFPI)</strong><br>
      Campus Senador Helvídio Nunes de Barros (CSHNB)<br>
      Tópicos Especiais em Visão Computacional<br>
      <strong>Docente:</strong> Prof. Dr. José Denes Lima Araújo
    </p>
  </div>
</div>

---

<!-- Slide 2: Contextualização Clínica -->
<span class="speaker-badge">Integrante 1 • 00:00 - 02:00</span>

# Contexto Clínico e Desafio Radiológico
## Câncer de Mama e os Limites do Rastreamento Mamográfico

<div class="grid-2">
  <div class="card">
    <h3>Impacto Epidemiológico Mundial</h3>
    <ul>
      <li><span class="accent">Neoplasia mais incidente</span> e líder em mortalidade feminina (OMS: 15,5% dos óbitos oncológicos).</li>
      <li><strong>Detecção precoce é crucial:</strong> Sobrevida em 5 anos > 90% para lesões iniciais (< 10 mm) vs < 30% em metástases.</li>
      <li><strong>Mamografia Digital (FFDM):</strong> Exame padrão-ouro internacional para rastreamento populacional.</li>
    </ul>
  </div>
  <div class="card">
    <h3>O Gargalo Radiológico Humano</h3>
    <ul>
      <li><strong>Efeito de Mascaramento:</strong> Mamas densas e massas malignas apresentam idêntica atenuação de raios-X.</li>
      <li><strong>Morfologia Sutil:</strong> Bordas espiculadas e microcalcificações pleomórficas de difícil percepção visual.</li>
      <li><strong>Fadiga do Especialista:</strong> Milhares de projeções de alta resolução (2944x1920) geram até 30% de falsos negativos.</li>
    </ul>
  </div>
</div>

<div class="card-accent" style="margin-top: 14px;">
  <strong>Oportunidade para CAD:</strong> Sistemas de Visão Computacional atuam como uma "segunda opinião" automatizada, delimitando regiões suspeitas com precisão.
</div>

---

<!-- Slide 3: O Paradigma WSOD -->
<span class="speaker-badge">Integrante 1 • 02:00 - 03:30</span>

# O Paradigma de Supervisão Fraca (WSOD)
## Weakly Supervised Object Detection: Rótulo Global vs Custo de Anotação

<div class="grid-2">
  <div class="card-danger">
    <h3>Supervisão Total (Full Supervision)</h3>
    <ul>
      <li>Requer delimitação manual de máscaras e bounding boxes para cada exame.</li>
      <li><strong>Inviabilidade clínica:</strong> Custo financeiro proibitivo e centenas de horas de radiologistas seniores.</li>
      <li><strong>Alta divergência:</strong> Variabilidade interobservador em bordas infiltrativas.</li>
      <li>Menos de 1% das bases hospitalares possui caixas anotadas.</li>
    </ul>
  </div>
  <div class="card-accent">
    <h3>Supervisão Fraca (WSOD)</h3>
    <ul>
      <li>Treinamento com <span class="highlight">apenas o rótulo da imagem</span>: $y \in \{0, 1\}$ (Normal vs Massa).</li>
      <li>Nenhuma coordenada espacial é fornecida durante a fase de treino.</li>
      <li><strong>Objetivo Duplo:</strong> Classificar a imagem e gerar a localização da lesão $\mathcal{B} = \{b_k\}$ via interpretabilidade.</li>
      <li>Viabiliza o uso de milhões de exames clínicos reais já laudados.</li>
    </ul>
  </div>
</div>

<div class="card" style="margin-top: 10px; font-size: 16px; text-align: center;">
  <strong>Formulação:</strong> Treino: $\mathcal{D}_{train} = \{(x_n, y_n)\}_{n=1}^N$ &nbsp; $\implies$ &nbsp; Inferência: Predição de classe $\hat{y}$ + Bounding Boxes com $\text{IoU} \ge 0.3$.
</div>

---

<!-- Slide 4: O Artigo Selecionado -->
<span class="speaker-badge">Integrante 1 • 03:30 - 05:00</span>

# O Artigo Reproduzido e a Questão Científica
## Sampaio & Cordeiro (UFRPE, 2022) e a Inovação do Desacoplamento

<div class="card-accent">
  <strong>Pergunta de Pesquisa:</strong> <em>"Substituir o CAM padrão por métodos de saliência avançados e desacoplar o CAM de treino do CAM de teste melhora a detecção de massas mamárias?"</em>
</div>

<div class="grid-3" style="margin-top: 14px;">
  <div class="card">
    <span class="badge">MODELO BASE</span>
    <h3 style="margin-top: 8px;">GMIC</h3>
    <p style="font-size: 15px;">Desenvolvido por Shen et al. (<em>Medical Image Analysis</em>, 2021) para lidar com mamografias de altíssima resolução sem perda de detalhes milimétricos.</p>
  </div>
  <div class="card">
    <span class="badge">DATASET PÚBLICO</span>
    <h3 style="margin-top: 8px;">VinDr-Mammo</h3>
    <p style="font-size: 15px;">20.000 imagens FFDM com anotações de consenso de múltiplos radiologistas especialistas (Vietnã/EUA).</p>
  </div>
  <div class="card">
    <span class="badge">CONTRIBUIÇÃO</span>
    <h3 style="margin-top: 8px;">Desacoplamento</h3>
    <p style="font-size: 15px;">Demonstrar que o método de CAM ideal para extrair patches no treino difere do ideal para inferir caixas no teste.</p>
  </div>
</div>

<div class="card" style="margin-top: 12px; font-size: 15px;">
  <strong>Nossa Meta de Reprodução:</strong> Reconstruir o GMIC em PyTorch, implementar os 5 CAMs desacoplados, reproduzir a Tabela 1 e a matriz mestra da Tabela 2 com rigor técnico.
</div>

---

<!-- Slide 5: Arquitetura GMIC -->
<span class="speaker-badge">Integrante 1 • 05:00 - 06:30</span>

# Arquitetura GMIC: Três Ramos Integrados
## Globally-Aware Multiple Instance Classifier (Shen et al. / Sampaio & Cordeiro)

<div class="grid-3">
  <div class="card">
    <span class="badge">1. RAMO GLOBAL</span>
    <h3 style="margin-top: 6px;">Visão Holística</h3>
    <ul>
      <li><strong>Entrada:</strong> Imagem completa $x$ ($2944 \times 1920$).</li>
      <li><strong>Backbone:</strong> ResNet-22 personalizada.</li>
      <li>Gera vetor $h_{global}$ e predição global $\hat{y}_{global}$.</li>
      <li>Produz o mapa de ativação $A^c \in \mathbb{R}^{H_g \times W_g}$.</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge">2. EXTRAÇÃO DE PATCHES</span>
    <h3 style="margin-top: 6px;">Seleção Gulosa</h3>
    <ul>
      <li>Localiza os $K=6$ picos de calor em $A^c$.</li>
      <li>Aplica <strong>supressão de vizinhança</strong> espacial.</li>
      <li>Recorta $K$ patches ($256 \times 256$) na resolução máxima nativa.</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge">3. RAMO LOCAL & FUSÃO</span>
    <h3 style="margin-top: 6px;">Detalhamento Fino</h3>
    <ul>
      <li><strong>Backbone Local:</strong> ResNet-18 extrai características morfológicas finas.</li>
      <li>Agregação MIL via Max-Pooling $\implies h_{local}$.</li>
      <li><strong>Módulo de Fusão:</strong> Concatenação $[h_g; h_l] \to \text{FC} \to \hat{y}_{fusao}$.</li>
    </ul>
  </div>
</div>

<div class="card-accent" style="margin-top: 12px; font-size: 15px;">
  <strong>Vantagem Estrutural:</strong> Processa gigapixels preservando a resolução nativa da lesão nos patches sem estourar a memória de vídeo.
</div>

---

<!-- Slide 6: Função de Perda Multi-Ramo -->
<span class="speaker-badge">Integrante 1 • 06:30 - 08:00</span>

# Função de Perda Multi-Ramo & Esparsidade $\beta$
## Otimização Sinergética e Regularização L1 sobre o Mapa de Calor

$$\mathcal{L}_{total} = \text{BCE}(y, \hat{y}_{local}) + \text{BCE}(y, \hat{y}_{global}) + \text{BCE}(y, \hat{y}_{fusao}) + \beta \cdot \mathcal{L}_{reg}(A^c)$$

<div class="grid-2" style="margin-top: 12px;">
  <div class="card">
    <h3>Sinergia dos Três Ramos</h3>
    <ul>
      <li>$\text{BCE}_{global}$: Força o backbone global a aprender o contexto de densidade da mama.</li>
      <li>$\text{BCE}_{local}$: Força o backbone local a discriminar bordas e espículas nos patches recortados.</li>
      <li>$\text{BCE}_{fusao}$: Calibra o classificador integrado final.</li>
    </ul>
  </div>
  <div class="card">
    <h3>Regularização de Esparsidade L1</h3>
    <ul>
      <li>$\mathcal{L}_{reg}(A^c) = \sum_{i=1}^{H_g} \sum_{j=1}^{W_g} |A_{i,j}^c|$</li>
      <li><span class="accent">Hiperparâmetro Crítico:</span> $\beta = 3.26$.</li>
      <li><strong>Por que é indispensável?</strong> Sem o termo L1 ($\beta = 0$), o CAM se espalha por todo o parênquima sadio, gerando patches sem lesão e ruído.</li>
    </ul>
  </div>
</div>

<div class="card-accent" style="margin-top: 10px; font-size: 15px;">
  <em>Transição: "Para apresentar a taxonomia matemática dos 5 CAMs e a engenharia de software em PyTorch, passo a palavra ao Integrante 2."</em>
</div>

---

<!-- Slide 7: Taxonomia dos CAMs - Clássico e Grad-CAM -->
<span class="speaker-badge">Integrante 2 • 08:00 - 09:30</span>

# Taxonomia dos Mapas de Ativação (1/2)
## Fundamentos de Interpretabilidade e Saliência Visual Convolucional

<div class="grid-2">
  <div class="card">
    <span class="badge">MÉTODO 1 (BASELINE)</span>
    <h3>CAM Clássico (Zhou et al., 2016)</h3>
    <p style="font-size: 14px; margin-bottom: 6px;">Requer camada GAP conectada diretamente à FC:</p>
    $$CAM^c(x, y) = \text{ReLU}\left( \sum_{k} w_k^c A^k(x, y) \right)$$
    <ul>
      <li><strong>Mecanismo:</strong> Projeção direta dos pesos da camada linear sobre os feature maps.</li>
      <li><strong>Limitação Clínica:</strong> Gera mapas extremamente <span class="accent">difusos e volumosos</span>, cobrindo tecido fibroso normal ao redor da massa.</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge">MÉTODO 2</span>
    <h3>Grad-CAM (Selvaraju et al., 2017)</h3>
    <p style="font-size: 14px; margin-bottom: 6px;">Ponderação via média dos gradientes de 1ª ordem:</p>
    $$\alpha_k^c = \frac{1}{Z} \sum_{i,j} \frac{\partial Y^c}{\partial A_{i,j}^k}, \quad L^c = \text{ReLU}\left( \sum_k \alpha_k^c A^k \right)$$
    <ul>
      <li><strong>Mecanismo:</strong> Não restringe a arquitetura (dispensa GAP exclusivo).</li>
      <li><strong>Comportamento:</strong> Concentra-se no "epicentro" da massa, mas pode subestimar margens espiculadas em lesões extensas.</li>
    </ul>
  </div>
</div>

---

<!-- Slide 8: CAMs Avançados - ++, XGrad e LayerCAM -->
<span class="speaker-badge">Integrante 2 • 09:30 - 11:00</span>

# Taxonomia dos Mapas de Ativação (2/2)
## Formulações Avançadas: Derivadas de Ordem Superior e Axiomas de Conservação

<div class="grid-3">
  <div class="card">
    <span class="badge">MÉTODO 3</span>
    <h3>Grad-CAM++</h3>
    <p style="font-size: 13px;">Chattopadhay et al. (2018)</p>
    <ul style="font-size: 14px;">
      <li>Utiliza derivadas parciais de <strong>2ª e 3ª ordem</strong>:
        $$w_k^c = \sum_{i,j} \alpha_{i,j}^{k,c} \text{ReLU}\left(\frac{\partial Y^c}{\partial A_{i,j}^k}\right)$$
      </li>
      <li>Pondera positivamente cada pixel da lesão.</li>
      <li><strong>Vantagem:</strong> Excelente na captura do contorno morfológico completo.</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge">MÉTODO 4</span>
    <h3>XGrad-CAM</h3>
    <p style="font-size: 13px;">Fu et al. (2020)</p>
    <ul style="font-size: 14px;">
      <li>Baseado em axiomas de <strong>Sensibilidade e Conservação</strong>:
        $$\alpha_k^c = \sum_{i,j} \frac{A_{i,j}^k}{\sum A^k} \cdot \frac{\partial Y^c}{\partial A_{i,j}^k}$$
      </li>
      <li>Gradientes escalados pela ativação normalizada.</li>
      <li><strong>Vantagem:</strong> Elimina ruídos em áreas de baixa ativação tecidual.</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge">MÉTODO 5</span>
    <h3>Layer-CAM</h3>
    <p style="font-size: 13px;">Jiang et al. (2021)</p>
    <ul style="font-size: 14px;">
      <li>Multiplicação elemento a elemento hierárquica:
        $$\hat{M}^k = \text{ReLU}\left(\frac{\partial Y^c}{\partial A_{i,j}^k}\right) \odot A^k$$
      </li>
      <li>Combina camadas rasas e profundas.</li>
      <li><strong>Problema Clínico:</strong> Hiper-reativo a glândulas sadias $\implies$ falso alarme.</li>
    </ul>
  </div>
</div>

---

<!-- Slide 9: A Teoria do Desacoplamento -->
<span class="speaker-badge">Integrante 2 • 11:00 - 12:30</span>

# A Teoria Científica do Desacoplamento
## Por que usar métodos distintos no Treino e no Teste?

<div class="grid-2">
  <div class="card-accent">
    <span class="badge">FASE DE TREINAMENTO: FILTRO SELETIVO</span>
    <h3 style="margin-top: 8px;">Objetivo: Pureza dos Patches</h3>
    <ul>
      <li>No treino, o CAM é usado para <strong>recortar patches</strong> para a ResNet-18 local.</li>
      <li>Se o CAM for disperso (ex: CAM padrão), ele recorta parênquima sadio rotulado como "massa".</li>
      <li><strong>O XGrad-CAM atua como um filtro cirúrgico:</strong> Seletivo e axiomático, garante que os patches contenham lesão tumoral real, treinando a rede local sem ruído.</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge">FASE DE INFERÊNCIA / TESTE: ENVOLTÓRIO</span>
    <h3 style="margin-top: 8px;">Objetivo: Cobertura da Bounding Box</h3>
    <ul>
      <li>No teste, o CAM deve gerar caixas delimitadoras com sobreposição $\text{IoU} \ge 0.3$.</li>
      <li>Se o CAM for pontual demais, a bounding box será diminuta e não cobrirá o tumor.</li>
      <li><strong>O Grad-CAM++ atua como um envelopador:</strong> Reage às derivadas de alta ordem e se expande sobre todo o halo da massa, atingindo $\text{IoU} \ge 0.3$.</li>
    </ul>
  </div>
</div>

<div class="card" style="margin-top: 10px; text-align: center; font-size: 16px;">
  <strong>Sinergia Perfeita:</strong> <span class="green">Treino com XGrad-CAM</span> (Patches Puros) &nbsp;+&nbsp; <span class="highlight">Teste com Grad-CAM++</span> (Cobertura Espacial).
</div>

---

<!-- Slide 10: Dataset VinDr-Mammo -->
<span class="speaker-badge">Integrante 2 • 12:30 - 13:45</span>

# Dataset VinDr-Mammo e Protocolo de Dados
## Benchmark Aberto de Alta Resolução e Balanceamento Experimental

<div class="grid-2">
  <div class="card">
    <h3>Estrutura do Benchmark VinDr-Mammo</h3>
    <ul>
      <li>5.000 exames mamográficos (20.000 imagens FFDM DICOM).</li>
      <li>4 projeções por paciente: <code>CC-D</code>, <code>CC-E</code>, <code>MLO-D</code>, <code>MLO-E</code>.</li>
      <li>Resolução nativa gigantesca: $2944 \times 1920$ pixels em escala de cinza 16-bit.</li>
      <li>Anotações independentes com consenso de radiologistas seniores certificados.</li>
    </ul>
  </div>
  <div class="card-accent">
    <h3>Protocolo de Isolamento de Supervisão</h3>
    <ul>
      <li><strong>Divisão Balanceada:</strong>
        <ul>
          <li><strong>Treino:</strong> 1.978 imagens (989 Normais, 989 Massas).</li>
          <li><strong>Teste:</strong> 474 imagens (237 Normais, 237 Massas).</li>
        </ul>
      </li>
      <li><span class="accent">Isolamento Rigoroso de Coordenadas:</span> Bounding boxes foram completamente ocultadas no treino, sendo acessadas <strong>apenas no teste para cálculo de IoU</strong>.</li>
      <li><strong>Augmentations:</strong> Flip horizontal ($p=0.5$), corte estocástico e normalização z-score.</li>
    </ul>
  </div>
</div>

---

<!-- Slide 11: Engenharia de Software PyTorch -->
<span class="speaker-badge">Integrante 2 • 13:45 - 15:00</span>

# Arquitetura de Software Modular em PyTorch
## Estrutura Orientada a Objetos na pasta `Trabalho 3 (Final)/src/`

<div class="grid-2">
  <div class="card">
    <span class="badge">TOPOLOGIA MODULAR</span>
    <ul style="font-size: 14px; margin-top: 8px;">
      <li><code>config.py</code>: Hiperparâmetros, resolução, batch, $\beta=3.26$.</li>
      <li><code>datasets/vindr_mammo.py</code>: Parser Albumentations, XML/CSV.</li>
      <li><code>models/backbones.py</code>: ResNet-22 global e ResNet-18 local.</li>
      <li><code>models/gmic.py</code>: Rede integrada GMIC e módulo de fusão.</li>
      <li><code>models/losses.py</code>: Multi-branch BCE + regularização L1.</li>
      <li><code>cams/cam_manager.py</code>: Interface desacoplada dos 5 CAMs.</li>
      <li><code>evaluation/metrics.py</code>: AUC, IoU $\ge 0.3$, FPPI e FROC.</li>
      <li><code>train.py</code> & <code>test.py</code>: CLI completa e checkpoints.</li>
    </ul>
  </div>
  <div class="card-accent">
    <span class="badge">EXTRATOR GULOSO DE PATCHES</span>
    <pre style="background: #020617; padding: 10px; border-radius: 6px; font-size: 12px; color: #38bdf8; overflow-x: auto;">
class GreedyPatchExtractor(nn.Module):
    def forward(self, img, cam_map):
        for _ in range(self.num_patches):
            max_idx = torch.argmax(cam_map)
            cy, cx = max_idx // W, max_idx % W
            patch = extract_patch(img, cy, cx)
            cam_map[suppress_region] = -1.0
        return torch.stack(patches)
    </pre>
    <p style="font-size: 13px; color: #94a3b8; margin-top: 4px;">Supressão espacial impede sobreposição de patches.</p>
  </div>
</div>

---

<!-- Slide 12: Soluções de Engenharia para Hardware -->
<span class="speaker-badge">Integrante 2 • 15:00 - 16:30</span>

# Adaptações Computacionais para Restrições de GPU
## Como viabilizar imagens de alta resolução mantendo equivalência metodológica

<div class="grid-2">
  <div class="card-danger">
    <h3>O Gargalo de Memória</h3>
    <ul>
      <li>Processar batch de 6 imagens de $2944 \times 1920$ com 6 patches locais de $256 \times 256$ requer $> 18\text{ GB}$ de VRAM.</li>
      <li>GPUs convencionais ou de laboratório enfrentam erro crítico de <code>CUDA Out of Memory</code>.</li>
    </ul>
  </div>
  <div class="card-accent">
    <h3>Soluções de Engenharia Implementadas</h3>
    <ul>
      <li><strong>Automatic Mixed Precision (AMP):</strong> <code>torch.cuda.amp</code> com autocast em FP16 $\implies$ economia de 45% na VRAM e aceleração de treino.</li>
      <li><strong>Gradient Accumulation (3 passos):</strong>
        $$\text{Batch Físico (2)} \times 3 \text{ passos} \implies \text{Batch Virtual Exato} = 6$$
        Garante fidelidade estatística ao artigo original.</li>
    </ul>
  </div>
</div>

<div class="card-accent" style="margin-top: 10px; font-size: 15px;">
  <em>Transição: "Para apresentar a validação de detecção, os resultados das Tabelas 1 e 2 e a errata técnica, passo a palavra ao Integrante 3."</em>
</div>

---

<!-- Slide 13: Protocolo Experimental e Detecção WSOD -->
<span class="speaker-badge">Integrante 3 • 16:30 - 17:45</span>

# Avaliação de Detecção Fracamente Supervisionada
## Binarização por Limiar, Extração de Bounding Boxes e Critério de Acerto Clínico

<div class="grid-2">
  <div class="card">
    <span class="badge">PIPELINE DE LOCALIZAÇÃO</span>
    <ul>
      <li>Avaliação executada sobre as <strong>237 imagens de teste com massa</strong>.</li>
      <li>Binarização do mapa de calor $A^c(x, y)$ por limiar $\tau$:
        $$\mathcal{M}_{bin}(x, y) = \mathbb{I}(A^c(x, y) \ge \tau)$$
      </li>
      <li>Componentes conexos geram as caixas preditas $\mathcal{B}_{pred}$.</li>
    </ul>
  </div>
  <div class="card-accent">
    <span class="badge">CRITÉRIO CLÍNICO DE SUCESSO</span>
    <h3>IoU $\ge 0.3$ e FPPI</h3>
    $$\text{IoU}(B_{pred}, B_{gt}) = \frac{\text{Área}(B_{pred} \cap B_{gt})}{\text{Área}(B_{pred} \cup B_{gt})} \ge 0.3$$
    <ul>
      <li><strong>TPR (Sensibilidade):</strong> Fração de tumores reais detectados.</li>
      <li><strong>FPPI:</strong> Média de falsos alarmes por exame radiológico.</li>
      <li><strong>Por que IoU 0.3 e não 0.5?</strong> Massas neoplásicas possuem margens difusas e infiltrativas sem bordas rígidas.</li>
    </ul>
  </div>
</div>

---

<!-- Slide 14: Resultados da Classificação Global -->
<span class="speaker-badge">Integrante 3 • 17:45 - 19:00</span>

# Resultados da Classificação Global no VinDr-Mammo
## Desempenho no Nível de Imagem (Tabela 1 do Artigo Original)

<div class="card">
  <table>
    <thead>
      <tr>
        <th>Modelo / Configuração</th>
        <th>Acurácia (%)</th>
        <th>AUC-ROC (%)</th>
        <th>TPR / Sensibilidade (%)</th>
        <th>Especificidade / TNR (%)</th>
      </tr>
    </thead>
    <tbody>
      <tr class="highlight-row">
        <td><strong>GMIC (Sampaio & Cordeiro / Reprodução)</strong></td>
        <td><strong>80,12%</strong></td>
        <td><strong>87,22%</strong></td>
        <td><strong>71,88%</strong></td>
        <td><strong>88,52%</strong></td>
      </tr>
      <tr>
        <td>Baseline Apenas Global (ResNet-22)</td>
        <td>76,45%</td>
        <td>82,10%</td>
        <td>66,24%</td>
        <td>83,90%</td>
      </tr>
      <tr>
        <td>Baseline Apenas Local (Patches Aleatórios)</td>
        <td>69,30%</td>
        <td>74,80%</td>
        <td>58,15%</td>
        <td>78,40%</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="grid-2" style="margin-top: 14px;">
  <div class="card-accent">
    <h3>Conclusão do Nível de Imagem</h3>
    <p style="font-size: 15px;">A integração dos três ramos (Global + Local + Fusão) eleva a AUC para <strong>87,22%</strong>, superando modelos que utilizam visão global ou recortes locais isolados.</p>
  </div>
  <div class="card">
    <h3>Capacidade Discriminativa</h3>
    <p style="font-size: 15px;">A alta especificidade (88,52%) garante que mamas saudáveis não sejam incorretamente encaminhadas para biópsias invasivas.</p>
  </div>
</div>

---

<!-- Slide 15: Tabela Comparativa de Detecção WSOD -->
<span class="speaker-badge">Integrante 3 • 19:00 - 20:30</span>

# Tabela Mestra de Detecção WSOD ($\text{TPR} @ \text{FPPI}$)
## Comparação Sistemática das Combinações de Desacoplamento Treino/Teste

<div class="card">
  <table>
    <thead>
      <tr>
        <th>Método no Treino</th>
        <th>Teste: CAM</th>
        <th>Teste: GradCAM</th>
        <th>Teste: GradCAM++</th>
        <th>Teste: XGradCAM</th>
        <th>Teste: LayerCAM</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>GMIC (CAM)</strong> [Baseline]</td>
        <td>0.69 @ 1.55</td>
        <td>0.60 @ 0.63</td>
        <td>0.67 @ 1.43</td>
        <td>0.68 @ 1.05</td>
        <td>0.68 @ 1.62</td>
      </tr>
      <tr>
        <td><strong>GMIC (GradCAM++)</strong></td>
        <td>0.71 @ 2.89</td>
        <td>0.13 @ 0.06</td>
        <td>0.65 @ 1.12</td>
        <td>0.13 @ 0.06</td>
        <td>0.67 @ 1.59</td>
      </tr>
      <tr class="highlight-row">
        <td><strong>GMIC (XGradCAM)</strong> [Campeão]</td>
        <td>0.64 @ 0.75</td>
        <td>0.60 @ 0.43</td>
        <td><strong>0.70 @ 0.88 🏆</strong></td>
        <td>0.60 @ 0.42</td>
        <td><span class="accent">0.72 @ 4.19 ⚠️</span></td>
      </tr>
    </tbody>
  </table>
</div>

<div class="grid-2" style="margin-top: 12px;">
  <div class="card-accent">
    <h3 style="color: #10b981;">Modelo Campeão Desacoplado 🏆</h3>
    <p style="font-size: 14px;"><strong>GMIC(XGradCAM) com Teste em GradCAM++:</strong> Atinge TPR de <strong>0.70</strong> com queda expressiva nos falsos positivos para <strong>0.88 FPPI</strong> (redução de 43,2% em relação ao baseline de 1.55).</p>
  </div>
  <div class="card-danger">
    <h3 style="color: #f43f5e;">O Colapso do Layer-CAM ⚠️</h3>
    <p style="font-size: 14px;">Embora obtenha TPR marginalmente maior (0.72), gera <strong>4.19 falsos alarmes por imagem</strong>, inviabilizando qualquer aplicação médica real de triagem.</p>
  </div>
</div>

---

<!-- Slide 16: Análise Qualitativa dos Mapas de Calor -->
<span class="speaker-badge">Integrante 3 • 20:30 - 21:45</span>

# Análise Visual Qualitativa dos Mapas de Calor
## Comportamento Espacial dos Métodos sobre Mamografias Reais do Teste

<div class="grid-3">
  <div class="card">
    <span class="badge">CAM PADRÃO</span>
    <h3 style="margin-top: 6px;">Difuso & Ruídos</h3>
    <ul>
      <li>Manchas espalhadas pelo parênquima mamário sadio.</li>
      <li>Gera caixas gigantescas com baixa precisão espacial.</li>
      <li>FPPI elevado (1.55).</li>
    </ul>
  </div>
  <div class="card">
    <span class="badge">GRAD-CAM</span>
    <h3 style="margin-top: 6px;">Hiper-Concentrado</h3>
    <ul>
      <li>Ativa apenas o ponto central de maior contraste.</li>
      <li>Subestima espículas e bordas neoplásicas.</li>
      <li>Perde o limiar $\text{IoU} \ge 0.3$.</li>
    </ul>
  </div>
  <div class="card-accent">
    <span class="badge">XGRAD + GRAD++ 🏆</span>
    <h3 style="margin-top: 6px;">Equilíbrio Ótimo</h3>
    <ul>
      <li>Núcleo limpo sem ativações falsas na periferia.</li>
      <li>Halo contínuo que cobre o ground truth verde.</li>
      <li>Bounding box atinge $\text{IoU} \ge 0.45$.</li>
    </ul>
  </div>
</div>

<div class="card" style="margin-top: 12px; font-size: 14px;">
  <strong>Interpretação Radiológica:</strong> O radiologista visualiza uma indicação focada e limpa sobre a lesão suspeita, sem distrações causadas por múltiplos alarmes falsos em áreas de tecido mamário fibroso normal.
</div>

---

<!-- Slide 17: Errata Técnica Identificada -->
<span class="speaker-badge">Integrante 3 • 21:45 - 22:45</span>

# Análise Crítica e Errata Técnica Identificada
## Demonstração Analítica da Inconsistência na Tabela 1 do Artigo Original

<div class="card-danger">
  <h3>Inconsistência Observada na Tabela 1 de Sampaio & Cordeiro</h3>
  <p style="font-size: 15px; margin-bottom: 6px;">No artigo original, a 4ª coluna da Tabela 1 é denominada <strong>"FNR" (Taxa de Falsos Negativos)</strong> com o valor de <strong>88,52%</strong>.</p>
</div>

<div class="grid-2" style="margin-top: 12px;">
  <div class="card">
    <span class="badge">DEDUÇÃO MATEMÁTICA</span>
    $$\text{TPR} = \frac{VP}{VP + FN} = 71,88\%$$
    $$\text{FNR} = \frac{FN}{VP + FN} = 1 - \text{TPR}$$
    $$\text{FNR}_{real} = 100\% - 71,88\% = \mathbf{28,12\%}$$
  </div>
  <div class="card-accent">
    <span class="badge">CORREÇÃO TÉCNICA DO TRIO</span>
    <p style="font-size: 15px;">O valor reportado de <strong>88,52%</strong> corresponde, na realidade, à <strong>Taxa de Verdadeiros Negativos (TNR / Especificidade)</strong>:</p>
    $$\text{TNR} = \frac{VN}{VN + FP} = 88,52\%$$
    <p style="font-size: 14px; color: #10b981; margin-top: 6px;">Documentamos formalmente esta errata em nosso relatório SBC, evidenciando domínio matemático.</p>
  </div>
</div>

---

<!-- Slide 18: Viabilidade Clínica -->
<span class="speaker-badge">Integrante 3 • 22:45 - 23:30</span>

# Viabilidade Clínica e Trade-Offs de Detecção
## Por que 0.88 FPPI é Aceitável e 4.19 FPPI é Inutilizável?

<div class="grid-2">
  <div class="card-accent">
    <h3>O Cenário Clínico Hospitalar</h3>
    <ul>
      <li>Um programa de rastreamento avalia de <strong>100 a 300 mamografias/dia</strong> por especialista.</li>
      <li>Com <strong>0.88 FPPI</strong> (GMIC XGrad-Grad++), o radiologista encontra menos de 1 falso alarme por exame — tolerável como checagem visual.</li>
      <li>Reduz o tempo de leitura e previne a omissão diagnóstica de carcinomas ocultos.</li>
    </ul>
  </div>
  <div class="card-danger">
    <h3>A Fadiga do Alarme Falso</h3>
    <ul>
      <li>Com <strong>4.19 FPPI</strong> (Layer-CAM), o médico recebe mais de 4 caixas falsas em cada exame normal!</li>
      <li>Gera perda total de credibilidade no sistema CAD.</li>
      <li>Causa estresse, aumento de tempo de análise e risco de biópsias desnecessárias.</li>
    </ul>
  </div>
</div>

<div class="card" style="margin-top: 10px; font-size: 15px; text-align: center;">
  <strong>Conclusão Técnica:</strong> A métrica isolada de TPR não define um sistema CAD. A relação $\text{TPR} / \text{FPPI}$ é o verdadeiro critério de viabilidade médica.
</div>

---

<!-- Slide 19: Conclusões e Trabalhos Futuros -->
<span class="speaker-badge">Integrante 3 • 23:30 - 24:30</span>

# Conclusões, Lições Aprendidas e Próximos Passos
## Fechamento da Reprodução Científica do Trabalho Final

<div class="grid-2">
  <div class="card-accent">
    <h3>Conclusões da Reprodução</h3>
    <ul>
      <li><span class="green">Reprodutibilidade Confirmada:</span> O desacoplamento de CAMs é uma contribuição sólida para WSOD médico.</li>
      <li><strong>XGrad-CAM no Treino:</strong> Assegura patches de alta pureza patológica.</li>
      <li><strong>Grad-CAM++ no Teste:</strong> Maximiza o $\text{IoU} \ge 0.3$, reduzindo FPPI em 43,2%.</li>
      <li><strong>Engenharia Eficiente:</strong> AMP e Gradient Accumulation tornam viável o treinamento em hardware acessível.</li>
    </ul>
  </div>
  <div class="card">
    <h3>Direções Futuras de Pesquisa</h3>
    <ul>
      <li>Investigar <strong>Vision Transformers (ViTs)</strong> e mecanismos de Cross-Attention para substituir a ResNet.</li>
      <li>Pré-treinamento auto-supervisionado com <strong>Masked Autoencoders (MAE)</strong> em mamografias não anotadas.</li>
      <li>Adaptação para detecção de <strong>microcalcificações agrupadas</strong> além de massas.</li>
    </ul>
  </div>
</div>

---

<!-- Slide 20: Agradecimentos e Q&A -->
<span class="speaker-badge">Trio Reunido • 24:30 - 30:00</span>

# Agradecimentos e Sessão de Perguntas (Q&A)
## Estamos abertos à avaliação e arguição da banca examinadora

<div class="grid-2" style="margin-top: 20px;">
  <div class="card-accent">
    <span class="badge">REPOSITÓRIO E ENTREGÁVEIS</span>
    <p style="margin-top: 10px; font-size: 15px;">
      <strong>Código Modular PyTorch:</strong> <code>src/</code><br>
      <strong>Artigo Científico SBC (LaTeX):</strong> <code>docs/relatorio_sbc/</code><br>
      <strong>Apresentação & Roteiro Oral:</strong> <code>slide/</code>
    </p>
    <p style="font-size: 14px; color: #94a3b8; margin-top: 12px;">
      Disciplina de Tópicos Especiais em Visão Computacional<br>
      <strong>Universidade Federal do Piauí (UFPI)</strong>
    </p>
  </div>
  <div class="card">
    <span class="badge">EQUIPE GRUPO 4</span>
    <ul style="list-style: none; padding-left: 0; margin-top: 10px; font-size: 15px;">
      <li><strong>Integrante 1:</strong> Introdução Clínica & Arquitetura GMIC</li>
      <li><strong>Integrante 2:</strong> CAMs & Engenharia PyTorch</li>
      <li><strong>Integrante 3:</strong> Experimentos, Detecção WSOD & Errata</li>
    </ul>
    <div style="margin-top: 14px; text-align: center; color: #38bdf8; font-weight: bold; font-size: 18px;">
      Obrigado pela atenção!
    </div>
  </div>
</div>
