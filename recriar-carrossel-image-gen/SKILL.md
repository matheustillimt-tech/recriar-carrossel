---
name: recriar-carrossel-image-gen
description: Recria carrossel viral do Instagram via GERAÇÃO DIRETA DE IMAGEM (sem Paper). Cada slide vira um PNG inteiro gerado por IA, roteado por qualidade: slide SEM rosto → Google AI Studio `gemini-3-pro-image` em 2K; slide COM o rosto do criador → OpenRouter `openai/gpt-5.4-image-2`. Alternativa: Higgsfield (Soul ID pra rosto consistente). Use quando o usuário quiser recriar rápido SEM precisar abrir Paper Desktop, ou quando o carrossel original tem foto realista forte e o que importa é visual + tipografia (não edição posterior). Ative em "recria esse carrossel só com IA", "gera o carrossel por imagem", "modo rápido sem Paper", "nano banana carrossel", "gpt image carrossel". Para texto editável e pixel-preciso → use `recriar-carrossel` (modo Paper).
---

# Recriar Carrossel via Image Gen

Modo **rápido e sem Paper Desktop** de recriar carrossel. Em vez de montar HTML/CSS dentro do Paper, a IA **gera cada slide inteiro como imagem** (foto + layout + tipografia, tudo num PNG).

## Quando usar este modo (vs `recriar-carrossel` Paper)

| Critério | Image Gen (esta skill) | Paper (`recriar-carrossel`) |
|---|---|---|
| Velocidade | ⚡ ~1-3 min/slide | 🐢 5-10 min/slide |
| Texto editável depois | ❌ É bitmap | ✅ HTML editável |
| Precisão tipográfica | 🟡 ~85% (errinhos de letra) | ✅ 100% pixel-perfeito |
| Foto realista forte | ✅ Gera junto | 🟡 Precisa importar |
| Requer Paper Desktop aberto | ❌ Não | ✅ Sim |
| Custo por slide | US$ 0.05–US$ 0.50 | US$ 0 (incluso no Paper Pro) |
| Variações rápidas | ✅ Re-roll fácil | 🟡 Refaz no Paper |
| Export PDF/JSX | ❌ Só PNG | ✅ PDF + JSX |
| Caso ideal | Carrossel com foto forte, protótipo, urgência | Carrossel texto-pesado, edição contínua, brand kit |

**Regra prática:** se você quer publicar HOJE e mexer pouco depois → image gen. Se vai iterar 5x → Paper.

## PASSO 0 (OBRIGATÓRIO) — Rotear cada slide pelo conteúdo

**Qualidade vem primeiro.** Economia só entra quando o resultado é igual. Antes de tudo, leia a seção "Observações" do `perfil.md` (ver abaixo): regras de modelo escritas lá mandam sobre esta skill.

Decida o modelo **por slide**, sem perguntar ao usuário (só avise o roteamento no plano):

| O slide tem... | Provedor | Modelo | Script |
|---|---|---|---|
| **Rosto do criador** (foto, capa com a pessoa, avatar do header re-renderizado pela IA) | OpenRouter | `openai/gpt-5.4-image-2` | `generate_openrouter.py` |
| **Sem rosto** (texto, print, objeto, cenário, pessoa genérica) | Google AI Studio | `gemini-3-pro-image` em **2K** | `generate_google.py` |
| Sem rosto, mas o Gemini errou texto em **2 tentativas** | OpenRouter | `openai/gpt-5.4-image-2` | `generate_openrouter.py` |
| Rosto consistente em muitos slides com Soul ID treinado | Higgsfield | `text2image_soul_v2` + `--character_id` | CLI `higgsfield` |

- **Gemini 3 Pro Image é o padrão sem rosto**, não o Flash. Testado em 15/09/2026: manchete e acentos PT-BR perfeitos, fiel ao layout da referência, saída nativa 1856×2304 em 2K.
- **`gemini-3.1-flash-image`** só pra rascunho rápido de layout. Não use em slide final.
- **Texto miúdo dentro de print** (tabela, código, números de interface) às vezes troca dígitos em qualquer modelo. Se o print da referência for conteúdo, não decoração, recorte o print original e cole por cima com Pillow, ou faça o slide no Paper (`recriar-carrossel`).
- O `generate_google.py` **recusa referências da pasta `perfil/` da skill** (fotos do criador). Se precisar dessas fotos, o slide é de rosto e vai pro GPT Image 2.

Se o usuário pedir um modelo específico, use o dele.

## Perfil do criador (@ + foto + cores) — carregar SEMPRE

