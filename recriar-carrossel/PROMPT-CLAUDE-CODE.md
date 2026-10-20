# Prompt — Recriar carrossel a partir de referência

Cole esse prompt no Claude Code (com a imagem de referência anexada ou a URL do post do Instagram) e o agente vai recriar o carrossel pra você.

---

## Versão 1 — Tenho a URL do post

```
Recria esse carrossel idêntico pra mim, mas trocando o conteúdo:

URL da referência: https://instagram.com/p/COLE_AQUI/

Novo tema/conteúdo:
[DESCREVE AQUI o que você quer que o carrossel fale — produto, oferta, lista de N coisas, etc.]

Usa a skill `recriar-carrossel` do Claude Code.
```

---

## Versão 2 — Tenho prints/arquivos da referência

```
Recria esse carrossel idêntico ao das imagens anexas, mas trocando o conteúdo por:

[DESCREVE AQUI o tema novo. Quanto mais específico, melhor: títulos exatos, tom de voz, CTA, etc.]

Usa a skill `recriar-carrossel` do Claude Code.
```

(E anexa as imagens dos slides na mensagem.)

---

## Versão 3 — Quero trocar a foto da capa também

```
Recria esse carrossel idêntico ao da imagem anexa, trocando:

1) O conteúdo (tema novo): [DESCREVE AQUI]
2) A foto da capa: usa essa foto que tô anexando / gera uma foto nova com IA mostrando [DESCRIÇÃO]

Mantém o mesmo design (paleta, fontes, decorativos, layout).

Usa a skill `recriar-carrossel` do Claude Code.
```

---

## Dicas pra um resultado melhor

- **Se tiver URL do Instagram, manda a URL** — o agente baixa sozinho via Apify (precisa do `APIFY_TOKEN` configurado).
- **Quanto mais específico o tema, melhor.** Em vez de "carrossel sobre produtividade", manda "carrossel listando 7 apps de IA pra freelancers, com nome do app + 1 frase do que faz + preço".
- **Diz o tom de voz** se for diferente do original ("mais técnico", "mais informal", "premium")
- **Se quiser usar tua identidade visual** (não a da referência), avisa: "mantém a estrutura/anatomia mas usa minha paleta: fundo `#XXXXXX`, destaque `#XXXXXX`, fonte `Inter`".

---

## Pré-requisitos

- Paper Desktop aberto + Paper MCP conectado (ver `SKILL.md` seção "Setup do Paper").
- Paper Pro recomendado pra uso frequente (o grátis tem limite semanal de chamadas).
- Pra baixar carrossel via URL: token do Apify (o Claude pede na primeira vez e grava no `.env` da skill).

Se algo falhar, o agente vai te avisar o que está faltando.
