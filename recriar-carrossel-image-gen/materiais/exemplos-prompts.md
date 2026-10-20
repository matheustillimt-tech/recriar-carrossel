# Exemplos de Prompts Validados

Prompts que rodaram em produção e funcionaram. Cole e adapte.

---

## Exemplo 1 — Capa educacional (GPT Image 2)

```
Instagram carousel COVER slide, vertical 3:4 ratio, 1080x1350.

DESIGN SYSTEM:
- Colors: #FFFFFF background, #000000 text, #FF6600 accent for highlight word
- Typography: bold sans-serif display "Inter Tight" or similar, very tight tracking
- Style: minimalist editorial, magazine-quality, brutal hierarchy
- Brand: "@seuhandle" small text bottom-right

LAYOUT: Headline fills 70% of canvas, top-aligned, left-justified. Small "1/8" indicator top-right. Swipe arrow icon bottom-right.

HEADLINE: "5 ERROS que te fazem PERDER dinheiro com IA"
- "5 ERROS" in 180pt bold caps
- "que te fazem" in 80pt regular
- "PERDER dinheiro" in 140pt bold with #FF6600 highlight on "PERDER"
- "com IA" in 100pt italic

SHOT: pure typography, no images, white background, scroll-stopping contrast.

QUALITY: sharp text rendering, no letter errors, mobile-readable at 50% zoom.
```

---

## Exemplo 2 — Capa com foto (Soul ID)

```
Instagram carousel COVER slide, vertical 3:4 ratio.

DESIGN: warm editorial — #F5E6D3 cream background, #2C2C2C text, soft natural lighting.

LAYOUT: photo of person fills bottom 65%, headline top 35% with cream background.

PERSON: <soul_seu_personagem> looking directly at camera, half smile, golden hour natural light, slightly leaning forward in conversation pose. White t-shirt. Studio backdrop blurred.

HEADLINE TOP (in cream area, bold serif):
"O que NINGUÉM te conta sobre criar conteúdo com IA"
- "NINGUÉM" in #8B2635 bordô bold

Caption bottom-right of photo: "@seuhandle | 1/8"

STYLE: magazine cover energy, editorial, premium feel, no stock-photo vibe.
```

---

## Exemplo 3 — Slide do meio (lista numerada)

```
Instagram carousel slide 3 of 8, vertical 3:4.

DESIGN SYSTEM (SAME as cover):
- #FFFFFF BG, #000000 text, #FF6600 accent
- Bold sans-serif display + clean sans body
- Minimalist editorial

LAYOUT:
- Large number "3" top-left in 320pt #FF6600
- Headline immediately below number, in 120pt black bold
- 3-line body text below, 48pt regular

CONTENT:
Number: "3"
Headline: "Não terceirizar tudo"
Body (3 lines, exact text):
"IA é ferramenta, não substituto.
Quem usa pra acelerar ganha 10x.
Quem usa pra escapar do trabalho, perde."

Footer: "@seuhandle | 3/8"

VISUAL: pure typography, no photo. Maximize whitespace.
```

---

## Exemplo 4 — Antes/Depois

```
Instagram carousel slide showing BEFORE/AFTER comparison, vertical 3:4.

DESIGN: clean modern split — left half BG #F0F0F0 (ANTES), right half BG #00FF88 (DEPOIS).

LAYOUT: vertical split 50/50.

LEFT (ANTES):
- Header label "ANTES" in 60pt bold gray
- Stat: "2h pra escrever 1 post"
- Sub: "manual, exaustivo, repetitivo"
- Small grayscale icon of clock

RIGHT (DEPOIS):
- Header label "DEPOIS" in 60pt bold black
- Stat: "10 min pra 5 posts"
- Sub: "IA + template + automação"
- Small green icon of lightning

Footer center: "@seuhandle | 5/8"

STYLE: contrast-driven, instant visual story.
```

---

## Exemplo 5 — CTA final (com código)

```
Instagram carousel FINAL CTA slide, vertical 3:4.

DESIGN: black background #000000, white text, orange accent #FF6600.

LAYOUT: massive call-to-action centered.

CONTENT:
Main headline (caps, 180pt bold):
"COMENTA"

Below in 220pt orange #FF6600:
"V2J8C"

Below in 80pt white:
"que eu te mando o link da Vibe Academy"

Bottom small (40pt white):
"@seuhandle | 8/8 | ↓ salva esse post"

STYLE: dramatic dark, single focal point, club-poster energy.
```

---

## Exemplo 6 — Nano Banana cartoon

```
Instagram carousel slide, illustrated cartoon style, vertical 3:4.

DESIGN: warm flat illustration, #FFE4B5 background, character with #FF6600 hoodie, line-art icons #2C2C2C.

LAYOUT: cartoon character left, speech bubble right.

CHARACTER: young developer pointing at laptop screen with surprised expression, cartoon style, flat colors, no realism.

SPEECH BUBBLE: "Espera... a IA fez ISSO em 30 segundos?!"

BACKGROUND: simple flat colored background, small icons of code symbols floating.

Footer: "@seuhandle | 4/8"

STYLE: editorial cartoon, NOT photorealistic, flat illustration like New Yorker editorial.
```

---

## Exemplo 7 — Higgsfield CLI (linha de comando completa)

