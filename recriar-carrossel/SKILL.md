---
name: recriar-carrossel
description: Recria um carrossel de Instagram idêntico a uma referência visual, trocando apenas o conteúdo. Use quando o usuário quiser clonar um carrossel viral (próprio ou de outro perfil) mantendo o design e adaptando o texto. Requer Paper MCP instalado.
---

# Recriar Carrossel

Skill pra **clonar um carrossel de Instagram** mantendo o design 1:1 e trocando só o conteúdo. O cliente manda uma referência (print, URL ou arquivos de imagem) + o tema/texto novo, e você reconstrói tudo dentro do **Paper Design** (via MCP), pronto pra exportar PNG/PDF e publicar.

> **Pré-requisito**: Paper Desktop aberto + Paper MCP conectado no Claude Code. Se não estiver, ver seção "Setup do Paper" no final.
>
> **Primeira vez?** Leia a seção "Primeira vez (configuração)" logo abaixo antes de começar.

---

## Primeira vez (configuração)

Faça só o que o pedido precisar, na hora em que precisar. Nada de pedir todas as chaves de uma vez.

1. **Paper:** rode `lsof -i :29979`. Se não voltar nada, ou se os tools `mcp__paper__*` não existirem, guie o usuário pela seção "Setup do Paper" no fim deste arquivo.
2. **Chaves de API:** ficam num arquivo só, `~/.claude/skills/recriar-carrossel/.env` (modelo em `.env.example`). Se o arquivo não existir, copie o modelo, peça ao usuário só a chave que o pedido precisa e grave com `chmod 600`. Nunca mostre a chave no chat depois de gravada.
   - `APIFY_TOKEN`: só pra baixar a referência pelo link do Instagram (sem ela, o usuário manda os prints).
   - `OPENROUTER_API_KEY`: só pra gerar foto nova com IA (Fase 4B).
3. **Perfil do criador:** fica em `~/.claude/skills/recriar-carrossel/perfil/` (`perfil.md` com @, nome, cores da marca e o caminho do documento de tom de voz; `avatar.jpg` = foto de perfil; `rosto/` = 3 a 5 fotos do rosto). Se não existir e o carrossel precisar do @, da foto ou do rosto do criador, pergunte e crie a pasta. As duas skills (`recriar-carrossel` e `recriar-carrossel-image-gen`) leem o mesmo perfil.
4. **Python:** os scripts precisam de `pip3 install httpx python-dotenv pillow`. Instale se faltar, avisando o usuário.

---

## Quando usar essa skill

Ative quando o usuário pedir coisas como:

- "Recria esse carrossel pra mim" + manda print/URL
- "Clona esse post do @fulano trocando o assunto pra X"
- "Pega esse carrossel que viralizou e adapta pra minha marca"
- "Faz igual a esse aqui mas com meu produto"

Não é pra:
- Criar carrossel **do zero** sem referência visual (usa outra skill, ou pede pro usuário escolher uma referência).
- Editar carrossel que **já está** no Paper (aí é direto na ferramenta).

---

## Visão geral em 7 fases

```
0. Entrada       → conseguir as imagens da referência
1. Transcrição   → ler cada slide e registrar TODO o texto + anatomia
2. Design system → extrair paleta, fontes, decorativos
3. Adaptação     → reescrever o conteúdo com o tema do cliente, na voz do criador (doc de voz) + aprovação
4. Fotos         → reusar da referência ou gerar nova com IA
5. Build no Paper→ slide a slide, screenshot a cada um
6. Revisão+Export→ checklist final e export PNG/PDF
```

Faça **uma fase por vez**, em sequência. Não pule a Fase 1 (transcrição) — sem ela o resto desanda.

---

## Fase 0 — Entrada (conseguir as imagens da referência)

Três caminhos, do mais automático pro mais manual:

### A) URL do Instagram (preferido)
Se o usuário mandou `instagram.com/p/XXXXX/`, baixe sozinho usando o **Apify Instagram Scraper**. Não peça as imagens pro usuário — economiza um round-trip.

