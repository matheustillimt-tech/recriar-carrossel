# PROMPT-CLAUDE-CODE — recriar-carrossel-image-gen

Cole esse prompt no Claude Code quando quiser recriar um carrossel via geração de imagem direta (sem Paper).

---

## Como o Claude escolhe o modelo (por slide, qualidade primeiro)

| Slide | Modelo |
|---|---|
| Com o rosto do criador | OpenRouter `openai/gpt-5.4-image-2` |
| Sem rosto | Google AI Studio `gemini-3-pro-image` em 2K |
| Sem rosto, Gemini errou texto 2x | OpenRouter `openai/gpt-5.4-image-2` |
| Rosto consistente com Soul ID treinado | Higgsfield `text2image_soul_v2` |

Se você informar um modelo no prompt, ele manda.

## Prompt template

```
Recria esse carrossel via image gen (sem Paper):

URL/Pasta: <URL Instagram OU pasta com slides .jpg>
Modelo: <vazio = roteamento automático | gpt image 2 | gemini-3-pro-image>

Adaptação para nicho: <ex: "marketing pra dentistas" OR "manter como está">
Soul ID (só Higgsfield, rosto consistente): <soul_xxx OR "skip">
Cor CTA: <ex: #FF6600 OR "manter original">
Idioma: <PT-BR | EN | manter original>

Tipo de adaptação:
[ ] Cópia idêntica (só re-gerar com IA)
[ ] Tradução + cópia
[ ] Adaptação pro nicho (texto novo, mesmo design)
[ ] Spin-off (mesmo template, conteúdo totalmente novo)
```

---

## Fluxo que o Claude segue

1. **Cria pasta de trabalho:** `recriar-{POST_ID}/` no diretório atual (ou no local que você indicar)
2. **Baixa referência:** Apify se URL, copia se pasta
3. **Lê todos os slides** (visão) e cria `analise-design.md` com:
   - Paleta hex
   - Tipografia (peso, tamanho, família)
   - Layout pattern
   - Hierarquia texto
4. **Cria `conteudo.md`** com texto de cada slide adaptado
5. **Mostra o roteamento** (quais slides têm rosto → GPT Image 2, quais não → Gemini 3 Pro) + "Confirma análise + texto? Posso gerar os PNGs?"
6. **Gera prompts** em `prompts/slide-NN.txt` (1 por slide)
7. **Gera PNGs**:
   - Sem rosto → `scripts/generate_google.py --prompt-file ... --ref ... --out ...` (default `gemini-3-pro-image`, 2K)
   - Com rosto → `scripts/generate_openrouter.py --prompt-file ... --ref ... --out ... --model openai/gpt-5.4-image-2`
   - Higgsfield → `higgsfield generate create <model> ...` (só Soul ID)
8. **Resize uniforme** pra 1080×1350
9. **Cria overview** `overview.jpg` (grid 4×2)
10. **Mostra preview** + pergunta "Re-rolar algum slide?"
11. **Quando aprovado:** salva final em `final/` + atualiza `Kanban Conteudos.md` (se aplicável)

---

## Exemplos de uso

### Caso 1: Replicar viral idêntico
```
Recria esse carrossel via image gen:
URL: https://instagram.com/p/DY7bJr5DJfR/
Adaptação: manter como está
Modelo: gpt_image_2
Idioma: manter (já em PT)
```

### Caso 2: Adaptar pra outro nicho
```
Recria esse carrossel via image gen:
URL: https://instagram.com/p/abcdef/
Adaptação: "criação de site sem código pra arquitetos"
Modelo: nano_banana_2
Idioma: PT-BR
```

### Caso 3: Carrossel com seu rosto (Soul ID)
```
Recria esse carrossel via image gen:
URL: https://instagram.com/p/xyz/
Adaptação: "manter texto, trocar rostos pelo meu"
Modelo: text2image_soul_v2
Soul ID: soul_seu_personagem
```

### Caso 4: Carrossel sem rosto (roteamento automático)
```
Recria esse carrossel via image gen:
URL: https://instagram.com/p/xyz/
Adaptação: traduzir PT-BR
Idioma: PT-BR
```
→ todos os slides no Google AI Studio `gemini-3-pro-image` 2K.

---

## Custo estimado

- Slide sem rosto (Google AI Studio) → grátis dentro da cota do free tier
- Slide com rosto (GPT Image 2 via OpenRouter) → ~US$ 0,20 cada

---

## Pegadinhas

1. **Modelos erram letras** ~15% das vezes. SEMPRE revise `overview.jpg`.
2. **PT-BR no prompt principal degrada qualidade** — passe briefing em inglês, só o texto que aparece no slide em PT entre aspas.
3. **Soul ID precisa estar treinada antes** com 15+ fotos. Sem treino: rostos genéricos.
4. **Re-roll é barato.** Se 1 slide saiu ruim, re-gere só ele, não o carrossel inteiro.
5. **Texto miúdo em print** (tabela, código) pode trocar dígitos em qualquer modelo. Se o print é conteúdo, cole o recorte original por cima ou use o modo Paper.

---

## Ver também

- Skill irmã (modo Paper): `recriar-carrossel`
- Higgsfield: https://higgsfield.ai
- Chave do Google AI Studio: https://aistudio.google.com/apikey
