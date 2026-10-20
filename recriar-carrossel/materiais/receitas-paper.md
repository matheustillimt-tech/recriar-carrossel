# Receitas Paper — snippets prontos

Coleção de blocos HTML/CSS que funcionam direto no `write_html` do Paper MCP.
Copia, cola, ajusta cor/texto.

> **Lembrete**: Paper só aceita inline styles + flex + padding + gap. Sem `margin`,
> sem `grid`, sem `display:inline`. `position:absolute` ok pra decorativos.

---

## 1. Artboard de slide (carrossel 4:5)

Use `create_artboard` com:

```js
create_artboard("01 - Capa", {
  display: "flex",
  flexDirection: "column",
  width: "1080px",
  height: "1350px",
  backgroundColor: "#F4EFE6",
  position: "relative",
  overflow: "hidden"
})
```

Pra story 9:16: `width:"1080px", height:"1920px"`. **Stories são fixos** — não
use `height:"fit-content"` (passaria de 1920).

---

## 2. Flex-wrap de palavras (rich text emulado)

Pra ter cor/peso/itálico diferentes dentro de um parágrafo (que Paper achata
no estilo base). Cada palavra vira um span / text node próprio.

```html
<div style="display:flex; flex-wrap:wrap; align-items:baseline;
            column-gap:9px; row-gap:5px; width:560px;
            font-family:'Poppins',sans-serif; font-size:32px;
            line-height:1.42; color:#2B2B2B;">
  <span>Um</span>
  <span>diurético</span>
  <span style="font-weight:700;">natural</span>
  <span>e</span>
  <span style="font-weight:700;">antioxidante</span>
  <span>com</span><span>sabor</span><span>de</span>
  <span style="color:#8B2A52; font-weight:600;">pink</span>
  <span style="color:#8B2A52; font-weight:600;">lemonade</span>
  <span>que</span><span>vira…</span>
  <span style="font-style:italic;">refrescante,</span>
  <span style="font-style:italic;">delicioso…</span>
</div>
```

Calibre o `column-gap` pelo tamanho da fonte:
- ~30px → `8px`
- ~32–34px → `9px`
- ~46–50px (títulos) → `12–14px`

---

## 3. Título com 2 estilos (display + script)

Como filhos diretos já viram text nodes distintos, NÃO precisa de flex-wrap:

```html
<div style="font-family:'Playfair Display',serif; font-weight:800;
            font-size:120px; line-height:0.95; letter-spacing:1px;
            color:#2B2B2B;">
  <span>BUBBLY</span>
  <span style="font-family:'Cormorant Garamond',serif;
               font-style:italic; font-weight:500;">bloom?</span>
</div>
```

---

## 4. Foto otimizada com object-fit

Sempre redimensione antes (`sips -Z 1080 in.png --out out_1080.png`).

```html
<img src="paper-asset:///Users/voce/projeto/assets/foto_1080.jpg"
     style="width:500px; height:500px; object-fit:cover;
            object-position:center top; border-radius:24px;">
```

3 barras no protocolo `paper-asset:///`. Caminho **absoluto**.

---

## 5. Vinheta escura (pra texto branco sobre foto)

Pra stories ou capas com foto + texto branco em cima. Vinheta mais pesada no
topo (onde mora o texto) e na base, mais leve no meio (pra ver o rosto):

```html
<div style="position:absolute; inset:0;
            background:linear-gradient(180deg,
              rgba(0,0,0,0.93) 0%,
              rgba(0,0,0,0.82) 20%,
              rgba(0,0,0,0.60) 40%,
              rgba(0,0,0,0.50) 56%,
              rgba(0,0,0,0.52) 70%,
              rgba(0,0,0,0.74) 86%,
              rgba(0,0,0,0.93) 100%);
            pointer-events:none;"></div>
```

---

## 6. Barra full-width (faixa de cor)

```html
<div style="width:1080px; background:#8B2A52;
            display:flex; justify-content:center;
            padding:24px 70px; box-sizing:border-box;
            color:#FBF8F2; font-family:'Poppins'; font-size:30px;
            text-align:center;">
  spoiler: fica ainda melhor com água com gás.
</div>
```

---

## 7. Moldura pontilhada (caixa de destaque)

```html
<div style="border:2px dashed rgba(244,239,230,0.45);
            border-radius:10px; padding:28px 32px;
            color:#2B2B2B; font-family:'Poppins'; font-size:28px;">
  texto dentro da caixa pontilhada
</div>
```

---

## 8. Texto-fantasma decorativo (de fundo)

Palavra gigante translúcida no fundo do slide:

```html
<div style="position:absolute; top:100px; left:-50px;
            font-family:'Playfair Display',serif; font-weight:800;
            font-size:280px; color:rgba(216,178,190,0.30);
            white-space:nowrap; pointer-events:none;
            letter-spacing:-5px;">
  bubbly
</div>
```

