# Exemplo — Design System extraído ("Bubbly Bloom" / @secasetrincadas)

Esse é um exemplo **real e completo** de design system extraído de uma referência,
pra você ver o nível de detalhe esperado quando aplicar o template em casos novos.

Marca: bem-estar feminino. Produto: sachê diurético/antioxidante sabor pink lemonade.
Estética: editorial premium, feminina, "ciência + natureza".

---

## Formato

- **Proporção**: 4:5 vertical (1080 × 1350 px). Algumas capas em ~1080×1920.
- **Plataforma**: Instagram (carrossel).
- **Slides**: 8 (a capa tem 4 variações de foto — mesmo layout, drinks diferentes).

---

## Paleta

| Cor | Hex aprox. | Uso |
|---|---|---|
| Creme / off-white | `#F4EFE6` | fundo principal |
| Bordô / vinho | `#8B2A52` | blocos arredondados, barras, fundo dos slides de benefícios |
| Rosa claro | `#E8C5CE` | texto-fantasma gigante de fundo, flores de cerejeira |
| Grafite / charcoal | `#2B2B2B` | texto principal; caixas de texto escuras nos slides bordô |
| Branco off | `#FBF8F2` | texto sobre fundo bordô |
| Dourado fino | `#B79A5B` | linhas divisórias finas (rodapé, topo) |

**Regra**: 1 fundo (creme **ou** bordô) + texto charcoal/branco + 1 destaque (bordô **ou** rosa).

---

## Tipografia

Três níveis, sempre os mesmos:

1. **Serif display bold** — headlines fortes. Caixa-alta nas capas.
   Ex.: "BUBBLY", "Ciência e natureza juntinhas.", "como tomar"
   → Mapear pra **Playfair Display** (800) no Paper.

2. **Itálico script elegante** — palavras de destaque/charme.
   Ex.: "bloom?", "*água com gostinho*"
   → Mapear pra **Cormorant Garamond Italic** no Paper.

3. **Sans-serif geométrica** (body) — texto corrido e instruções.
   Ex.: "Link na BIO", "1 sachê em 300ml..."
   → Mapear pra **Poppins** no Paper.

Detalhes:
- Body com `text-align: justify` em algumas caixas.
- **Negrito** sans pra realçar palavras-chave.
- *Itálico* sans pra nuances.

---

## Elementos gráficos recorrentes

- **Textura de papel amassado** — overlay sutil em todos os slides.
- **Logo** — cacto de óculos escuros segurando um drink rosa (canto, ~80px).
- **Assinatura de rodapé** — `@secasetrincadas` + linha dourada fina.
- **Texto-fantasma** — palavra gigante em rosa claro de fundo ("bubbly", "bloom",
  "benefícios" girado 90°).
- **Blocos arredondados bordô** flanqueando a foto na capa.
- **Foto em rounded-square** (border-radius ~24px).
- **Caixas com borda pontilhada** nos slides de fundo bordô (texto charcoal dentro).
- **Linhas conectoras finas** (callout) ligando título a parágrafo.
- **Decorativos**: flores de cerejeira rosa-claro nas bordas; bolhas/bubbles translúcidas.
- **Barra inferior bordô** com texto branco centralizado (subtítulo/CTA).

---

## Anatomia — 8 slides

| # | Slide | Conteúdo |
|---|---|---|
| 1 | **Capa** | Serif pequeno "afinal.. o que é o" + display "BUBBLY *bloom?*" · foto da mulher c/ drink rosa entre 2 blocos bordô · barra inferior: "e porque você precisa ser uma Bubbly lover.." |
| 2 | **O que é** | "É o seu novo ritual **diário** de leveza. Um momento só seu para **cuidar de você!**" · diurético natural + antioxidante sabor pink lemonade · faixa bordô: "spoiler: fica **ainda** melhor com água com gás." |
| 3 | **Ciência** | "Ciência e natureza juntinhas." / "*água com gostinho*? É fórmula séria." · **Cactin** (cacto Opuntia ficus-indica → diurese sem perder minerais, detox) · **Drenow C** (Opuntia + Rosa canina + vit. C → celulite, TPM, pele) |
| 4 | **Benefícios I** (fundo bordô) | "adeus, retenção de líquido" (+27% eliminação, 68% menos inchaço) · "antioxidante poderoso, pele radiante" (betalaínas + vit. C) · "beleza que vem de dentro pra fora" |
| 5 | **Benefícios II** (fundo bordô) | "sua perna vai agradecer" (lipedema, drenagem, circulação) · "intestino feliz, cacto feliz" (regula intestino) · "tudo conectado, amor." |
| 6 | **Como tomar** | "como tomar" · 1 sachê em 300ml de água, 15min após o café; até 2 sachês/dia (2º até 17h) · dica: água com gás gelada · caixa com 30 sachês |
| 7 | **Prova social** | "o que as Cactos dizem" · prints de depoimentos de WhatsApp (colagem) |
| 8 | **CTA** | "Vem ser uma Bubbly lover!" · Link na BIO → WhatsApp · retirada local · envio Correios · "Sua versão mais **leve, linda e radiante** tá te esperando." |

---

## Tom de voz

Feminino, próximo, carinhoso ("amor", "cacto"), com humor leve (trocadilho
cacto/Cactos), mas ancorado em credibilidade ("fórmula séria", dados de %,
nomes dos ativos). Frases curtas, muito uso de **negrito** e *itálico* pra ritmo.

---

## Snippet base — fundo creme

```html
<div style="width:1080px; height:1350px; background:#F4EFE6;
            padding:90px; box-sizing:border-box; position:relative;
            font-family:'Poppins',sans-serif; color:#2B2B2B;
            display:flex; flex-direction:column;">

  <!-- Eyebrow -->
  <div style="font-family:'Playfair Display',serif; font-weight:700;
              font-size:34px;">afinal.. o que é o</div>

  <!-- Display headline (com 2 estilos em spans separados) -->
  <div style="font-family:'Playfair Display',serif; font-weight:800;
              font-size:120px; line-height:0.95; letter-spacing:1px;">
    <span>BUBBLY</span>
    <span style="font-family:'Cormorant Garamond',serif;
                 font-style:italic; font-weight:500;">bloom?</span>
  </div>

  <!-- Espacador fixo (NAO use flex-grow:1 em div vazio — vira altura 0) -->
  <div style="height:120px; flex-shrink:0;"></div>

  <!-- Barra inferior -->
  <div style="position:absolute; left:0; right:0; bottom:120px;
              background:#8B2A52; color:#FBF8F2; text-align:center;
              padding:22px; font-size:30px;">
    e porque você precisa ser uma Bubbly lover..
  </div>

  <!-- Handle -->
  <div style="position:absolute; left:90px; bottom:50px;
              color:#2B2B2B; opacity:0.7;">@secasetrincadas</div>
</div>
```