Antes de compor os prompts, carregue o **perfil do criador** (fonte única de identidade, compartilhado com a skill `recriar-carrossel`):

```
~/.claude/skills/recriar-carrossel/perfil/
├── perfil.md          → @ do Instagram, nome, selo, cores da marca, caminho do doc de tom de voz
├── avatar.jpg         → foto de perfil (vai no HEADER de cada slide)
└── rosto/*.jpg        → 3 a 5 fotos do rosto (multi-image ref pra IA manter o rosto)
```

Use assim na geração:
- **Header do slide:** foto circular (`avatar.jpg`) + nome + selo + `@handle` do `perfil.md`
- **Multi-image input:** passe `assets/rosto/*.jpg` junto da referência original pro modelo manter o rosto do criador nos slides (ex: capa com a pessoa)
- **Cores:** use `cores.accent/background/texto` do `perfil.md` no design system do prompt

Se o perfil não existir (primeira vez), **pergunte o @, o nome e as cores, e peça a foto de perfil** (e as fotos do rosto, se algum slide tiver o rosto dele) antes de gerar. Crie a pasta e grave tudo lá pra não perguntar de novo.

## Primeira vez (chaves de API)

As chaves ficam no mesmo arquivo da skill irmã, `~/.claude/skills/recriar-carrossel/.env` (modelo em `.env.example` na pasta `recriar-carrossel`). Se faltar a chave que o slide precisa, peça só ela ao usuário, grave no arquivo com `chmod 600` e nunca mostre a chave no chat depois:

- `GOOGLE_AI_STUDIO_API_KEY` (slides sem rosto): https://aistudio.google.com/apikey
- `OPENROUTER_API_KEY` (slides com rosto): https://openrouter.ai/keys, com crédito colocado em https://openrouter.ai/credits
- `APIFY_TOKEN` (só pra baixar a referência pelo link do Instagram): https://console.apify.com/settings/integrations

Os scripts precisam de `pip3 install httpx python-dotenv pillow`.

## Stack

| Camada | Padrão | Alternativa |
|---|---|---|
| **Slide com rosto do criador** | OpenRouter `openai/gpt-5.4-image-2` | Higgsfield `text2image_soul_v2` (Soul ID) |
| **Slide sem rosto** | Google AI Studio `gemini-3-pro-image` 2K | OpenRouter `openai/gpt-5.4-image-2` se o texto não sair certo |
| **Rascunho de layout** | Google AI Studio `gemini-3.1-flash-image` | — |
| **Multi-image input (ref + estilo)** | ✅ base64 no payload (`image_url` no OpenRouter, `inlineData` no Google) | ✅ via `media_upload` |
| **Resize 1080×1350** | `sips -Z 1350 in.png --out out.png` ou Pillow | idem |

## Pipeline (7 passos)

### 1. Capturar input
Receba: URL do post Instagram OU pasta com prints dos slides OU descrição textual ("recria estilo Nik Sharma").

### 2. Baixar referência (se URL)
```bash
# Apify Instagram Scraper (script da skill irmã; lê APIFY_TOKEN do .env da skill)
python3 ~/.claude/skills/recriar-carrossel/materiais/download-apify.py <URL> <PASTA>/referencia
# Output: <PASTA>/referencia/slide_01.jpg ... slide_NN.jpg + metadata.json
```

`<PASTA>` = pasta do carrossel (ver "Saída esperada").

### 3. Ler slides com visão
Use Read tool em cada `.jpg` da referência. Extraia:
- Texto exato de cada slide (transcrição)
- Hierarquia tipográfica (qual é H1, H2, body, caption)
- Paleta de cores (3-5 cores principais)
- Layout (single column, split, foto-cima/texto-baixo, foto-fundo)
- Foto/ilustração (estilo, ângulo, mood)
- Marca registrada do criador (logo, watermark, ornamento)

Registre a análise (design system em 3-5 linhas) em `analise-design.md` na pasta do carrossel.

### 4. Traduzir/adaptar conteúdo
Se for adaptar pra outro nicho:
- Traduza PT-BR (se vier em inglês)
- Ajuste exemplos pro nicho do usuário
- Mantenha hierarquia (capa = hook, slide N = CTA)
- CTA de comentário: use a palavra ou o código que o usuário definir. Sem um, sugira um código curto que ninguém escreveria por acaso e sem letras que se confundem (0/O, 1/I/l)
- **Tom de voz:** se o `perfil.md` apontar um doc de tom de voz, escreva todo texto dos slides e a legenda seguindo ele. Sem doc, peça 3 adjetivos do tom e um texto que ele já escreveu

### 5. Compor master prompt
Para cada slide, monte prompt assim:

