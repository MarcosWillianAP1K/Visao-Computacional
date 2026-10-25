# Guia Visual, Operacional e de Exportação de Slides
## Trabalho 2: Tópicos Especiais em Visão Computacional — UFPI | Prof. Dr. José Denes Lima Araújo
### Grupo 4: CNN Leve (UFCSPA) vs. Vision Transformers Dinâmicos (PUC Minas / UFMG)

---

## 1. Visão Geral dos Arquivos Disponíveis

Na pasta `Trabalho 2\slide\`, você encontrará os arquivos completos e prontos para a apresentação:

1. **`apresentacao_trabalho_2.pptx` (ou `slides.pptx`)**: Apresentação nativa em formato **PowerPoint** (16:9 widescreen) contendo os 26 slides estilizados no tema Dark Tech, com tabelas de métricas, cards, marcadores e **Notas do Orador (*Speaker Notes*)** embutidas nativamente em cada slide. Pronto para abrir no Microsoft PowerPoint ou no **Google Apresentações (Google Slides)**.
2. **`ROTEIRO_FALA_TRIO.md`**: Guia verbal completo com as falas exatas, marcações de tempo minuto a minuto (00:00 a 34:30), transições formais entre os três alunos e estratégia de arguição para a banca.
3. **`slides.md`**: Apresentação formatada para a ferramenta Marp / Markdown contendo a íntegra dos textos e notas.
4. **`GUIA_VISUAL_E_EXPORTACAO.md`** *(este documento)*: Instruções práticas para operar os slides no PowerPoint / Google Slides e no dia da defesa online.

---

## 2. Como Utilizar no PowerPoint ou Google Apresentações

### 2.1. No Google Apresentações (Google Slides)
1. Acesse o [Google Drive](https://drive.google.com).
2. Clique em **`+ Novo`** > **`Upload de arquivo`** e selecione o arquivo `apresentacao_trabalho_2.pptx`.
3. Dê um duplo clique no arquivo carregado e clique em **"Abrir com o Apresentações Google"**.
4. Para ver as notas de fala de cada aluno durante o ensaio ou apresentação, clique em **`Exibir`** > **`Mostrar notas do orador`** (ou utilize o **Modo Apresentador** ao projetar).

### 2.2. No Microsoft PowerPoint
1. Dê um duplo clique no arquivo `apresentacao_trabalho_2.pptx`.
2. Para apresentar em tela cheia, pressione **`F5`** (ou **`Shift + F5`** para o slide atual).
3. No modo de exibição do apresentador (**Modo Apresentador**), as anotações completas de fala do integrante aparecerão automaticamente na tela secundária ao lado do slide.

### 2.3. O Cronômetro Inteligente com Detecção de Apresentador
O widget no topo do slide monitora automaticamente o tempo transcorrido e atualiza o crachá do apresentador daquele instante:
- **`00:00 a 11:30`**: `[Aluno 1] Abertura & CNN` (Borda ciano)
- **`11:30 a 23:00`**: `[Aluno 2] ViTs Dinâmicos` (Borda roxa)
- **`23:00 a 34:30`**: `[Aluno 3] Comparação & Crítica` (Borda esmeralda)
- **`34:30 a 40:00`**: `[Trio] Arguição da Banca` (Borda âmbar)
- **`> 40:00`**: `TEMPO EXCEDIDO (>40 min)` (Alerta vermelho piscante)

---

## 3. Como Apresentar no Google Meet com Notas do Orador

Para apresentar no Google Meet mantendo suas anotações de fala visíveis sem que a banca as veja:

### Opção A: Configuração com Dois Monitores (Ideal)
1. Conecte um segundo monitor (ou notebook + monitor externo).
2. Abra o `slides.html` no Monitor 1 em tela cheia (`F`) e compartilhe **apenas essa tela** ou janela no Google Meet.
3. Abra o arquivo `ROTEIRO_FALA_TRIO.md` no Monitor 2 para leitura e acompanhamento contínuo dos tempos.

### Opção B: Monitor Único (Apresentando Janela ou Aba)
1. No Google Meet, clique em **Apresentar agora** ➔ **Uma janela** (ou **Uma guia**).
2. Selecione a janela do navegador com o `slides.html`.
3. Pressione a tecla **`N`** no `slides.html` para abrir a gaveta de notas lateral enquanto apresenta, ou mantenha a janela do Meet em meia-tela e o roteiro na outra metade.

---

## 4. Como Exportar para PDF

Caso o Prof. Dr. José Denes solicite o envio do arquivo dos slides em formato PDF antes ou depois da defesa:

### Método 1: Exportação Direta pelo Navegador (Recomendado - 10 Segundos)
1. Abra o arquivo `slides.html` no Google Chrome ou Microsoft Edge.
2. Pressione **`Ctrl + P`** (Imprimir).
3. No campo **Destino**, escolha **Salvar como PDF**.
4. Configure as seguintes opções:
   - **Layout:** *Paisagem (Landscape)*
   - **Páginas:** *Todas*
   - **Tamanho do papel:** *A4* ou *Letter*
   - **Margens:** *Nenhuma (None)*
   - **Mais definições ➔ Opções:** Marque a caixa **"Gráficos de segundo plano" (Background graphics)** *(obrigatório para manter o tema escuro)*.
5. Clique em **Salvar** e salve como `Apresentacao_Grupo4_Trabalho2.pdf`.

### Método 2: Exportação via Marp CLI (A partir do `slides.md`)
Caso possua o Node.js instalado na máquina, execute no terminal:
```bash
npx @marp-team/marp-cli "c:\Users\MWSS\OneDrive\Desktop\Visao Computacional\Trabalho 2\slide\slides.md" --pdf -o "c:\Users\MWSS\OneDrive\Desktop\Visao Computacional\Trabalho 2\slide\slides.pdf" --allow-local-files
```

### Método 3: Extensão "Marp for VS Code"
1. Instale a extensão oficial **Marp for VS Code** no VS Code.
2. Abra o arquivo `slides.md`.
3. Clique no ícone do Marp no canto superior direito e selecione **Export slide deck...** ➔ **PDF**.

---

## 5. Como Importar para Google Slides, PowerPoint ou Canva

Se algum membro do grupo preferir apresentar pelo Google Slides ou PowerPoint:

### Importar no Google Slides / PowerPoint via PDF
1. Exporte a apresentação para PDF pelo Método 1 acima.
2. Acesse uma ferramenta gratuita de conversão como o [IlovePDF PDF to PPTX](https://www.ilovepdf.com/pdf_to_powerpoint).
3. Converta o PDF para `.pptx` e abra diretamente no **Microsoft PowerPoint** ou importe no **Google Slides** (*Arquivo ➔ Importar slides*).

### Importar no Canva
1. Acesse sua conta no [Canva](https://www.canva.com).
2. No painel inicial, clique em **Criar um design** ➔ **Importar arquivo**.
3. Selecione o arquivo `slides.pdf` gerado. O Canva importará todos os 26 slides mantendo os layouts, fontes, caixas e cores 100% editáveis.

---

## 6. Identidade Visual e Design System

Os slides foram construídos sob os mais modernos preceitos de design de apresentações científicas de Aprendizado Profundo (*Deep Learning Tech Aesthetics*):

### 6.1. Paleta de Cores Hexadecimal

```
┌─────────────────┬───────────┬────────────────────────────────────────────────────────┐
│ NOME DA COR     │ CÓDIGO HEX│ FUNÇÃO SEMÂNTICA NO SLIDE                              │
├─────────────────┼───────────┼────────────────────────────────────────────────────────┤
│ Deep Space Dark │ #090d16   │ Fundo principal (Background global com radial glow).    │
│ Slate Glass     │ #0f172a   │ Superfície dos cartões (Cards com bordas sutis).       │
│ Cyan Electric   │ #38bdf8   │ Destaques do Artigo 1 (UFCSPA, CNN, Grad-CAM, Acurácia).│
│ Indigo Purple   │ #818cf8   │ Destaques do Artigo 2 (PUC Minas, ViT, Autoatenção).   │
│ Emerald Green   │ #34d399   │ Resultados positivos, conclusões e métricas vencedoras.│
│ Amber Gold      │ #f59e0b   │ Problemas detectados, hipóteses dinâmicas e atenção.  │
│ Rose Crimson    │ #f43f5e   │ Células de carcinoma (SCC) e aviso de tempo limite.   │
│ Pure White      │ #f8fafc   │ Títulos primários e números de métricas de alto relevo. │
│ Slate Text      │ #cbd5e1   │ Texto descritivo e marcadores analíticos de leitura.   │
│ Muted Slate     │ #94a3b8   │ Metadados, rodapés e legendas de figuras.             │
└─────────────────┴───────────┴────────────────────────────────────────────────────────┘
```

### 6.2. Tipografia e Legibilidade
- **Fontes Primárias de Texto e Título:** `Inter`, `-apple-system`, `Segoe UI`, `Roboto` (alta legibilidade em telas compartilhadas em resolução 1080p ou 720p).
- **Fontes de Código, Fórmulas e Arquitetura:** `JetBrains Mono`, `Fira Code`, `monospace` (monoespaçada com alto contraste para matrizes e operações de tensores).
- **Relação de Contraste:** Todos os textos possuem contraste superior a **7:1**, atendendo ao padrão de acessibilidade visual **WCAG AAA**.

---

## 7. Recomendações de Ensaio para o Trio

1. **Façam pelo Menos 2 Ensaios Completos Cronometrados:**  
   Reúnam-se no Google Meet e façam duas passagens completas do início ao fim usando o cronômetro do `slides.html`. O objetivo é que cada um finalize seu bloco cravando entre **11 e 12 minutos**.
2. **Sinais Combinados no Chat do Meet:**  
   Enquanto o colega estiver apresentando, o membro que está na espera pode enviar no chat privado do WhatsApp ou do Meet alertas discretos aos 9 minutos (*"Faltam 2 minutos para fechar seu bloco"*), garantindo que ninguém se alongue excessivamente.
3. **Mantenham o Roteiro de Perguntas da Banca Aberto:**  
   Deixem o arquivo `Trabalho 2\docs\brain\06_GUIA_DE_DEFESA_E_PERGUNTAS_BANCA.md` em uma aba lateral durante a sabatina para consultar respostas rápidas caso o Prof. José Denes formule perguntas sobre o K-Fold, Grad-CAM ou o algoritmo GrabCut.
