#!/usr/bin/env python3
"""
generate_openrouter.py — gera 1 slide de carrossel via OpenRouter.

É o método que a gente usa em produção nos carrosséis do Grupo Vórtex.

OpenRouter expõe os modelos de imagem pelo endpoint de chat
(/api/v1/chat/completions) com "modalities": ["image", "text"].
Você passa o prompt + imagens de referência (base64) e recebe a
imagem gerada em choices[0].message.images[].image_url.url.

Modelos (passe via --model ou env OPENROUTER_IMAGE_MODEL):
  openai/gpt-5.4-image-2                   (GPT Image 2 — default; imagem com rosto do criador)
  Imagem SEM rosto: use generate_google.py (Gemini 3 Pro Image direto no Google AI Studio).

Requer:
  - OPENROUTER_API_KEY no ambiente (ou .env)
  - pip install httpx python-dotenv

Uso:
  python3 generate_openrouter.py \
      --prompt-file prompts/slide-01.txt \
      --ref referencia/slide-01.jpg \
      --ref fotos/criador.jpg \
      --out output/slide-01.png \
      --model openai/gpt-5.4-image-2 \
      --aspect-ratio 4:5

  # thumbnail YouTube com rosto do criador (sempre modelo GPT):
  python3 generate_openrouter.py --prompt-file thumb.txt \
      --ref rosto-03.jpg --ref rosto-05.jpg \
      --out thumb.png --model openai/gpt-5.4-image-2 --aspect-ratio 16:9

  # prompt inline em vez de arquivo:
  python3 generate_openrouter.py --prompt "Instagram carousel slide..." --out out.png
"""

import argparse
import base64
import os
import sys
import time
from pathlib import Path

try:
    import httpx
except ImportError:
    print("ERROR: pip install httpx", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
    # .env da skill primeiro, depois o .env da pasta atual
    load_dotenv(Path.home() / ".claude" / "skills" / "recriar-carrossel" / ".env")
    load_dotenv(Path.home() / ".config" / "vortex-marketing" / ".env")
    load_dotenv()
except ImportError:
    pass  # dotenv é opcional


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = os.getenv(
    "OPENROUTER_IMAGE_MODEL", "openai/gpt-5.4-image-2"
)


def encode_image(path: str) -> tuple[str, str]:
    """Retorna (mime_type, base64_string) de uma imagem."""
    p = Path(path)
    ext = p.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode("utf-8")
    return mime, b64


def generate(prompt: str, ref_paths: list[str], model: str, out_path: str,
             aspect_ratio: str = "4:5", retries: int = 3, sleep_s: int = 20) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY não configurada (env ou .env)", file=sys.stderr)
        sys.exit(1)

    content_parts = [{"type": "text", "text": prompt}]
    for path in ref_paths:
        mime, b64 = encode_image(path)
        content_parts.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{b64}"},
        })

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content_parts}],
        "modalities": ["image", "text"],
        # teto de tokens: sem isso o OpenRouter reserva 65536 e recusa (402) quando o saldo está baixo
        "max_tokens": int(os.getenv("OPENROUTER_MAX_TOKENS", "12000")),
        # Sem isso o modelo devolve quadrado (1024×1024) e o resize distorce o slide.
        # GPT Image 2 em 4:5 devolve 896×1120; em 16:9, 1280×720.
        "image_config": {"aspect_ratio": aspect_ratio},
        "usage": {"include": True},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://conteudos.grupovortex.online",
        "X-Title": "Vibe Marketing - Carrossel Image Gen",
    }

    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with httpx.Client(timeout=300) as client:
                resp = client.post(
                    f"{OPENROUTER_BASE_URL}/chat/completions",
                    headers=headers,
                    json=payload,
                )
            if resp.status_code != 200:
                last_err = f"HTTP {resp.status_code}: {resp.text[:200]}"
                print(f"  ⚠️  tentativa {attempt}/{retries} falhou: {last_err}", file=sys.stderr)
                if attempt < retries:
                    time.sleep(sleep_s)
                continue

            data = resp.json()
            cost = (data.get("usage") or {}).get("cost")
            if cost is not None:
                print(f"  💰 custo: US$ {cost:.4f}", file=sys.stderr)
            message = data.get("choices", [{}])[0].get("message", {}) or {}
            images = message.get("images") or []
            for img in images:
                url = img.get("image_url", {}).get("url", "")
                if url.startswith("data:") and ";base64," in url:
                    raw = base64.b64decode(url.split(";base64,", 1)[1])
                    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(out_path, "wb") as f:
                        f.write(raw)
                    return out_path

            last_err = "resposta sem imagem (choices[0].message.images vazio)"
            print(f"  ⚠️  {last_err}", file=sys.stderr)
            if attempt < retries:
                time.sleep(sleep_s)
        except Exception as e:
            last_err = str(e)
            print(f"  ⚠️  tentativa {attempt}/{retries} erro: {last_err}", file=sys.stderr)
            if attempt < retries:
                time.sleep(sleep_s)

    print(f"ERROR: falhou após {retries} tentativas. Último erro: {last_err}", file=sys.stderr)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Gera slide de carrossel via OpenRouter.")
    ap.add_argument("--prompt", help="Prompt inline.")
    ap.add_argument("--prompt-file", help="Arquivo com o prompt.")
    ap.add_argument("--ref", action="append", default=[],
                    help="Imagem de referência (pode repetir: original, foto criador, style ref).")
    ap.add_argument("--out", required=True, help="Caminho do PNG de saída.")
    ap.add_argument("--aspect-ratio", default=os.getenv("OPENROUTER_ASPECT_RATIO", "4:5"),
                    help="Proporção da imagem: 4:5 (carrossel, default), 16:9 (thumb), 1:1, 9:16.")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"Slug do modelo OpenRouter (default: {DEFAULT_MODEL}).")
    args = ap.parse_args()

    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    elif args.prompt:
        prompt = args.prompt
    else:
        print("ERROR: passe --prompt ou --prompt-file", file=sys.stderr)
        sys.exit(1)

    out = generate(prompt, args.ref, args.model, args.out, aspect_ratio=args.aspect_ratio)
    print(f"✅ {out}  (modelo: {args.model})")


if __name__ == "__main__":
    main()