```
Instagram carousel slide, 1080x1350, vertical 4:5 ratio.

DESIGN SYSTEM:
- Color palette: {hex1}, {hex2}, {hex3}
- Typography: {font-style description} (bold display + clean sans body)
- Visual style: {minimalist/editorial/bubbly/brutalist/etc}
- Brand element: {logo/ornament/watermark se aplicável}

LAYOUT:
- {single column / split / foto-cima / etc}
- {hierarquia: headline grande no topo, body médio no meio, CTA pequeno no rodapé}

CONTENT:
- Headline (large, bold): "{texto exato}"
- Subheadline (medium): "{texto exato}"
- Body (small): "{texto exato}"
- {se houver foto: descrição da foto}

STYLE REFERENCES:
- Mood: {clean/dramatic/playful}
- Lighting: {natural/studio/golden hour}
- {se rosto: "use Soul ID xyz" ou "use as 3 reference photos attached"}

OUTPUT: high-quality PNG, ready for Instagram carousel, no watermarks, text rendered perfectly.
```

### 6. Gerar slide-a-slide

> Use o roteamento do **PASSO 0**: slide sem rosto no Caminho A, slide com rosto no Caminho B.

**Caminho A — Google AI Studio (slides SEM rosto):**

Script pronto: `scripts/generate_google.py`. Chama `generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent` com `responseModalities: ["IMAGE"]` e `imageConfig` (`aspectRatio` + `imageSize`). Lê `GOOGLE_AI_STUDIO_API_KEY` do `.env` da skill.

```bash
python3 ~/.claude/skills/recriar-carrossel-image-gen/scripts/generate_google.py \
  --prompt-file prompts/slide-02.txt \
  --ref referencia/slide_02.jpg \
  --aspect-ratio 4:5 \
  --image-size 2K \
  --out output/slide-02.png
```

- Defaults do script: `gemini-3-pro-image`, 4:5, 2K. Leva ~20-40 s por slide. Rode vários slides em paralelo (`&` + `wait`).
- 2K em 4:5 devolve 1856×2304: mais nitidez no texto antes do resize pra 1080×1350. Use `--image-size 4K` só se for recortar/ampliar parte da imagem.

**Caminho B — OpenRouter GPT Image 2 (slides COM rosto, ou sem rosto quando o Gemini errou texto 2x):**

Endpoint: `https://openrouter.ai/api/v1/chat/completions`. Geração de imagem usa o mesmo formato de chat, com `"modalities": ["image", "text"]` e imagens de referência passadas como `image_url` em base64. A imagem gerada volta em `choices[0].message.images[].image_url.url` (data URL base64).

Script pronto: `scripts/generate_openrouter.py`.

```bash
R=~/.claude/skills/recriar-carrossel/perfil/rosto
python3 ~/.claude/skills/recriar-carrossel-image-gen/scripts/generate_openrouter.py \
  --prompt-file prompts/slide-01.txt \
  --ref referencia/slide_01.jpg --ref $R/rosto-01.jpg --ref $R/rosto-02.jpg \
  --model openai/gpt-5.4-image-2 \
  --aspect-ratio 4:5 \
  --out output/slide-01.png
```

- **`--aspect-ratio 4:5` é obrigatório** (já é o default do script). Sem `image_config.aspect_ratio` no payload, o modelo devolve **quadrado 1024×1024** e o resize distorce o slide. GPT Image 2 em 4:5 devolve 896×1120.
- O script lê `OPENROUTER_API_KEY` do `.env` da skill (`~/.claude/skills/recriar-carrossel/.env`) e imprime o custo de cada geração.
- GPT Image 2 leva ~2 min por slide. Pra vários slides, rode em background e siga trabalhando.

Mínimo em Python (núcleo da chamada — multi-image input):

```python
import os, base64, httpx

def b64(path):
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode()

def gen_openrouter(prompt, image_paths, model, out_path):
    content = [{"type": "text", "text": prompt}]
    for p in image_paths:  # referência original, foto do criador, style ref...
        mime = "image/png" if p.endswith(".png") else "image/jpeg"
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{b64(p)}"},
        })
    payload = {
        "model": model,                       # openai/gpt-5.4-image-2
        "messages": [{"role": "user", "content": content}],
        "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": "4:5"},   # sem isso volta 1:1
    }
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://conteudos.grupovortex.online",
        "X-Title": "Recriar Carrossel",
    }
    r = httpx.post("https://openrouter.ai/api/v1/chat/completions",
                   headers=headers, json=payload, timeout=300)
    r.raise_for_status()
    images = (r.json()["choices"][0]["message"].get("images") or [])
    for img in images:
        url = img["image_url"]["url"]
        if ";base64," in url:
            open(out_path, "wb").write(base64.b64decode(url.split(";base64,", 1)[1]))
            return out_path
    raise RuntimeError("Sem imagem na resposta")
```

