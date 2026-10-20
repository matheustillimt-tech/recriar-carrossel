# Recriar Carrossel

Duas skills do Claude Code que recriam um carrossel do Instagram que já viralizou, mantendo o design e trocando só o conteúdo pelo seu.

Você manda o link do post (ou os prints) e o seu tema. O Claude lê cada slide, extrai cores, fontes e layout, reescreve o texto no seu tom, mostra pra você aprovar e só então monta os slides.

| Skill | Como monta | Quando usar |
|---|---|---|
| `recriar-carrossel` | No **Paper** (app de design), slide a slide, com texto editável | Quando você quer acertar cada detalhe e editar depois |
| `recriar-carrossel-image-gen` | **Só com IA de imagem**: cada slide sai pronto como PNG | Quando você quer rápido, sem abrir app de design |

As duas usam a mesma pasta de configuração, então dá pra instalar e usar as duas.

## Instalar

Precisa do [Claude Code](https://claude.com/claude-code) instalado.

**Jeito mais fácil:** abre o Claude Code e cola: `Instala as skills do repositório https://github.com/matheustillimt-tech/recriar-carrossel na minha pasta de skills (~/.claude/skills)`. Ele faz o resto.

Prefere fazer na mão?

**Mac ou Linux**, no Terminal:

```bash
D=$(mktemp -d) && git clone -q https://github.com/matheustillimt-tech/recriar-carrossel "$D"
mkdir -p ~/.claude/skills && cp -R "$D"/recriar-carrossel "$D"/recriar-carrossel-image-gen ~/.claude/skills/
pip3 install httpx python-dotenv pillow
```

**Windows**, no PowerShell:

```powershell
git clone https://github.com/matheustillimt-tech/recriar-carrossel "$env:TEMP\recriar-carrossel"
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force "$env:TEMP\recriar-carrossel\recriar-carrossel", "$env:TEMP\recriar-carrossel\recriar-carrossel-image-gen" "$HOME\.claude\skills\"
pip install httpx python-dotenv pillow
```

Sem `git`? Clica em **Code → Download ZIP** aqui em cima, descompacta e copia as duas pastas pra `~/.claude/skills/`.

Depois, fecha e abre o Claude Code de novo pra ele carregar as skills.

## Usar

No Claude Code:

```
/recriar-carrossel recria esse carrossel com o meu conteúdo: https://www.instagram.com/p/XXXXX/
Tema: [o que o seu carrossel vai falar]
```

Ou, no modo só com imagem:

```
/recriar-carrossel-image-gen recria esse carrossel só com IA: [link ou prints]
Tema: [o que o seu carrossel vai falar]
```

Na primeira vez, o Claude pergunta o que faltar (seu @, sua foto de perfil, as chaves) e guarda pra não perguntar de novo.

Mais modelos de pedido em `PROMPT-CLAUDE-CODE.md`, dentro de cada pasta.

## O que você precisa

| | Pra quê | Custo |
|---|---|---|
| [Paper Desktop](https://paper.design) | Montar os slides (só na `recriar-carrossel`) | Tem plano grátis com limite semanal; pra uso frequente, o Pro |
| [Apify](https://apify.com) | Baixar o carrossel pelo link do Instagram | Opcional (dá pra mandar os prints). O plano grátis serve pra começar |
| [Google AI Studio](https://aistudio.google.com/apikey) | Gerar slide sem rosto (modo só com imagem) | Tem cota grátis |
| [OpenRouter](https://openrouter.ai/keys) | Gerar foto ou slide com o seu rosto | Pago por uso, o script mostra o custo de cada imagem |

As chaves ficam em `~/.claude/skills/recriar-carrossel/.env` (modelo em `.env.example`). Nunca suba esse arquivo pra lugar nenhum.

## Licença

MIT. Feito pelo Grupo Vórtex.
