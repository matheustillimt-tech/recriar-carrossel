# Comparativo de Modelos para Geração de Carrossel

Qual provedor + modelo escolher para cada caso.

## Provedor primeiro (roteado por qualidade, sem perguntar)

| Provedor | Quando | Modelos | Chave |
|---|---|---|---|
| **Google AI Studio** | Slide/imagem **sem rosto** do criador (padrão) | `gemini-3-pro-image` (2K), `gemini-3.1-flash-image` (só rascunho) | `GOOGLE_AI_STUDIO_API_KEY` |
| **OpenRouter** | Slide/imagem **com rosto** do criador, ou sem rosto quando o Gemini errou texto 2x | `openai/gpt-5.4-image-2` | `OPENROUTER_API_KEY` |
| **Higgsfield** | Só pra **Soul ID** (rosto consistente) | `gpt_image_2`, `nano_banana_2`, `text2image_soul_v2` | conta Higgsfield (CLI/MCP) |

> **Google AI Studio direto voltou a funcionar pra imagem** (testado 15/09/2026: `gemini-3-pro-image` e `gemini-3.1-flash-image` geraram em 4:5 e 16:9, 2K, acentos PT-BR corretos). O 429 `RESOURCE_EXHAUSTED` de abr/2026 era nos modelos `-preview`. Se voltar a dar 429, a cota acabou: gere no OpenRouter com `openai/gpt-5.4-image-2`.

### Como a chamada Google AI Studio funciona (resumo)

- `POST https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent` com header `x-goog-api-key`
- `generationConfig.responseModalities: ["IMAGE"]` + `imageConfig: {aspectRatio: "4:5", imageSize: "2K"}`
- Referências entram como `inlineData` (base64) nos `parts`
- Imagem volta em `candidates[0].content.parts[].inlineData.data`
- Script pronto: `scripts/generate_google.py` (recusa fotos do perfil do criador)

### Como a chamada OpenRouter funciona (resumo)

- Endpoint de chat: `POST https://openrouter.ai/api/v1/chat/completions`
- `"modalities": ["image", "text"]`
- Imagens de referência entram como `image_url` em base64 (`data:image/jpeg;base64,...`)
- Imagem gerada volta em `choices[0].message.images[].image_url.url`
- Multi-image input: passe original + foto do criador + style-ref na mesma chamada
- Script pronto: `scripts/generate_openrouter.py`

---

## Resumo rápido (decisão em 5s)

| Você quer... | Use |
|---|---|
| Slide sem rosto: tipografia + design + texto | **Gemini 3 Pro Image 2K** (Google AI Studio) |
| Slide com o rosto do criador | **GPT Image 2** (OpenRouter `openai/gpt-5.4-image-2`) |
| Texto que o Gemini errou 2x | **GPT Image 2** (OpenRouter) |
| Cartoon, character, ilustração estilizada | **Gemini 3 Pro Image** (Google AI Studio) |
| Rosto do criador consistente em vários slides | **text2image_soul_v2** (Higgsfield, requer Soul ID) |
| Rascunho rápido de layout (não vai pro final) | **Gemini 3.1 Flash Image** (Google AI Studio) |
| Foto de produto / lifestyle / marketing | **Higgsfield Marketing Studio Image** |
| Foto editorial / fashion / moodboard | **Higgsfield Soul 2.0** |
| Cinematic / dramatic mood | **Soul Cinema** (Higgsfield) |

## Detalhado por modelo

### 1. GPT Image 2 (OpenAI via Higgsfield)

**Sweet spot:** design gráfico, banners, tipografia, **texto no slide**.

- ✅ Renderiza texto melhor que outros modelos
- ✅ Sabe fazer layout (header / body / CTA)
- ✅ Bom em logos e ícones
- ⚠️ Custa mais (2-3 créditos em 2k high)
- ⚠️ Lento (~30-60s por slide em 2k)

**Quando usar:** carrossel com muito texto, headlines grandes, infográficos.

**Comando:**
```bash
higgsfield generate create gpt_image_2 \
  --prompt "..." \
  --aspect_ratio 3:4 \
  --resolution 2k \
  --quality high \
  --wait
```

### 2. Nano Banana 2 (Google via Higgsfield ou direto)

**Sweet spot:** personagem, cartoon, animado, ilustração estilizada.

- ✅ Rápido (~10-15s)
- ✅ Barato (~1 crédito)
- ✅ Excelente em poses / expressões
- ⚠️ Texto não é forte (erra letra mais que GPT)
- ⚠️ Tende pra estilo "ilustração" mesmo quando pede "fotorrealista"

**Quando usar:** slides de história visual, ilustrações de conceito, mascote.

**Via Higgsfield:**
```bash
higgsfield generate create nano_banana_2 \
  --prompt "..." --aspect_ratio 3:4 --wait
```

**Via Google AI Studio direto:**
```bash
python3 scripts/generate_google.py --model gemini-3.1-flash-image --prompt-file p.txt --out rascunho.png
```

### 3. Nano Banana Pro (`gemini-3-pro-image`) — PADRÃO SEM ROSTO

**Sweet spot:** slide sem rosto com texto, print, objeto ou cenário.