**Por que multi-image input é poderoso aqui:** você passa (1) o slide original baixado + (2) foto do criador + (3) um style-ref do seu padrão visual, e pede "mantenha o layout, troque o texto pra X, use o rosto da foto 2, estilo da foto 3". O modelo respeita as 3 referências. É assim que a gente clona carrossel mantendo identidade.

**Troca de modelo:** `--model` em qualquer um dos dois scripts. Os dois aceitam as mesmas flags (`--prompt-file`, `--ref`, `--aspect-ratio`, `--out`).

**Caminho C — Higgsfield (só se precisar de Soul ID / rosto consistente):**

```bash
export PATH="$HOME/.npm-global/bin:$PATH"

# Rosto consistente (Soul Character treinada) — diferencial do Higgsfield
higgsfield generate create text2image_soul_v2 \
  --prompt "$(cat prompts/slide-01.txt)" \
  --character_id soul_abc123 \
  --aspect_ratio 3:4 --wait \
  --output ./output/slide-01.png

# GPT Image 2 / Nano Banana via Higgsfield (alternativa ao OpenRouter)
higgsfield generate create gpt_image_2 --prompt "..." --aspect_ratio 3:4 --resolution 2k --quality high --wait --output ./output/slide-02.png
higgsfield generate create nano_banana_2 --prompt "..." --aspect_ratio 3:4 --wait --output ./output/slide-03.png
```

Ou via MCP: `mcp__higgsfield__generate_image(model="gpt_image_2", ...)`.

**Quando usar cada provedor:**

| Situação | Provedor |
|---|---|
| Slide sem rosto (padrão) | **Google AI Studio** `gemini-3-pro-image` 2K |
| Slide com rosto do criador | **OpenRouter** `openai/gpt-5.4-image-2` |
| Sem rosto e o Gemini errou texto 2x | OpenRouter `openai/gpt-5.4-image-2` |
| Rosto do criador consistente em todos os slides (Soul ID treinado) | **Higgsfield** |
| Cartoon/character estilizado | Google AI Studio `gemini-3-pro-image` ou Higgsfield `nano_banana_2` |

### 7. Resize uniforme + montagem

```bash
# Confira a proporção ANTES do resize: tem que ser 4:5 (GPT 896×1120, Gemini 2K 1856×2304). Se veio 1024×1024, faltou --aspect-ratio.
sips -g pixelWidth -g pixelHeight output/slide-01.png

# Resize todos pra 1080×1350 (4:5 Instagram)
for f in output/slide-*.png; do
  sips -Z 1350 "$f" --out "final/$(basename "$f")"
done
```

Overview pra revisar (Pillow; o `montage` do ImageMagick falha sem fonte configurada):

```bash
python3 -c "
from PIL import Image; from pathlib import Path
fs=sorted(Path('final').glob('*.png')); w,h,c=270,337,4
S=Image.new('RGB',(c*w,((len(fs)+c-1)//c)*h),'white')
[S.paste(Image.open(f).convert('RGB').resize((w,h)),((i%c)*w,(i//c)*h)) for i,f in enumerate(fs)]
S.save('overview.jpg')"
```

## Validação visual

Antes de publicar, **abra `overview.jpg`** e cheque:
- [ ] Tipografia legível em mobile (zoom 50%)
- [ ] Texto SEM erros de letra (IA às vezes troca "AI" por "AL", "K" por "X")
- [ ] Paleta consistente entre slides
- [ ] Foto não tem dedos extras / olhos errados
- [ ] CTA (último slide) com código 5-char correto
- [ ] Sem watermarks indesejados (algumas IAs deixam logo do provider)

**Se errou alguma letra:** re-roll só o slide problemático com o mesmo prompt + nota "ensure text reads exactly: '...'".

## Custos típicos

> Custo é critério de desempate, nunca de escolha: o roteamento do PASSO 0 é por qualidade.

| Modelo | Custo por slide | Onde |
|---|---|---|
| OpenRouter `openai/gpt-5.4-image-2` | ~US$ 0,20 (medido set/2026) | Pay-per-use |
| Google AI Studio `gemini-3-pro-image` | grátis dentro da cota do free tier; pago se o projeto tiver billing | Google AI Studio |
| Google AI Studio `gemini-3.1-flash-image` | idem, mais barato que o Pro | Google AI Studio |
| Higgsfield `text2image_soul_v2` (com Soul ID) | ~3 créditos (~US$ 0.12) | Plus plan |