Pra texto vertical (girado): adicione `transform: rotate(90deg);`.

---

## 9. Bolha translúcida

```html
<div style="width:120px; height:120px; border-radius:50%;
            background:rgba(214,180,150,0.15);
            border:1px solid rgba(193,151,120,0.3);
            position:absolute; top:200px; right:100px;"></div>
```

---

## 10. Flor de cerejeira (SVG inline, sem asset)

```html
<svg width="150" height="150" viewBox="0 0 100 100">
  <g fill="#E7AEBE">
    <ellipse cx="50" cy="24" rx="15" ry="22"/>
    <ellipse cx="50" cy="24" rx="15" ry="22" transform="rotate(72 50 50)"/>
    <ellipse cx="50" cy="24" rx="15" ry="22" transform="rotate(144 50 50)"/>
    <ellipse cx="50" cy="24" rx="15" ry="22" transform="rotate(216 50 50)"/>
    <ellipse cx="50" cy="24" rx="15" ry="22" transform="rotate(288 50 50)"/>
  </g>
  <circle cx="50" cy="50" r="8" fill="#E6C84F"/>
</svg>
```

---

## 11. Card branco arredondado (com sombra)

```html
<div style="background:#FFFFFF; border-radius:24px;
            padding:36px 40px; display:flex; flex-direction:column;
            gap:18px; box-shadow:0 8px 24px rgba(0,0,0,0.06);
            width:920px; box-sizing:border-box;">
  <!-- conteudo do card aqui -->
</div>
```

---

## 12. Chips/pílulas (categoria, stat, marca)

```html
<!-- Stat primario verde -->
<div style="display:inline-flex; align-items:center; gap:8px;
            background:#3E8E5A; color:#FFFFFF;
            padding:8px 16px; border-radius:999px;
            font-family:'Hanken Grotesk'; font-size:20px; font-weight:600;">
  ★ 5,0k estrelas
</div>

<!-- Categoria tan -->
<div style="display:inline-flex; align-items:center;
            background:#E2DAC8; color:#1A1A1A;
            padding:8px 16px; border-radius:999px;
            font-family:'Hanken Grotesk'; font-size:20px; font-weight:500;">
  Claude Code
</div>

<!-- Marca coral-claro -->
<div style="display:inline-flex; align-items:center;
            background:#F1DACB; color:#C8552E;
            padding:8px 16px; border-radius:999px;
            font-family:'Hanken Grotesk'; font-size:20px; font-weight:600;">
  Google, Meta, TikTok
</div>
```

---

## 13. CTA pill (botão preto com seta colorida)

```html
<div style="display:inline-flex; align-items:center; gap:14px;
            background:#1A1A1A; color:#FFFFFF;
            padding:22px 36px; border-radius:999px;
            font-family:'Hanken Grotesk'; font-size:28px; font-weight:700;
            letter-spacing:0.02em;">
  COMENTA "VIBE" PRA RECEBER
  <span style="color:#EE6E3F;">→</span>
</div>
```

---

## 14. Espaçador (NÃO use flex-grow:1 em div vazio)

Pra empurrar conteúdo pra base do artboard:

```html
<div style="height:120px; flex-shrink:0;"></div>
```

Ajuste o `height` olhando o screenshot. Se sobrar muito no fim do artboard,
troque o artboard pra `height:"fit-content"` via `update_styles` (não chute px novo).

---

## 15. Reuso de rodapé entre artboards

Construa o rodapé uma vez no primeiro artboard. Depois:

```js
duplicate_nodes([{
  id: "<rodape_id>",
  parentId: "<novo_artboard_id>"
}])
```

Se quiser reusar um rodapé editado em vários artboards, faça isso em loop.

---

## 16. Trocar foto de um slide já montado (sem desmontar)

Use `write_html(mode:"replace")` no nó da `<img>`. Preserva z-order (vinheta e
texto continuam por cima):

```js
write_html({
  nodeId: "<img_node_id>",
  mode: "replace",
  html: '<img src="paper-asset:///caminho/nova-foto.jpg" style="..." >'
})
```

---

## 17. Export PNG em alta (2x)

```js
export({
  nodes: [
    { nodeId: "<artboard_id_01>", format: "png", scale: "2x" },
    { nodeId: "<artboard_id_02>", format: "png", scale: "2x" }
    // ... ate 8-10 por chamada
  ]
})
```

Sai pra `~/Downloads` com o nome do artboard. Pra carrossel: 2160×2700.

PDF combinado (todos slides num arquivo só):

```js
export_combined_pdf({ nodeIds: ["<id_01>", "<id_02>", ...] })
```