- ✅ Tipografia editorial e acentos PT-BR corretos (teste 15/09/2026)
- ✅ Fiel ao layout quando recebe o slide original como referência
- ✅ 2K nativo (1856×2304 em 4:5), ~20-40 s por slide
- ⚠️ Texto miúdo dentro de print (tabela, números) pode trocar dígitos
- ⚠️ Não usar com o rosto do criador (pouco realista)

**Comando:**
```bash
python3 scripts/generate_google.py --prompt-file p.txt --ref referencia/slide_02.jpg --out slide-02.png
```

### 4. text2image_soul_v2 (Higgsfield, Soul ID)

**Sweet spot:** **mesma pessoa em vários slides** com fidelidade facial.

- ✅ Rosto consistente entre slides (ÚNICO modelo que faz isso bem)
- ✅ Pose / expressão / roupa variáveis com rosto fixo
- ⚠️ Requer Soul ID treinada antes (15+ fotos, 10 min de treino)
- ⚠️ Custo médio-alto (3 créditos)

**Quando usar:**
- Carrossel "você falando" com várias expressões
- Você como personagem em diferentes cenas
- Marca pessoal forte (mesmo criador em todos os slides)

**Comando:**
```bash
higgsfield generate create text2image_soul_v2 \
  --prompt "..." \
  --character_id soul_abc123 \
  --aspect_ratio 3:4 \
  --wait
```

### 5. Higgsfield Soul 2.0

**Sweet spot:** UGC aesthetic, fashion editorial, lifestyle.

- ✅ Look "magazine cover"
- ✅ Aceita Soul Character como referência
- ⚠️ Não é forte em texto/tipografia
- ⚠️ Pode sair "muito clean" demais

**Quando usar:** carrosséis lifestyle, fitness, beleza, fashion.

### 6. OpenAI gpt-image-1 (API direta)

**Sweet spot:** alternativa premium ao GPT Image 2 sem Higgsfield.

- ✅ Mesma qualidade do GPT Image 2 (mesmo modelo backend)
- ✅ Não precisa Higgsfield account
- ⚠️ Custo fixo $0.19/imagem high
- ⚠️ Aspect ratios limitados (1024×1536 é o mais próximo de 3:4)

**Quando usar:** já tem OpenAI account, não quer Higgsfield.

**Código:**
```python
from openai import OpenAI
client = OpenAI()
r = client.images.generate(
    model="gpt-image-1",
    prompt="...",
    size="1024x1536",
    quality="high",
    n=1,
)
```

### 7. Higgsfield Auto

**Sweet spot:** "não sei qual modelo escolher".

- ✅ Routing automático
- ✅ Bom default quando o brief é amplo
- ⚠️ Pode não pegar o melhor modelo pro seu caso específico

**Quando usar:** primeiros testes, não sabe ainda o que precisa.

## Tabela mestre — custo × velocidade × qualidade-texto

| Modelo | Custo (USD/slide) | Velocidade | Texto | Visual | Quando NÃO usar |
|---|---|---|---|---|---|
| GPT Image 2 (1k low) | $0.02 | Médio | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Foto editorial fashion |
| GPT Image 2 (2k high) | $0.10 | Lento | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Volume / iteração rápida |
| Nano Banana 2 | $0.04 | Rápido | ⭐⭐⭐ | ⭐⭐⭐⭐ | Texto-pesado |
| Nano Banana Pro 2K (Google AI Studio) | free tier / pago com billing | Médio | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Rosto do criador |
| GPT Image 2 (OpenRouter) | ~$0.20 | Lento (~2 min) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (rosto) | — |
| text2image_soul_v2 | $0.12 | Médio | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ (rosto) | Sem Soul ID treinada |
| OpenAI gpt-image-1 | $0.19 | Lento | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Restrição de orçamento |
| Higgsfield Marketing Studio | $0.15 | Médio | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (ads) | Conteúdo não-ad |

## Decisão por tipo de carrossel

| Carrossel | Modelo recomendado |
|---|---|
| Educativo texto-pesado (10 tips, 5 erros, etc) | **Gemini 3 Pro Image 2K**; GPT Image 2 se errar texto 2x |
| Antes/depois lifestyle | **Soul 2.0** ou **Marketing Studio** |
| Storytelling com sua cara | **text2image_soul_v2** + Soul ID treinada |
| Cartoon educacional | **Nano Banana 2** |
| Showcase de produto | **Higgsfield product-photoshoot** (skill irmã) |
| Editorial / fashion | **Soul 2.0** |
| Pure design / brand | **GPT Image 2** |

## Pegadinhas comuns

1. **Não use modelo de vídeo pra imagem.** GPT Image 2 ≠ Seedance 2.0.
2. **`auto` é tentador mas inconsistente** entre slides — fixe um modelo por carrossel.
3. **4:5 existe no Google AI Studio e no OpenRouter** (`--aspect-ratio 4:5`). No Higgsfield use `3:4` e recorte depois.
4. **Resolution 2k+quality high custam 5-6× mais.** Comece em 1k low pra iterar.
5. **Soul ID é skill separada** (`higgsfield-soul-id`) — treine antes.

## Quando trocar de modelo

Se 2 re-rolls não corrigiram um problema:

- **Texto sempre errado** → mude pra GPT Image 2 (se já está) ou OpenAI gpt-image-1
- **Rosto inconsistente** → use Soul ID (treine)
- **Estilo muito "AI clean"** → tente Soul Cinema ou Flux 2.0
- **Muito lento** → caia pra Nano Banana 2 ou Z Image (fastest)