> Cota e preço do Google mudam: confira em https://aistudio.google.com/usage. Se der 429 `RESOURCE_EXHAUSTED`, a cota acabou; gere o slide sem rosto no OpenRouter com `openai/gpt-5.4-image-2` e avise o usuário.

## Quando re-rolar vs aceitar

**Re-roll obrigatório se:**
- Texto principal tem erro de letra
- Foto tem deformação visível (dedos extras, olhos errados, distorção facial)
- Paleta destoou muito do design system
- CTA ilegível

**Aceitar se:**
- Texto secundário tem 1 erro pequeno (você corrige no Pillow/Photoshop)
- Cores 95% no alvo
- Composição ok mesmo que não pixel-perfect

## Saída esperada

Se o usuário tiver uma pasta própria de carrosséis (ou um vault do Obsidian com regra de pasta), use a dele. Senão, diretório `recriar-{POST_ID}/` no diretório atual:
```
recriar-DXX/
├── referencia/         # JPGs do post original baixado
├── prompts/            # 1 .txt por slide
├── output/             # PNGs gerados pela IA
├── final/              # PNGs resized 1080x1350
├── analise-design.md   # Design system extraído
├── conteudo.md         # Textos adaptados PT-BR
└── overview.jpg        # Grid 4x2 pra revisão
```

## Anti-padrões

❌ **Não passe o prompt em PT-BR pro modelo de imagem** — modelos de imagem entendem inglês muito melhor. Texto que vai aparecer NO slide pode ser PT-BR (entre aspas no prompt), mas o restante do briefing em inglês.

❌ **Não use temperature/seeds aleatórias entre slides** — passe seed fixa OU prompts com mesma estrutura para manter coesão visual.

❌ **Não tente "Soul ID" sem treinar** — precisa treinar antes no Higgsfield com 15+ fotos. Sem treino, vai gerar rostos genéricos.

❌ **Não confie cegamente em texto** — sempre revise overview.jpg slide-by-slide antes de publicar. ~15% das vezes IA troca letras.

❌ **Não pule a etapa de análise (passo 3)** — gerar sem entender o design original = saída genérica que parece "AI slop".

## Fluxo híbrido (recomendado quando dá tempo)

Para carrossel premium:
1. Gere as FOTOS no Higgsfield (Soul ID, modelo consistente)
2. Monte LAYOUT + TIPOGRAFIA no Paper (texto perfeito, editável)
3. Exporte PNG/PDF do Paper

→ usa esta skill PARA as fotos + `recriar-carrossel` (Paper) PARA o layout.

## Pré-requisitos

- `APIFY_TOKEN` (se for baixar Instagram): https://console.apify.com/settings/integrations
- **Provedores de imagem:**
  - **Google AI Studio** — `GOOGLE_AI_STUDIO_API_KEY` (https://aistudio.google.com/apikey). Slides sem rosto.
  - **OpenRouter** — `OPENROUTER_API_KEY` (https://openrouter.ai/keys). GPT Image 2 pros slides com rosto.
  - **Higgsfield** (opcional, plano pago, só pra Soul ID / rosto consistente): https://higgsfield.ai
- Python 3 com `Pillow`, `httpx`, `python-dotenv`
- `sips` (já vem no macOS). No Windows e no Linux, redimensione com Pillow (`Image.open(f).resize((1080, 1350))`)

## Custo via OpenRouter

OpenRouter cobra por imagem gerada (pay-as-you-go, sem mensalidade). Nesta skill ele fica pro GPT Image 2:

| Modelo | ~Custo/slide | Carrossel 8 slides |
|---|---|---|
| `openai/gpt-5.4-image-2` | ~US$ 0,20 (medido set/2026, 1 ref, 4:5) | ~US$ 1,60 se todos tiverem rosto |

> Preços exatos variam — confira em https://openrouter.ai/models (filtra output:image). Pra estimar, gere 1 slide e veja o débito em https://openrouter.ai/activity.

## Referências

- [`materiais/comparativo-modelos.md`](materiais/comparativo-modelos.md) — qual modelo escolher por caso
- [`materiais/template-prompt.md`](materiais/template-prompt.md) — prompt master parametrizado
- [`materiais/exemplos-prompts.md`](materiais/exemplos-prompts.md) — prompts validados (capa, body, CTA)
- [`../recriar-carrossel/SKILL.md`](../recriar-carrossel/SKILL.md) — modo Paper (irmã)
