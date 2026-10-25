# Relatório Técnico-Científico SBC (Overleaf / LaTeX)

> **Artigo**: *"Reprodução Experimental e Avaliação de Mapas de Ativação Desacoplados para Detecção de Massas em Mamografia via Aprendizado Fracamente Supervisionado"*  
> **Modelo**: Sociedade Brasileira de Computação (SBC) — 8 a 12 páginas  
> **Disciplina**: Tópicos Especiais em Visão Computacional — UFPI / CSHNB  
> **Docente**: Prof. Dr. José Denes Lima Araújo  
> **Equipe**: Grupo 4

---

## 1. Estrutura dos Arquivos da Pasta

```
Trabalho 3 (Final)/docs/relatorio_sbc/
├── main.tex             # Documento mestre do artigo científico completo formatado em SBC
├── sbc.bib              # Base de referências bibliográficas BibTeX com todas as citações
├── sbc-template.sty     # Arquivo de estilo oficial da SBC (margens, fontes e seções)
└── README.md            # Este guia de importação e compilação
```

---

## 2. Como Importar Diretamente para o Overleaf

1. Compacte os arquivos desta pasta em um arquivo `.zip`:
   - Selecione `main.tex`, `sbc.bib` e `sbc-template.sty`.
   - Clique com o botão direito e escolha **Compactar para arquivo ZIP** (ex: `relatorio_sbc_grupo4.zip`).
2. Acesse o [Overleaf](https://www.overleaf.com) e faça login em sua conta.
3. No painel principal (*Dashboard*), clique no botão verde **"New Project"** (Novo Projeto) e selecione **"Upload Project"** (Carregar Projeto).
4. Arraste ou selecione o arquivo `relatorio_sbc_grupo4.zip`.
5. O Overleaf descompactará e abrirá automaticamente o projeto.
6. No menu superior esquerdo (**Menu**), certifique-se de que as configurações estão:
   - **Compiler**: `pdfLaTeX`
   - **TeX Live version**: `2023` ou `2024`
   - **Main document**: `main.tex`
7. Clique no botão verde **"Recompile"** (ou pressione `Ctrl + Enter`). O PDF será gerado com perfeição visual e conformidade com as normas SBC.

---

## 3. Como Compilar Localmente (Linux, Windows ou Mac)

Caso possua uma distribuição LaTeX instalada (TeX Live, MiKTeX ou MacTeX):

```bash
cd "Trabalho 3 (Final)/docs/relatorio_sbc"

# Compilação em 4 passos para resolução de referências cruzadas e BibTeX:
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Ou de forma automática via `latexmk`:
```bash
latexmk -pdf main.tex
```

---

## 4. Destaques Acadêmicos do Artigo Redigido

- **Rigor Metodológico**: Equacionamento completo da arquitetura GMIC, função de perda multi-ramo com regularização L1 ($\beta = 3,26$) e dos 5 geradores de CAM (Zhou, Selvaraju, Chattopadhay, Fu e Jiang).
- **Engenharia de Software e Hardware**: Detalhamento das mitigações computacionais via Precisão Mista Automática (AMP FP16) e Acumulação de Gradientes (batch virtual de 6 imagens).
- **Auditoria Crítica da Literatura (Errata Técnica)**: Demonstração analítica formal de que a métrica reportada como "FNR = 88.52%" na Tabela 1 de Sampaio & Cordeiro é na realidade a Taxa de Verdadeiros Negativos (TNR / Especificidade), pois $\text{TPR} = 71.88\% \implies \text{FNR} = 1 - \text{TPR} = 28.12\%$.
- **Avaliação de Impacto Clínico**: Discussão minuciosa sobre a viabilidade da taxa de falsos positivos por imagem (0.88 FPPI do modelo campeão vs colapso de 4.19 FPPI do Layer-CAM).
