# Design System — {NOME DA REFERÊNCIA / MARCA}

> Template — preencha cada seção olhando os slides da referência. Salva como
> `design-system-{slug}.md` na pasta do trabalho.

---

## Metadados

- **Referência**: {URL do post ou nome da pasta de imagens}
- **Autor original**: @{handle}
- **Plataforma**: Instagram / LinkedIn / outro
- **Quantidade de slides**: {N}
- **Data da extração**: {YYYY-MM-DD}

---

## Formato

- **Proporção**: 4:5 vertical (carrossel padrão Instagram)
- **Resolução**: 1080 × 1350 px
- **Variações**: {ex.: capa em 1080×1920, ou mesmo formato em todos}

---

## Paleta

Amostre os hex direto das imagens (use uma ferramenta tipo "Digital Color Meter"
no Mac, ou pergunte ao Claude pra extrair via análise da imagem).

| Cor | Hex | Uso |
|---|---|---|
| Fundo principal | `#XXXXXX` | fundo creme / claro / etc. |
| Acento / destaque | `#XXXXXX` | títulos, barras, CTA |
| Texto principal | `#XXXXXX` | corpo de texto |
| Texto secundário | `#XXXXXX` | legendas, footnotes |
| Cor decorativa 1 | `#XXXXXX` | flores, blocos, gradientes |
| Cor decorativa 2 | `#XXXXXX` | (se houver) |

**Regra do design**: 1 fundo + texto + 1 acento. (Ou descreva a regra que viu.)

---

## Tipografia

| Papel | Família | Peso | Tamanho aprox. | Notas |
|---|---|---|---|---|
| Headline display (capas) | {ex.: Playfair Display serif} | 800 | 120px | caixa-alta? itálico no gancho? |
| Título de slide | {ex.: Hanken Grotesk} | 700 | 64px | |
| Subtítulo / eyebrow | {ex.: Poppins} | 600 | 28px | letter-spacing alto? |
| Corpo de texto | {ex.: Poppins} | 400 | 32px | line-height 1.4 |
| Itálico de charme | {ex.: Cormorant Garamond Italic} | 500 | varia | só palavras-chave |
| Kicker / contador | {ex.: Hanken Grotesk Bold CAIXA ALTA} | 700 | 18px | tracking alto |

> Confirme as fontes com `get_font_family_info` no Paper antes de estilizar.

---

## Elementos gráficos recorrentes

Lista da "cara" da marca — elementos que aparecem em **vários slides**:

1. **{Elemento 1}** — ex.: flag/bookmark terracota no canto superior esquerdo
2. **{Elemento 2}** — ex.: pílula branca com @handle no topo-centro
3. **{Elemento 3}** — ex.: grid sutil no fundo
4. **{Elemento 4}** — ex.: seta → terracota no canto inferior direito
5. **{Elemento 5}** — ex.: contador "0N / NN" embaixo

Decorativos pontuais (aparecem em alguns slides):
- Flores de cerejeira
- Bolhas translúcidas
- Texto-fantasma gigante de fundo
- Caixas com borda pontilhada
- Linhas conectoras finas (callouts)
- Outros: {...}

---

## Anatomia slide a slide

| # | Tipo | Conteúdo / estrutura |
|---|---|---|
| 1 | **Capa** | foto full-bleed + headline serif + gancho em itálico + kicker em caixa-alta |
| 2 | **Conteúdo #1** | #1 colorido + título bold + card branco arredondado + corpo + chips |
| 3 | **Conteúdo #2** | (mesma estrutura do anterior) |
| ... | ... | ... |
| N-1 | **{Tipo diferente}** | ex.: prints de depoimentos colados |
| N | **CTA** | título + 3 bullets de benefício + pill preto "COMENTA X" |

---

## Tom de voz

{Descreve em 2-3 frases.}

Exemplos:
- Premium founder, didático, sem gírias, frases curtas e diretas.
- Feminino próximo, carinhoso ("amor"), humor leve, ancorado em credibilidade.
- Técnico descontraído, muita analogia, emoji ocasional.

---

## Snippet base (Paper / `write_html`) — fundo {cor}

```html
<style>
  :root {
    --bg: #XXXXXX;
    --accent: #XXXXXX;
    --ink: #XXXXXX;
  }
  .slide {
    width: 1080px; height: 1350px;
    background: var(--bg);
    padding: 90px;
    box-sizing: border-box;
    position: relative;
    font-family: 'Poppins', sans-serif;
    color: var(--ink);
  }
  .eyebrow {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 34px;
  }
  .display {
    font-family: 'Playfair Display', serif;
    font-weight: 800;
    font-size: 120px;
    line-height: 0.95;
  }
</style>
<div class="slide">
  <div class="eyebrow">eyebrow text</div>
  <div class="display">HEADLINE</div>
</div>
```

(Lembre-se: no Paper o CSS vai inline; o `<style>` aqui é só pra documentar a
intenção. Na hora de escrever no Paper, transforme em `style="..."` em cada
elemento.)
