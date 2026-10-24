# Análise de Riscos Técnicos e Plano de Contingência

> **Projeto**: Reprodução Científica do Modelo GMIC em WSOD Mamográfico  
> **Disciplina**: Tópicos Especiais em Visão Computacional (UFPI / 2026.2)  
> **Finalidade**: Mapear vulnerabilidades computacionais, metodológicas e operacionais, estabelecendo salvaguardas e planos de contingência para assegurar a obtenção de nota máxima em todos os eixos de avaliação.

---

## 1. Matriz de Mapeamento e Severidade de Riscos

```mermaid
quadrantChart
    title Matriz de Risco do Projeto
    x-axis Baixo Impacto --> Alto Impacto
    y-axis Baixa Probabilidade --> Alta Probabilidade
    quadrant-1 Monitorar e Agir Rapidamente
    quadrant-2 Risco Crítico: Mitigação Obrigatória
    quadrant-3 Risco Baixo: Tolerável
    quadrant-4 Risco Latente: Contingência Preparada
    "Estouro de VRAM (OOM)": [0.85, 0.85]
    "Tempo Excessivo de Treino": [0.75, 0.70]
    "Divergência Numérica de Métricas": [0.60, 0.65]
    "Falha de Conexão na Apresentação": [0.90, 0.35]
    "Inadequação ao Limite de Páginas SBC": [0.55, 0.40]
```

---

## 2. Riscos Técnicos e Computacionais

### 2.1. Risco 1: Estouro de Memória de Vídeo da GPU (*Out Of Memory - OOM*)
- **Natureza do Problema**:  
  O pipeline do GMIC processa mamografias de resolução ultra-alta ($2944 \times 1920$) em batch size de 6, combinando a extração convolucional da ResNet-22 com a propagação de $K=6$ patches de $256 \times 256$ na ResNet-18 e os grafos de retropropagação das 3 perdas mais os gradientes de CAM. Essa configuração ultrapassa facilmente **18 GB a 22 GB de VRAM**, gerando erro fatal de `CUDA out of memory` em GPUs comuns (RTX 3060/4060 locais de 8-12 GB ou Tesla T4 gratuita do Colab de 15 GB).
- **Probabilidade**: Alta | **Impacto**: Crítico
- **Plano de Contingência e Mitigação**:
  1. **Acumulação de Gradientes (*Gradient Accumulation*)**:
     - Configurar batch físico de **2 imagens** com acumulação por **3 passos** (`accum_steps = 3`).
     - Matematicamente, os gradientes são somados antes de atualizar os pesos, replicando a trajetória estocástica exata do batch size 6 sem sobrecarregar a memória física.
  2. **Precisão Mista Automática (*Automatic Mixed Precision - AMP*)**:
     - Utilizar `torch.cuda.amp.autocast(dtype=torch.float16)` e `torch.cuda.amp.GradScaler`.
     - Economiza entre 40% e 50% de VRAM por meio de representação em ponto flutuante de 16 bits nas ativações intermediárias.
  3. **Redimensionamento Proporcional Seguro (*Aspect-Ratio Aware Scaling*)**:
     - Caso o ambiente computacional disponha de GPU com menos de 10 GB de VRAM, realizar downsampling proporcional controlado para $1472 \times 960$ ou $1024 \times 768$ acompanhado de *zero-padding*.
     - *Justificativa Científica*: Documentar no relatório da SBC que a escala proporcional manteve a morfologia das espículas das lesões e o cálculo proporcional do IoU.

---

### 2.2. Risco 2: Custo Temporal Prolongado de Treinamento
- **Natureza do Problema**:  
  Treinar 50 épocas sobre 1.978 imagens com múltiplos ramos pode demandar entre 12 e 24 horas ininterruptas de processamento. Sessões do Google Colab frequentemente desconectam após 4 a 6 horas por inatividade ou timeout de GPU.
- **Probabilidade**: Alta | **Impacto**: Alto
- **Plano de Contingência e Mitigação**:
  1. **Transferência de Aprendizado (*Transfer Learning*)**:
     - Inicializar os pesos dos backbones ResNet-22 e ResNet-18 com pré-treinamento da base *NYU Breast Cancer Screening Dataset* ou ImageNet modificado. Isso reduz o número de épocas necessárias para convergência de 50 para aproximadamente 20 a 30 épocas.
  2. **Checkpointing Atômico Automatizado**:
     - Salvar pesos e estado do otimizador a cada 2 épocas em arquivo `.pth` sincronizado diretamente com Google Drive / armazenamento em nuvem.
     - Em caso de desconexão, o script retoma exatamente da última época concluída via flag `--resume`.
  3. **Critério de Parada Prematura (*Early Stopping*)**:
     - Monitorar o AUC de validação. Se o ganho após 5 épocas for menor que 0.001, interromper o treino e salvar o melhor modelo.

---

## 3. Riscos Metodológicos e Científicos

