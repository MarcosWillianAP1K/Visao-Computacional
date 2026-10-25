# Guia de Apresentação e Exportação dos Slides

> **Equipe**: Grupo 4  
> **Disciplina**: Tópicos Especiais em Visão Computacional — UFPI  
> **Arquivos na Pasta**:
> - `apresentacao_trabalho_3_final.pptx` (ou `slides.pptx`): Apresentação nativa em PowerPoint (16:9 widescreen) com 20 slides e notas de orador integradas.
> - `ROTEIRO_FALA_TRIO.md`: Script de fala sincronizado minuto a minuto
> - `slides.md`: Apresentação em formato Marp / Markdown padronizado

---

## 1. Como Usar no Microsoft PowerPoint e Google Apresentações

### 1.1. No Google Apresentações (Google Slides)
1. Acesse o [Google Drive](https://drive.google.com).
2. Clique em **`+ Novo`** > **`Upload de arquivo`** e selecione o arquivo `apresentacao_trabalho_3_final.pptx`.
3. Dê um duplo clique no arquivo carregado e clique em **"Abrir com o Apresentações Google"**.
4. Para visualizar as anotações completas de cada membro durante os ensaios ou a apresentação, clique em **`Exibir`** > **`Mostrar notas do orador`** (ou utilize o **Modo Apresentador** ao projetar).

### 1.2. No Microsoft PowerPoint
1. Dê um duplo clique no arquivo `apresentacao_trabalho_3_final.pptx`.
2. Para apresentar em tela cheia, pressione **`F5`** (ou **`Shift + F5`** a partir do slide atual).
3. No **Modo Apresentador**, o cronômetro oficial e o script exato de fala do slide atual são exibidos na tela secundária ao lado do slide.

---

## 2. Como Exportar para PDF no PowerPoint / Google Slides

### Método A: Pelo Microsoft PowerPoint
1. Abra o arquivo `.pptx`.
2. Vá em **`Arquivo`** > **`Salvar como`** ou **`Exportar`** > **`Criar documento PDF/XPS`**.
3. Selecione o local e salve como PDF de alta qualidade.

### Método B: Pelo Google Apresentações
1. Com a apresentação aberta no Google Slides, clique em **`Arquivo`** > **`Fazer download`** > **`Documento PDF (.pdf)`**.

---

### Método B: Via Marp CLI (A partir do `slides.md`)
Caso possua o Node.js ou a extensão Marp no VS Code:

```bash
# Instalação do Marp CLI (se não possuir)
npm install -g @marp-team/marp-cli

# Exportação direta para PDF de alta fidelidade
marp --pdf slides.md -o Apresentacao_GMIC_Grupo4.pdf --allow-local-files
```

---

## 3. Como Importar para o Google Slides

1. Gere o arquivo PDF através do Método A ou B acima.
2. Acesse o [Google Drive](https://drive.google.com).
3. Faça upload do arquivo `Apresentacao_GMIC_Grupo4.pdf`.
4. Ou utilize uma ferramenta como [Smallpdf / Ilovepdf](https://www.ilovepdf.com/pt/pdf_para_powerpoint) para converter o PDF em formato `.pptx`.
5. Abra o Google Apresentações (*Google Slides*), vá em **Arquivo > Importar slides** e selecione o arquivo gerado.

---

## 4. Dicas Estratégicas para a Apresentação no Google Meet

1. **Compartilhamento de Aba ou Janela**:
   - No Google Meet, selecione **"Apresentar agora > Uma guia do Chrome"** e escolha a guia do `slides.html`. Isso garante a maior taxa de quadros e nitidez máxima das fontes e equações.
2. **Uso de Duas Telas ou Janela Dividida**:
   - Mantenha a guia da apresentação em tela cheia na tela principal.
   - Mantenha o arquivo `ROTEIRO_FALA_TRIO.md` aberto em uma segunda tela ou janela ao lado para consulta imediata de tempos e dados técnicos.
3. **Plano de Contingência de Conexão**:
   - Conforme acordado na equipe: se a conexão de um colega cair, o próximo membro da ordem assume imediatamente o slide sem interrupção do cronômetro, informando brevemente à banca.
