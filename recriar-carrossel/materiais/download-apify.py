"""
Template — Download de carrossel/post do Instagram via Apify.

Como usar:
1. Crie conta em https://apify.com e pegue seu token em Settings → Integrations.
2. Grave no .env da skill: ~/.claude/skills/recriar-carrossel/.env
   APIFY_TOKEN=<SEU_TOKEN_AQUI>
3. Troque POST_URL pela URL do post que você quer baixar.
4. Ajuste OUT_DIR pra onde quer salvar os slides.
5. Rode: python download-apify.py
   (ou passe por argumento: python download-apify.py <POST_URL> [OUT_DIR])

Saída:
- slide_01.jpg, slide_02.jpg, ... slide_NN.jpg na pasta OUT_DIR
- metadata.json com info do post (autor, caption, tipo, etc.)

Dependências:
    pip install httpx python-dotenv
"""

import httpx
import os
import sys
import json
from pathlib import Path

# Carrega o .env da skill e depois o .env da pasta atual
try:
    from dotenv import load_dotenv
    load_dotenv(Path.home() / ".claude" / "skills" / "recriar-carrossel" / ".env")
    load_dotenv(Path.home() / ".config" / "vortex-marketing" / ".env")
    load_dotenv()
except ImportError:
    pass

# ====== CONFIGURE AQUI ======
POST_URL = "https://www.instagram.com/p/COLE_O_CODIGO_DO_POST_AQUI/"
OUT_DIR = "./referencia-1"  # pasta onde salvar os slides
APIFY_TOKEN = os.getenv("APIFY_TOKEN", "<SEU_APIFY_TOKEN_AQUI>")
# ============================

if len(sys.argv) > 1:
    POST_URL = sys.argv[1]
if len(sys.argv) > 2:
    OUT_DIR = sys.argv[2]

POST_ID = POST_URL.split("?")[0].rstrip("/").split("/")[-1]
OUT = Path(OUT_DIR)
OUT.mkdir(parents=True, exist_ok=True)

if APIFY_TOKEN == "<SEU_APIFY_TOKEN_AQUI>":
    raise SystemExit(
        "ERRO: configure APIFY_TOKEN como variavel de ambiente "
        "ou direto no script."
    )

# Dispara o scraper e espera o resultado
with httpx.Client(timeout=180) as c:
    resp = c.post(
        "https://api.apify.com/v2/acts/apify~instagram-scraper/runs?waitForFinish=120",
        headers={"Authorization": f"Bearer {APIFY_TOKEN}"},
        json={"directUrls": [POST_URL], "resultsLimit": 1},
    )
    # Apify retorna 201 em sucesso (nao 200) — trate ambos
    if resp.status_code not in (200, 201):
        raise SystemExit(f"Apify erro {resp.status_code}: {resp.text[:300]}")

    dataset_id = resp.json()["data"]["defaultDatasetId"]
    # O dataset também exige o token (sem ele a API responde "insufficient-permissions")
    items = c.get(
        f"https://api.apify.com/v2/datasets/{dataset_id}/items",
        headers={"Authorization": f"Bearer {APIFY_TOKEN}"},
    ).json()

if not isinstance(items, list):
    raise SystemExit(f"Apify erro ao ler dataset: {str(items)[:300]}")

if not items:
    raise SystemExit("Apify nao retornou nenhum item. Verifique a URL.")

post = items[0]
print(f"Autor: @{post.get('ownerUsername')}, tipo: {post.get('type')}")

# Carrossel = type "Sidecar" com childPosts; foto/video unico = displayUrl raiz
if post.get("type") == "Sidecar" and post.get("childPosts"):
    urls = [ch.get("displayUrl") for ch in post["childPosts"] if ch.get("displayUrl")]
else:
    urls = [post.get("displayUrl")] if post.get("displayUrl") else []

if not urls:
    raise SystemExit("Nenhum displayUrl encontrado no post.")

# Baixa cada slide
with httpx.Client(timeout=120) as c:
    for i, url in enumerate(urls, 1):
        r = c.get(url)
        (OUT / f"slide_{i:02d}.jpg").write_bytes(r.content)
        print(f"slide_{i:02d}.jpg salvo")

# Salva metadados (caption original eh util pra revisao/atribuicao)
(OUT / "metadata.json").write_text(
    json.dumps(
        {
            "post_id": POST_ID,
            "url": POST_URL,
            "owner": post.get("ownerUsername"),
            "type": post.get("type"),
            "caption": post.get("caption"),
            "slide_count": len(urls),
        },
        ensure_ascii=False,
        indent=2,
    )
)
print(f"OK — {len(urls)} slides salvos em {OUT}")