### 2.3. Risco 3: Divergência Numérica nas Métricas de Detecção WSOD
- **Natureza do Problema**:  
  Diferenças sutis na implementação da biblioteca de CAM (ex.: versão do `pytorch-grad-cam`), sementes estocásticas de inicialização dos pesos ou interpolações de downsampling podem produzir valores de TPR e FPPI ligeiramente discrepantes daqueles reportados na Tabela 2 de Sampaio & Cordeiro (ex.: obter TPR de 0.68 em vez de 0.70 ou FPPI de 0.95 em vez de 0.88).
- **Probabilidade**: Moderada | **Impacto**: Moderado
- **Plano de Contingência e Mitigação**:
  1. **Determinismo Numérico**:
     - Fixar sementes globais no início dos scripts:
       ```python
       torch.manual_seed(42)
       np.random.seed(42)
       torch.backends.cudnn.deterministic = True
       ```
  2. **Foco na Validação da Hipótese Relativa**:
     - O rigor acadêmico da Modalidade 2 não exige que os números sejam idênticos até a terceira casa decimal, mas sim que a **tendência científica e a superioridade da hipótese de desacoplamento** sejam comprovadas (ou seja, comprovar que o par XGrad-CAM no treino e Grad-CAM++ no teste reduz significativamente o FPPI em relação ao CAM tradicional).
  3. **Valorização Acadêmica da Divergência no Relatório SBC**:
     - Na Seção 5 do artigo, detalhar formalmente as causas técnicas das variações observadas (arquitetura de GPU, bibliotecas, hiperparâmetros de threshold). O docente valoriza a capacidade analítica e crítica do grupo em justificar discrepâncias em vez de mascarar dados.

---

## 4. Riscos Editoriais e de Formatação do Relatório SBC

### 2.4. Risco 4: Extrapolação ou Insuficiência de Páginas (Faixa: 8 a 12 páginas)
- **Natureza do Problema**:  
  O edital impõe limite estrito de **8 a 12 páginas**. Escrever menos de 8 páginas denota superficialidade científica; exceder 12 páginas viola o edital da SBC e acarreta perda imediata de nota no critério "Estrutura e organização (0,75 pt)".
- **Probabilidade**: Média | **Impacto**: Alto
- **Plano de Contingência e Mitigação**:
  1. **Agrupamento Eficiente de Figuras via `subcaption`**:
     - Reunir os heatmaps dos 5 métodos de CAM e a imagem original em uma única figura modular com subfiguras `(a)`, `(b)`, `(c)`, `(d)`, economizando cerca de 1,5 página.
  2. **Tabelas Compactas no Padrão `booktabs`**:
     - Estruturar a comparação entre artigo original e reprodução em uma tabela única de dupla entrada, evitando tabelas fragmentadas redundantes.
  3. **Revisão de Extensão no Overleaf**:
     - Monitorar o número de páginas a cada nova seção redigida. Se o texto atingir 11 páginas, iniciar síntese das discussões para fechar em exatamente 11 a 12 páginas com as referências.

---

## 5. Riscos Operacionais e de Apresentação Oral (Data: 07/12)

### 2.5. Risco 5: Falha Técnica ou Ausência Repentina de Integrante no Dia da Apresentação
- **Natureza do Problema**:  
  Como a apresentação é síncrona e online, panes na conexão de internet, corte de energia elétrica ou emergências de saúde podem afetar um dos integrantes do trio.
- **Probabilidade**: Média | **Impacto**: Crítico (50% da nota)
- **Plano de Contingência e Mitigação**:
  1. **Protocolo Oficial de Substituição Instantânea**:
     - Conforme regra expressa do edital do Prof. José Denes: *"Se um integrante faltar, os demais do grupo devem apresentar a parte do integrante que faltou"*.
     - Todos os três integrantes devem dominar o roteiro completo dos slides (Slides 1 ao 19). Se o apresentador da vez sofrer pane, o colega imediatamente seguinte assume a fala em menos de 5 segundos, sem interrupção do compartilhamento de tela.
  2. **Espelhamento e Nuvem**:
     - Slides salvos simultaneamente em PDF local nos três computadores e hospedados no Google Slides com acesso compartilhado.
  3. **Conexão Redundante de Emergência**:
     - Cada membro deve deixar o pacote de dados do telefone celular (4G/5G) configurado como ponto de acesso móvel (*tethering*) para uso imediato em caso de queda da banda larga fixa.
  4. **Ensaio Técnico Prévio**:
     - Realizar ensaio geral do trio no Google Meet 24 horas antes (em 06/12), cronometrando a apresentação e testando áudio, vídeo e troca de tela.

---

## 6. Risco de Penalidade por Falta nas Apresentações dos Demais Grupos

> [!WARNING]
> **Penalidade Institucional Formal**: O edital prevê desconto de **-1,0 ponto** na média final para qualquer estudante que faltar às sessões de apresentação dos outros grupos sem justificativa formal.

- **Mitigação**:
  - Inclusão de todos os dias de apresentação no calendário pessoal com alarmes sonoros:
    - **07/12 (segunda)**: Grupos 1, 3 e **4 (Nosso Grupo)**;
    - **10/12 (quinta)**: Grupos 5 e 6;
    - **14/12 (segunda)**: Grupos 8 e 9.
  - Presença registrada desde o início até o término de cada sessão.