```bash
# Slide 1 - capa premium
higgsfield generate create gpt_image_2 \
  --prompt "$(cat prompts/slide-01.txt)" \
  --aspect_ratio 3:4 \
  --resolution 2k \
  --quality high \
  --wait \
  --output ./output/slide-01.png

# Slides 2-7 - mid (mais barato, iterar rápido)
for i in 2 3 4 5 6 7; do
  printf "Gerando slide %02d...\n" $i
  higgsfield generate create gpt_image_2 \
    --prompt "$(cat prompts/slide-$(printf "%02d" $i).txt)" \
    --aspect_ratio 3:4 \
    --resolution 1k \
    --quality medium \
    --wait \
    --output ./output/slide-$(printf "%02d" $i).png
done

# Slide 8 - CTA premium
higgsfield generate create gpt_image_2 \
  --prompt "$(cat prompts/slide-08.txt)" \
  --aspect_ratio 3:4 \
  --resolution 2k \
  --quality high \
  --wait \
  --output ./output/slide-08.png
```

---

## Exemplo 8 — Lote roteado (sem rosto no Google, com rosto no OpenRouter)

Forma recomendada: um comando por slide, em paralelo, com o script certo pra cada tipo.

```bash
S=~/.claude/skills/recriar-carrossel-image-gen/scripts
R=~/.claude/skills/recriar-carrossel/perfil/rosto
# slide 01 tem o rosto do criador → GPT Image 2
python3 $S/generate_openrouter.py --model openai/gpt-5.4-image-2 --prompt-file prompts/slide-01.txt \
  --ref referencia/slide_01.jpg --ref $R/rosto-03.jpg --ref $R/rosto-05.jpg --out output/slide-01.png &
# slides 02..08 sem rosto → Gemini 3 Pro Image 2K
for i in 02 03 04 05 06 07 08; do
  python3 $S/generate_google.py --prompt-file prompts/slide-$i.txt \
    --ref referencia/slide_$i.jpg --out output/slide-$i.png &
done
wait
```

Loop equivalente em Python só pro formato OpenRouter (slides com rosto):

```python
import os, base64, time
import httpx
from pathlib import Path

API_KEY = os.environ["OPENROUTER_API_KEY"]
MODEL = "openai/gpt-5.4-image-2"  # slides com o rosto do criador

OUT = Path("output"); OUT.mkdir(exist_ok=True)

def b64(path):
    ext = Path(path).suffix.lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    return mime, base64.standard_b64encode(open(path, "rb").read()).decode()

def gen(prompt, refs, out):
    content = [{"type": "text", "text": prompt}]
    for p in refs:
        mime, data = b64(p)
        content.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}})
    payload = {"model": MODEL, "messages": [{"role": "user", "content": content}],
               "modalities": ["image", "text"]}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json",
               "HTTP-Referer": "https://conteudos.grupovortex.online", "X-Title": "Carrossel Image Gen"}
    r = httpx.post("https://openrouter.ai/api/v1/chat/completions",
                   headers=headers, json=payload, timeout=300)
    r.raise_for_status()
    for img in (r.json()["choices"][0]["message"].get("images") or []):
        url = img["image_url"]["url"]
        if ";base64," in url:
            open(out, "wb").write(base64.b64decode(url.split(";base64,", 1)[1]))
            return out
    raise RuntimeError("sem imagem na resposta")

for i, pf in enumerate(sorted(Path("prompts").glob("slide-*.txt")), start=1):
    print(f"Gerando slide {i:02d} ({MODEL})...")
    ref = f"referencia/slide-{i:02d}.jpg"   # original baixado (opcional)
    refs = [ref] if Path(ref).exists() else []
    gen(pf.read_text(), refs, OUT / f"slide-{i:02d}.png")
    time.sleep(3)   # previne 429 (rate limit)

print("✅ Todos slides gerados em output/")
```

> Ou use o script pronto: `scripts/generate_openrouter.py` (com retry automático 3× + sleep 20s em 503/timeout).

---

## Exemplo 9 — Python OpenAI gpt-image-1

```python
import os, base64
from openai import OpenAI
from PIL import Image
from io import BytesIO
from pathlib import Path

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

OUT = Path("output")
OUT.mkdir(exist_ok=True)

for i, prompt_file in enumerate(sorted(Path("prompts").glob("slide-*.txt")), start=1):
    print(f"Gerando slide {i:02d}...")
    prompt = prompt_file.read_text()
    r = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1536",
        quality="high",
        n=1,
    )
    img_data = base64.b64decode(r.data[0].b64_json)
    img = Image.open(BytesIO(img_data))
    img.save(OUT / f"slide-{i:02d}.png")

print("✅ Todos slides gerados em output/")
```

---

## Snippet — Resize + overview

```bash
# Resize todos pra 1080×1350 (4:5)
mkdir -p final
for f in output/slide-*.png; do
  sips -z 1350 1080 "$f" --out "final/$(basename "$f")"
done

# Overview pra revisão (4 colunas × 2 linhas)
montage final/slide-*.png -tile 4x2 -geometry +4+4 -background white overview.jpg
open overview.jpg
```

---

## Snippet — Re-roll de slide específico

Quando 1 slide saiu ruim (texto errado, foto deformada):

```bash
# Edita o prompt
nano prompts/slide-03.txt
# Adiciona no final: "CRITICAL: text must read EXACTLY 'Não terceirizar tudo' — no letter changes."

# Re-gera só esse slide
higgsfield generate create gpt_image_2 \
  --prompt "$(cat prompts/slide-03.txt)" \
  --aspect_ratio 3:4 --resolution 2k --quality high \
  --wait --output ./output/slide-03.png

# Resize de novo
sips -z 1350 1080 output/slide-03.png --out final/slide-03.png

# Recria overview
montage final/slide-*.png -tile 4x2 -geometry +4+4 overview.jpg
```