**Setup do token Apify** (uma vez):
1. Cliente cria conta em [apify.com](https://apify.com) (free tier serve pra testar).
2. Pega o token em Settings → Integrations.
3. Grava no `.env` da skill: `APIFY_TOKEN=<SEU_TOKEN_AQUI>`.

**Script de download** (`materiais/download-apify.py`, lê `APIFY_TOKEN` do `.env` da skill, `~/.claude/skills/recriar-carrossel/.env`):

```bash
python3 ~/.claude/skills/recriar-carrossel/materiais/download-apify.py "<URL_DO_POST>" "<PASTA_DO_CARROSSEL>/referencia"
```

Pontos críticos do Apify (já validados na prática):
- POST em `https://api.apify.com/v2/acts/apify~instagram-scraper/runs?waitForFinish=120` com body `{"directUrls":[URL],"resultsLimit":1}` e header `Authorization: Bearer $APIFY_TOKEN`.
- **Sucesso retorna HTTP 201** (não 200) — trate ambos.
- Resposta traz `defaultDatasetId` → GET em `/datasets/{id}/items` **também com o header `Authorization`** (sem ele a API responde `insufficient-permissions` e o script quebra).
- Carrossel chega como `type:"Sidecar"`, slides em `childPosts[].displayUrl`. Foto única: `displayUrl` na raiz.
- Salve `slide_NN.jpg` + `metadata.json` (com a caption original) na pasta da referência.

### B) Imagens locais
Cliente coloca os JPGs/PNGs numa subpasta (ex.: `referencia-meu-cliente/`). Você lê dali com a tool `Read`.

### C) Print único / colado no chat
Aceita também — você lê direto da mensagem. Se for só 1 print, pergunte se tem os outros slides; se não, segue com o que tem.

> **Regra de ouro**: salve sempre numa pasta dedicada ao carrossel pra não misturar com outros trabalhos (ver "Onde salvar" no fim).

---

## Fase 1 — Transcrição (não pule)

Pra **cada slide**, use a tool `Read` (visão) na imagem e registre numa tabela mental ou num doc:

- **Todo o texto**, exatamente como está no idioma original. Separe por: título / subtítulo / corpo / legendas / CTA.
- **Hierarquia tipográfica** — o que é grande, médio, pequeno; o que é bold / itálico / colorido.
- **Posição** dos elementos — topo / centro / base, esquerda / direita.
- **Fotos** — o que mostram (rosto, produto, lifestyle, etc.).
- **Decorativos** — flores, bolhas, ícones, texto-fantasma de fundo, blocos, molduras, linhas, gradientes.

Monte uma "**anatomia dos N slides**" estilo tabela. Exemplo em `materiais/exemplo-anatomia.md`.

> Por que isso importa: sem transcrição literal, a tradução/adaptação vira inventiva. E a referência visual vira "lembrança", não cópia.

---

## Fase 2 — Design System

Extraia e escreva um doc `design-system-{marca}.md` (template em `materiais/template-design-system.md`):

**Formato** — proporção e px. Carrossel Instagram padrão = **1080×1350 (4:5)**.

**Paleta** — 4 a 6 hex **amostrados das imagens** (use a tool `Read` se precisar, ou peça pro cliente). Nomeie o papel de cada cor: fundo / primária-destaque / texto / neutros / acentos.

**Tipografia** — identifique as famílias visualmente e **mapeie pra Google Fonts** (todas disponíveis no Paper). Combos testados:

| Estilo da referência | Google Font sugerida |
|---|---|
| Serif display editorial | **Playfair Display** (800/900) ou **PT Serif** Bold |
| Script italic elegante | **Cormorant Garamond Italic** |
| Corpo sans geométrico | **Poppins** |
| Grotesk moderno | **Inter**, **Inter Tight**, **Hanken Grotesk**, **Archivo** |

**Elementos gráficos recorrentes** — logo, assinatura/handle, molduras, flores, bolhas, ícones, blocos, linhas divisórias.

**Anatomia slide a slide** — repete o que você fez na Fase 1 numa visão consolidada.

**Tom da referência** — feminino próximo? premium founder? técnico didático? humor? Anote só como leitura da estrutura: o texto final **não** copia esse tom, segue a voz do criador (Fase 3).

---

## Fase 3 — Adaptação do conteúdo

Aqui você troca o **conteúdo** e mantém a **estrutura** da referência. O **tom** é o do criador, não o da referência.

### 3.0) Tom de voz (obrigatório, antes de escrever qualquer texto)

1. Veja se o `perfil.md` (`~/.claude/skills/recriar-carrossel/perfil/perfil.md`) aponta um documento de tom de voz. Se não apontar, pergunte se o usuário tem um (um arquivo que descreve como ele escreve e fala) e anote o caminho no `perfil.md`.
2. **Leia o doc inteiro.** Ele manda em: regras duras, bordões, vocabulário (usar/evitar), cadência da escrita, esqueleto do carrossel, hooks e CTAs. Se o tom da referência brigar com o doc de voz, **o doc de voz vence** (vale pra tradução 3.1 e adaptação 3.2).
3. Sem doc de voz: peça 3 adjetivos do tom dele e 1 ou 2 textos que ele já escreveu (uma legenda serve), e escreva igual.

Dois cenários:

### 3.1) Tradução EN → PT-BR (referência gringa)
- **Fidelidade de sentido, NÃO literal.** O registro final é o do doc de voz (3.0), não o da referência gringa.
- **Mantenha**: nomes de marca, produto, ingredientes, números/claims, @handle.
- **Adapte**: gírias, trocadilhos, CTAs ("Link in bio" → "Link na BIO", "DM us" → "chama no direct"), unidades.
- **Comprimento**: PT-BR costuma ser 15–20% mais longo que EN. Confira se ainda cabe no layout (senão ajuste font-size).
- Registre EN | PT lado a lado pra revisão.

### 3.2) Mesmo idioma, novo tema (adaptação)
- Mantenha a **fórmula** dos slides (capa-gancho → conteúdo numerado → CTA, por exemplo).
- Troque os exemplos/dados pelo tema do cliente.
- **Nunca invente dado, número, feature ou "hack"** que não existe. Se o cliente não te passou, pergunte.
- **Tom de voz:** texto dos slides e legenda seguem o doc de voz lido no 3.0.
- **CTA:** se o carrossel pedir comentário ("comenta X que eu te mando"), use a palavra ou o código que o usuário definir. Se ele não tiver, sugira um código curto que ninguém escreveria por acaso e sem letras que se confundem (0/O, 1/I/l).
- Se um slide é gringo/irrelevante demais pra realidade do cliente, **corta** — não force.

### Regras de honestidade (valem sempre)
- Atribuição da referência no doc final (`baseado_em: {URL ou nome}`).
- Sem inventar autoridade ("estudo da Harvard" sem fonte → não).
- Sem travessão (`-` `—` `–`) como separador em copy publicada (use vírgula, ponto, reticências).

### 3.3) Aprovação (NÃO PULE)
Mostre ao usuário a tabela `Slide | Texto original | Texto novo` + rascunho de legenda + CTA, com o "Checklist final" do doc de voz conferido. **Só vá pra Fase 4/5 depois do ok.** Texto errado depois de montado no Paper custa chamada MCP e retrabalho.

---

## Fase 4 — Fotos

Duas opções:

### A) Reusar fotos da referência
Mais fiel. Se conseguir extrair/recortar a foto isolada (sem o texto sobreposto), use. Sempre redimensione antes de inserir no Paper:

```bash
sips -Z 1080 in.jpg --out out_1080.jpg
```

(Alvo: ~1080px de lado maior, arquivo <2MB.)

### B) Gerar foto nova com IA
Quando não dá pra extrair a foto, ou quando o cliente quer trocar (ex.: foto do **dele** na capa em vez da do gringo).

- **Padrão:** GPT Image 2 via OpenRouter com as fotos de rosto do perfil (`~/.claude/skills/recriar-carrossel/perfil/rosto/`) como referência. **Foto com o rosto do criador = sempre modelo GPT**, nunca Gemini (rosto sai pouco realista). Se o `perfil.md` tiver regras de modelo escritas pelo usuário, elas mandam.

  ```bash
  python3 ~/.claude/skills/recriar-carrossel-image-gen/scripts/generate_openrouter.py \
    --prompt "Photorealistic photo of ... NO text, NO watermark" \
    --ref ~/.claude/skills/recriar-carrossel/perfil/rosto/rosto-01.jpg \
    --model openai/gpt-5.4-image-2 --aspect-ratio 4:5 --out _assets/foto.png
  ```
- **Alternativa:** **Higgsfield** (https://higgsfield.ai), modelo `gpt_image_2` na qualidade `2k high` (Soul ID pra rosto consistente).

Dicas de prompt:
- Descreva cabelo, roupa, objeto, luz, fundo — pra casar com a estética da referência.
- **Sem texto/watermark na imagem** (o texto vai no Paper).
- Se for foto da pessoa do cliente (ex.: capa do influencer), treine um **Soul ID / character LoRA** antes pra ter consistência de rosto entre slides.

Outras opções: Midjourney, DALL-E 3, Flux. Qualquer um serve — o importante é manter a estética da referência.

Depois, redimensiona com `sips -Z 1080 foto.png --out foto_1080.png` e move pra uma pasta `_assets/` perto do projeto.

---

## Fase 5 — Build no Paper (slide a slide)

**Checklist de abertura de sessão Paper** (toda vez):

1. Confirme o Paper Desktop aberto com um arquivo: `lsof -i :29979` (precisa retornar algo).
2. **Primeiro tool**: `get_guide({topic:"paper-mcp-instructions"})` — obrigatório.
3. `get_basic_info` — vê arquivo, página, fontes carregadas, artboards existentes.
4. `get_font_family_info(["<fonte1>","<fonte2>"])` — confirme as fontes do design.
5. `create_page` → `open_page` com nome do trabalho (ex.: "Carrossel — Como Ganhar 1k Followers"). **Nunca suje uma página existente.**

**Pra cada slide:**

1. `create_artboard` com `width:"1080px"`, `height:"1350px"`, `backgroundColor:"<hex>"`, `position:"relative"`, `overflow:"hidden"`, `display:"flex"`, `flexDirection:"column"`.
2. Monte **um grupo visual por chamada `write_html`** — assim o usuário vê em tempo real. Ordem típica: decorativos de fundo → topo (flag/handle) → headline → corpo → barras → rodapé.
3. Fotos: `<img src="paper-asset:///caminho/absoluto/foto_1080.png" style="...">` (3 barras no protocolo).
4. Elementos repetidos (rodapé, handle do canto): construa **uma vez** e use `duplicate_nodes([{id, parentId: outroArtboard}])` nos outros.
5. `get_screenshot` **do artboard inteiro** (não de nós isolados — ver armadilha #4). Avalie e corrija.
6. `finish_working_on_nodes` quando o slide estiver ok.

**Truque pra slides parecidos** (ex: "benefício 1", "benefício 2", "benefício 3"): use `duplicate_nodes` do artboard inteiro e troque o conteúdo com `set_text_content` ou `write_html(mode:"replace")` em nós específicos.

---

## Armadilhas críticas do Paper (LEIA antes de construir)

Dez coisas que **vão te morder** se não conhecer:

### 1. Paper NÃO suporta rich text
Cor / peso / itálico **diferentes dentro de um mesmo bloco de texto corrido são achatados** pro estilo base. `<span style="color:...">` no meio de um `<p>` não aplica.

**Solução: flex-wrap de palavras.** Monte o parágrafo como wrap onde cada palavra (ou segmento) é um `<span>` próprio — vira um text node distinto, e o flex-wrap reflui como texto normal.

```html
<div style="display:flex; flex-wrap:wrap; align-items:baseline;
            column-gap:9px; row-gap:5px;
            font-family:'Poppins'; font-size:32px; line-height:1.42; color:#2B2B2B;">
  <span>Um</span><span>diurético</span>
  <span style="font-weight:700;">natural</span><span>e</span>
  <span style="font-weight:700;">antioxidante</span>
  <span>com</span><span>sabor</span><span>de</span>
  <span style="color:#8B2A52; font-weight:600;">pink</span>
  <span style="color:#8B2A52; font-weight:600;">lemonade</span>
</div>
```

Calibre o `column-gap` (que é a largura do espaço) pelo tamanho da fonte:
- ~30px → `8px` · ~32–34px → `9px` · ~46px (títulos) → `12–14px`
- `row-gap` ~ 4–6px

Para **títulos com 2 estilos** (ex.: "BUBBLY" bold + "bloom?" italic), spans separados como filhos diretos já viram text nodes distintos, sem precisar de flex-wrap.

### 2. Imagens — sempre redimensione antes
- A 1ª imagem da sessão dispara um **popup de permissão** no Paper Desktop — o usuário precisa aceitar. Antes disso, o `<img>` vira frame vazio.
- **Imagens grandes travam o render**. PNG de 2048px / 10MB quebra a sessão (screenshots passam a voltar vazias).
- **Sempre**: `sips -Z 1080 in.png --out out_1080.png` (alvo ~1080px, <2MB).
- Se os screenshots começarem a voltar vazios → **fecha e reabre o Paper Desktop** (o design não se perde).

### 3. Espaçador flex
`flex-grow:1` num `<div>` vazio NÃO expande — vira altura 0. Pra empurrar rodapé pra base:
- ✅ Use espaçador de altura fixa: `<div style="height:120px; flex-shrink:0;"></div>` e ajuste olhando o screenshot.
- Se sobrar muito espaço no final do artboard: troca pra `height:"fit-content"` via `update_styles` (não chuta px novo).

### 4. Screenshots de nós isolados voltam pretos
`get_screenshot` de um nó **sem fundo** retorna **fundo preto** (JPEG sem alpha). Cores escuras (bordô × grafite, por exemplo) ficam idênticas e você julga errado.

✅ **Sempre tire screenshot do artboard inteiro** (que tem o fundo do design) pra avaliar cor/contraste. Use nó isolado só pra checar layout/posição.

### 5. CSS proibido
Paper SÓ aceita: **flex + padding + gap + inline styles**.

**Proibido**: `margin`, `display:grid`, `display:inline`, tabelas HTML.

`position:absolute` ok pra decorativo, mas **nunca cubra o artboard inteiro** com 1 elemento absolute (bloqueia clique).

### 6. `update_styles` NÃO aumenta opacity de volta
Bug confirmado: um bloco com `opacity:0.5` **não volta pra 1** via `update_styles({opacity:1})` — fica travado em 0.5. Diminuir funciona; aumentar não.

✅ **Solução**: recria o bloco no lugar com `write_html(mode:"replace")` no próprio nó. O nó novo nasce com opacity padrão (1) e o `replace` preserva a posição (z-order). Capture o conteúdo exato antes com `get_jsx(nodeId, {format:"inline-styles"})`.

### 7. `set_text_content` apaga spans
Se o bloco foi montado com flex-wrap de palavras (`<span>palavra1</span><span>palavra2</span>`), **não use `set_text_content` pra trocar o texto** — ele achata tudo num text node único, e você perde os destaques. Use `write_html(mode:"replace")` no nó pai e remonte os spans.

### 8. `background-size` não funciona (grade de pontos, padrões repetidos)
`background-image: radial-gradient(...)` + `background-size: 14px 14px` **não repete**: o gradiente estica e vira um véu cinza chapado no artboard inteiro.

✅ **Solução**: padrão em SVG.

```html
<svg width="1080" height="1350" viewBox="0 0 1080 1350" style="position:absolute; left:0px; top:0px;">
  <defs><pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse">
    <circle cx="7" cy="7" r="1.6" fill="#15201C"/></pattern></defs>
  <rect width="1080" height="1350" fill="url(#dots)"/>
</svg>
```

Glow radial **único** (sem repetir) funciona normal: `radial-gradient(closest-side, ...)` + `filter:blur(30px)`.

### 9. `update_styles` de fonte no container NÃO chega no texto
Depois que o texto foi criado, cada `<span>`/text node guarda o próprio `fontSize`/`lineHeight`. Mudar `fontSize` no `<div>` pai não muda nada visualmente.

✅ **Solução**: aplique `update_styles` **nos nós de texto** (ids que o `write_html` devolveu com `component: "Text"`).

### 10. Headline gigante quebra linha no meio da frase
Texto de 130px+ dentro do artboard com padding quebra sozinho ("modelos de / IA"). Se cada linha é um `<span>` próprio, trave com `white-space:nowrap; flex-shrink:0` e ajuste o `font-size` até caber (screenshot confirma).

---

## Fase 6 — Revisão e Export

**Revisão**: pra cada slide, screenshot do artboard e cheque:
- Spacing entre elementos
- Hierarquia tipográfica (o que devia ser maior está maior?)
- **Contraste de cores** (sempre julgue no artboard com fundo, não em nó isolado)
- Alinhamento
- Conteúdo cortado (se sobrar, troca pra `height:"fit-content"`)
- Fidelidade à referência — posições? decorativos?
- Texto igual à copy aprovada na Fase 3 (na voz do criador)?

Corrija **pontualmente** — não recomece o slide.

**Export:**
- `export` com `{nodeId, format:"png", scale:"1x"}` → PNG 1080×1350 (padrão Instagram). `2x` → 2160×2700 se quiser mais nitidez. Sai pra `~/Downloads` com o nome do artboard.
- **Mova** (não copie) cada PNG de `~/Downloads` pra `slides/{slug}-NN.png` da pasta do carrossel (ver "Onde salvar"). Não deixe export solto no Downloads.
- `export_combined_pdf` → todos os slides num PDF só, na ordem dos artboards.
- Exporte em lotes de 8–10 artboards (a tool pode timeoutar com muitos de uma vez).

**Overview de revisão** (opcional, mas útil):
```bash
montage S*.png -tile 5x4 -geometry 360x640+6+6 -background "#111" _overview.jpg
```
(Requer ImageMagick: `brew install imagemagick`.)

---

## Entregáveis ao final

1. Carrossel pronto numa página do Paper (artboards nomeados `01 - …` até `0N - …`).
2. Design system registrado em `design-system-{marca}.md`, na pasta do carrossel.
3. Fotos otimizadas em uma pasta `_assets/`.
4. Exports PNG prontos pra publicar, **já na pasta do carrossel**.
5. (Opcional) PDF combinado pra revisão do cliente.

---

## Onde salvar

Se o usuário tiver uma pasta própria de carrosséis (ou um vault do Obsidian com regra de pasta), use a dele. Senão, crie `carrosseis/{AAAA-MM-DD}-{slug}/` no diretório atual:

```
carrosseis/{AAAA-MM-DD}-{slug}/
├── {slug}.md                              # referência (link), design system, copy aprovada e legenda
├── slides/{slug}-01.png …                 # exports do Paper, renomeados
├── referencia/{slug}-ref-01.jpg + metadata.json
└── _assets/                               # fotos usadas no Paper (opcional)
```

- Nome de arquivo **único** (`{slug}-NN.png`), nunca `slide-01.png` repetido em vários carrosséis.

---

## Setup do Paper (uma vez)

Se o Paper MCP ainda não está conectado:

1. Baixe o Paper Desktop em [paper.design](https://paper.design) e instale.
2. Crie uma conta. O plano grátis tem limite semanal de chamadas do MCP e um carrossel inteiro gasta muitas; pra uso frequente, o Pro.
3. Abra o Paper Desktop e crie/abra um arquivo qualquer.
4. Confirme que o servidor MCP local está rodando: `lsof -i :29979`.
5. Registre o MCP no Claude Code: `claude mcp add paper --transport http http://127.0.0.1:29979/mcp --scope user`.
6. **Reinicie a sessão do Claude Code** pra os tools `mcp__paper__*` aparecerem.

Validação:
```
get_guide({topic:"paper-mcp-instructions"})
get_basic_info()
```
Se ambos respondem ok, tá pronto.

---

## Tools mais usados (referência rápida)

| Tool | Pra que serve |
|---|---|
| `get_guide` | **1º da sessão**, topic `paper-mcp-instructions` |
| `get_basic_info` | arquivo, página, fontes, artboards |
| `get_font_family_info` | confirmar fontes antes de estilizar |
| `create_page` / `open_page` | página nova pra não sujar a existente |
| `create_artboard` | um por slide (1080×1350) |
| `write_html` | escrever conteúdo (1 grupo por chamada) |
| `update_styles` | ajustes de estilo (batch) |
| `set_text_content` | trocar texto sem reescrever HTML — **não preserva spans** |
| `duplicate_nodes` | clonar rodapé/slides; aceita `parentId`; devolve `descendantIdMap` |
| `move_nodes` | reordenar/reparentar sem perder IDs |
| `rename_nodes` | renomear camadas (ex.: nome do artboard) |
| `get_screenshot` | revisar (no artboard inteiro!) |
| `get_jsx` / `get_computed_styles` | exportar pra código (valores exatos) |
| `export` / `export_combined_pdf` | exportar PNG / PDF |
| `finish_working_on_nodes` | **obrigatório** ao terminar |

---

## Material complementar

Na pasta `materiais/` desta skill você encontra:

- `download-apify.py` — script Python pra baixar carrossel do Instagram via Apify.
- `template-design-system.md` — modelo pra preencher ao extrair o design da referência.
- `exemplo-anatomia.md` — exemplo real de anatomia slide a slide (caso "Bubbly Bloom").
- `receitas-paper.md` — snippets prontos (artboard, flex-wrap, flores SVG, vinheta, bolhas, etc.).
