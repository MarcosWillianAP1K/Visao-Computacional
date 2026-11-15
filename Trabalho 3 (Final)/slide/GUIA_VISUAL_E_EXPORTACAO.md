# Guia Visual da Apresentação no Canva (23 Slides)

## Links Diretos da Apresentação no Canva
- **Design ID:** `DAHbBE7J4gk`
- **Template Base Utilizado:** *Apresentação genérica minimalista cinza* (`UFPI | CSHNB — Visão Computacional`)
- **Link para Editar no Canva:** https://www.canva.com/d/iW-PX1jfShuI_aM
- **Link para Visualizar / Apresentar:** https://www.canva.com/d/UDfF9EnbRcpAHbm

---

## Melhorias Aplicadas Nesta Versão
1. **Template Oficial do Grupo (*Apresentação genérica minimalista cinza*):**
   - Clorado diretamente da base visual da equipe (`UFPI | CSHNB | Visão`), preservando o brasão da UFPI, tipografia minimalista, paleta cinza/ardósia e faixas metálicas.
2. **Zero Imagens Geradas por IA:**
   - Todas as fotos genéricas de banco de imagens foram eliminadas. Os slides contêm exclusivamente tópicos técnicos objetivos, prints reais extraídos em 350 DPI do artigo original de Sampaio & Cordeiro (2022) e os gráficos/resultados reais da nossa reprodução em PyTorch.
3. **Numeração de Página e Identificação do Apresentador em Todos os Slides:**
   - Cabeçalho padronizado com `UFPI | CSHNB — Parte X: [Nome do Integrante]` e `Visão Computacional | Pág. XX/23` (`01/23` a `23/23`).
4. **Estrutura Expandida (23 Slides) Dividida por Tópicos e entre os 3 Integrantes:**
   - **Parte 1 — Contexto do Artigo (Walison Weudes — Slides 01 a 06):** Capa, Sumário, Introdução & Problema Clínico, Gargalo da Anotação (Supervisão Total vs. WSOD), O Artigo Base (com print do cabeçalho/Abstract original) e Resumo da Solução Proposta (com diagrama arquitetural).
   - **Parte 2 — Explicação do Modelo e Como Funciona (Hermeson Alves — Slides 07 a 13):** Divisor Parte 2, Visão Geral do Modelo GMIC (com print da **Figura 2** do artigo), Módulo Global ResNet-22 & Seleção Gulosa de Patches (com **Figura 2**), Módulo Local ResNet-18 MIL & Fusão & Loss (com print da **Equação 2** do artigo), Fundamentos do CAM (com print da **Figura 1** e **Equação 1** do artigo), Evolução dos 4 CAMs de Gradiente (com painel comparativo) e Teoria do Desacoplamento Treino vs. Teste.
   - **Parte 3 — Resultados Comparativos, Auditoria e Conclusão (Marcos Willian — Slides 14 a 23):** Divisor Parte 3, Base VinDr-Mammo (com print da **Figura 3** do artigo), Implementação PyTorch & Protocolo WSOD $\text{IoU} \ge 0{,}3$ (com saída real do nosso pipeline), Resultados de Classificação Global (com print da **Tabela 1** do artigo), Auditoria Crítica da Errata Matemática na Tabela 1 ($\text{FNR}$ vs. $\text{TNR}$ com print da **Tabela 1**), Resultados de Detecção WSOD (com print da **Tabela 2** do artigo), Comparação Visual Qualitativa dos 5 CAMs (com print da **Figura 4** do artigo), Síntese Quantitativa do Trade-off Clínico $\text{TPR} \times \text{FPPI}$, Conclusões Gerais e Encerramento.

---

## Prints do Artigo Original Extraídos em `slide/paper_prints/`
- [paper_header_abstract.png](file:///c:/Users/MWSS/OneDrive/Desktop/Visao%20Computacional/Trabalho%203%20(Final)/slide/paper_prints/paper_header_abstract.png) — Título, Autores e *Abstract* original (Slide 05)
- [paper_fig1_cam.png](file:///c:/Users/MWSS/OneDrive/Desktop/Visao%20Computacional/Trabalho%203%20(Final)/slide/paper_prints/paper_fig1_cam.png) e [paper_eq1_cam.png](file:///c:/Users/MWSS/OneDrive/Desktop/Visao%20Computacional/Trabalho%203%20(Final)/slide/paper_prints/paper_eq1_cam.png) — Figura 1 e Equação 1 do artigo (Slide 11)
- [paper_fig2_gmic.png](file:///c:/Users/MWSS/OneDrive/Desktop/Visao%20Computacional/Trabalho%203%20(Final)/slide/paper_prints/paper_fig2_gmic.png) — Figura 2 do artigo: Arquitetura GMIC (Slides 08 e 09)
- [paper_eq2_loss.png](file:///c:/Users/MWSS/OneDrive/Desktop/Visao%20Computacional/Trabalho%203%20(Final)/slide/paper_prints/paper_eq2_loss.png) — Equação 2 do artigo: Função de Perda GMIC (Slide 10)
- [paper_fig3_vindr.png](file:///c:/Users/MWSS/OneDrive/Desktop/Visao%20Computacional/Trabalho%203%20(Final)/slide/paper_prints/paper_fig3_vindr.png) — Figura 3 do artigo: 4 Projeções da base VinDr-Mammo (Slide 15)
- [paper_tab1_classificacao.png](file:///c:/Users/MWSS/OneDrive/Desktop/Visao%20Computacional/Trabalho%203%20(Final)/slide/paper_prints/paper_tab1_classificacao.png) — Tabela 1 do artigo: Classificação Global Normal vs. Massa (Slides 17 e 18)
- [paper_tab2_deteccao_wsod.png](file:///c:/Users/MWSS/OneDrive/Desktop/Visao%20Computacional/Trabalho%203%20(Final)/slide/paper_prints/paper_tab2_deteccao_wsod.png) — Tabela 2 do artigo: Matriz $\text{TPR}@\text{FPPI}$ dos 5 CAMs (Slide 19)
- [paper_fig4_segmentacao_cams.png](file:///c:/Users/MWSS/OneDrive/Desktop/Visao%20Computacional/Trabalho%203%20(Final)/slide/paper_prints/paper_fig4_segmentacao_cams.png) — Figura 4 do artigo: Comparação Qualitativa dos 5 Mapas de Ativação (Slide 20)
