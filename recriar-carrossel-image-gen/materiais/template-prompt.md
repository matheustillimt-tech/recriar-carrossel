# Template de Prompt Master

Template parametrizado pra gerar cada slide. Cole, preencha entre `<...>`, mande pro modelo.

---

## Template — Slide individual

```
Instagram carousel slide, 1080x1350px, vertical 4:5 ratio (or 3:4 if model only supports that).

DESIGN SYSTEM:
- Color palette (hex): <#hex1>, <#hex2>, <#hex3>, <#accent>
- Typography: <ex: bold serif display headline + clean sans-serif body>
- Visual style: <ex: minimalist editorial / bubbly playful / brutalist tech / clean corporate>
- Brand element: <ex: "small @username watermark bottom-right" OR "no watermark">

LAYOUT (slide N of <total>):
- <ex: "Headline takes top 40%, image bottom 60%, CTA bottom-center">
- Hierarchy: HEADLINE > subheadline > body > caption
- Margins: <ex: "120px from edges, breathable whitespace">

CONTENT (text must render PERFECTLY, exact characters):
- Slide number/page indicator: "<ex: 1/8>"
- Headline (large bold): "<TEXTO EXATO ENTRE ASPAS>"
- Subheadline (medium): "<TEXTO EXATO ENTRE ASPAS>"
- Body (small): "<TEXTO EXATO ENTRE ASPAS>"
- CTA (if applicable): "<TEXTO EXATO ENTRE ASPAS>"

VISUAL ELEMENT:
- <ex: "photo of person looking at camera, natural lighting, golden hour">
- OR <ex: "abstract gradient background, no people">
- OR <ex: "illustrated icon of a brain, minimal line art">
- Soul ID: <soul_xxx OR "skip">

QUALITY REQUIREMENTS:
- Sharp text rendering, no letter mistakes
- Consistent with previous slides in this carousel
- No deformed faces, no extra fingers, no AI artifacts
- No watermark from the AI provider
- High contrast, mobile-readable

NEGATIVE PROMPT (avoid):
- Blurry text, illegible characters
- Cluttered composition
- Generic stock photo look
- Multiple competing focal points
```

---

## Template — Capa (slide 1)

```
Instagram carousel COVER slide, 1080x1350px, vertical 4:5.

DESIGN: <design system as above>

GOAL: HOOK. Stop the scroll. Maximum visual punch.

LAYOUT:
- Headline takes 60% of the canvas, very large bold
- Background image or color block
- Small "ARRASTA →" / "swipe →" indicator bottom-right
- Author handle "@<username>" subtle at top or bottom

HEADLINE (must hook):
"<EXACT HEADLINE TEXT IN QUOTES>"

(Use the same headline formulas as YouTube: shock + number + benefit + curiosity gap.)

VISUAL: <photo OR background OR illustration>

STYLE: scroll-stopper, high contrast, instantly readable in feed thumbnail.
```

---

## Template — CTA (último slide)

```
Instagram carousel FINAL CTA slide, 1080x1350px, vertical 4:5.

DESIGN: <same design system>

GOAL: drive action — comment, save, share, click bio.

LAYOUT:
- Big call to action centered
- Author handle prominent
- Optional: profile photo

CONTENT:
- Headline (CTA action): "<ex: COMENTA 'VIBE' QUE EU TE MANDO O LINK>"
- Sub-line: "<ex: ↓ Salva esse post pra não perder">
- Code (5-char): "<ex: V2J8C>"
- Author: "@<username>"

STYLE: clear, focused, single action.
```

---

## Variáveis comuns por design system

### Identidade "Editorial Clean" (exemplo)
```
- Colors: #FFFFFF (BG), #000000 (texto), #FF6600 (accent), #FFD500 (highlight)
- Typography: bold serif display + clean sans body
- Style: minimalist editorial, bold typography forward
- Brand: small @seuhandle bottom-right
```

### Identidade "Bubbly Bloom"
```
- Colors: #F5E6D3 (cream BG), #8B2635 (bordô), #2C2C2C (texto), #D4A373 (gold accent)
- Typography: mixed BUBBLY display (caps, rounded) + lowercase italic bloom serif
- Style: warm editorial, soft natural lighting, organic shapes
- Brand: handwritten signature mark
```

### Identidade "Tech Minimal"
```
- Colors: #000000 (BG), #FFFFFF (texto), #00FF88 (accent neon)
- Typography: monospace caps headline + sans body
- Style: brutalist tech, grid layouts, neon glows
- Brand: monogram icon top-left
```

## Modificadores que ajudam

Adicione no final do prompt:

- `"professional graphic design, magazine-quality typography"`
- `"sharp readable text rendering"`
- `"consistent with carousel slide deck design"`
- `"trending on Behance, Awwwards-worthy"`
- `"no AI artifacts, no extra limbs, no text errors"`
- `"shot on Hasselblad, natural daylight"` (para fotos)
- `"isometric vector illustration, flat colors"` (para ilustração)

## Modificadores que PIORAM

Evite:

- ❌ `"perfect"` (modelo "perfeito" piora composição)
- ❌ `"best quality, masterpiece, 8k"` (chavões antigos)
- ❌ Prompt muito longo (>500 palavras) — modelos cortam
- ❌ Múltiplas instruções contraditórias
- ❌ Aspectos misturados ("16:9 photo of a vertical slide")

## Como manter coesão entre slides

1. **Fixe o modelo** — não troque entre slides
2. **Repita o bloco DESIGN SYSTEM** em TODOS os prompts
3. **Use seed fixa** se o modelo permitir (`--seed 12345`)
4. **Mesmo aspect_ratio + resolution** em todos
5. **Mesmas keywords de mood** ("natural lighting", "minimalist")
6. **Slide 1 e último mais elaborados**, slides do meio mais limpos
