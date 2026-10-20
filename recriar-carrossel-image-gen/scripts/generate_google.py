#!/usr/bin/env python3
"""
generate_google.py — gera 1 imagem SEM ROSTO via Google AI Studio (Gemini direto).

Padrão pra slide de carrossel e thumbnail que não têm o rosto do criador.
Imagem com rosto do criador continua em generate_openrouter.py com
openai/gpt-5.4-image-2 (regra do perfil.md).

Endpoint: generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
com responseModalities IMAGE + imageConfig (aspectRatio, imageSize).

Modelos (passe via --model ou env GOOGLE_IMAGE_MODEL):
  gemini-3-pro-image         (Nano Banana Pro — melhor tipografia/composição, default)
  gemini-3.1-flash-image     (Nano Banana 2 — rascunho rápido de layout)

Requer:
  - GOOGLE_AI_STUDIO_API_KEY no ambiente (ou .env central)
  - pip install httpx python-dotenv

Uso:
  python3 generate_google.py \
      --prompt-file prompts/slide-02.txt \
      --ref referencia/slide_02.jpg \
      --out output/slide-02.png \
      --aspect-ratio 4:5 --image-size 2K

  # thumbnail sem rosto:
  python3 generate_google.py --prompt-file thumb.txt --out thumb.png --aspect-ratio 16:9
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
    load_dotenv(Path.home() / ".claude" / "skills" / "recriar-carrossel" / ".env")
    load_dotenv(Path.home() / ".config" / "vortex-marketing" / ".env")
    load_dotenv()
except ImportError:
    pass


GOOGLE_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODEL = os.getenv("GOOGLE_IMAGE_MODEL", "gemini-3-pro-image")
# Fotos do criador ficam aqui: passar como referência = imagem com rosto = GPT Image 2.
FOTOS_DO_CRIADOR = [
    str(Path.home() / ".claude" / "skills" / "recriar-carrossel" / "perfil"),
    str(Path.home() / ".config" / "vortex-marketing" / "perfil" / "assets"),
]


def encode_image(path: str) -> tuple[str, str]:
    ext = Path(path).suffix.lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".webp": "image/webp"}.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        return mime, base64.standard_b64encode(f.read()).decode("utf-8")


def generate(prompt: str, ref_paths: list[str], model: str, out_path: str,
             aspect_ratio: str = "4:5", image_size: str = "2K",
             retries: int = 3, sleep_s: int = 20) -> str:
    api_key = os.getenv("GOOGLE_AI_STUDIO_API_KEY", "")
    if not api_key:
        print("ERROR: GOOGLE_AI_STUDIO_API_KEY não configurada (env ou .env)", file=sys.stderr)
        sys.exit(1)

    parts = [{"text": prompt}]
    for path in ref_paths:
        mime, b64 = encode_image(path)
        parts.append({"inlineData": {"mimeType": mime, "data": b64}})

    image_config = {"aspectRatio": aspect_ratio}
    if image_size:
        image_config["imageSize"] = image_size
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": image_config,
        },
    }

    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with httpx.Client(timeout=300) as client:
                resp = client.post(f"{GOOGLE_BASE_URL}/{model}:generateContent",
                                   headers={"x-goog-api-key": api_key}, json=payload)
            if resp.status_code != 200:
                last_err = f"HTTP {resp.status_code}: {resp.text[:300]}"
                print(f"  ⚠️  tentativa {attempt}/{retries} falhou: {last_err}", file=sys.stderr)
                if attempt < retries:
                    time.sleep(sleep_s)
                continue

            data = resp.json()
            candidates = data.get("candidates") or [{}]
            for part in (candidates[0].get("content") or {}).get("parts") or []:
                inline = part.get("inlineData")
                if inline and inline.get("data"):
                    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
                    Path(out_path).write_bytes(base64.b64decode(inline["data"]))
                    return out_path

            reason = candidates[0].get("finishReason") or data.get("promptFeedback")
            last_err = f"resposta sem imagem (finishReason: {reason})"
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
    ap = argparse.ArgumentParser(description="Gera imagem sem rosto via Google AI Studio.")
    ap.add_argument("--prompt", help="Prompt inline.")
    ap.add_argument("--prompt-file", help="Arquivo com o prompt.")
    ap.add_argument("--ref", action="append", default=[],
                    help="Imagem de referência (pode repetir: slide original, style ref).")
    ap.add_argument("--out", required=True, help="Caminho do PNG de saída.")
    ap.add_argument("--aspect-ratio", default="4:5",
                    help="4:5 (carrossel, default), 16:9 (thumb), 1:1, 9:16.")
    ap.add_argument("--image-size", default="2K",
                    help="1K, 2K (default) ou 4K. Resolução nativa maior = texto mais nítido.")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"Modelo Gemini (default: {DEFAULT_MODEL}).")
    args = ap.parse_args()

    face_refs = [r for r in args.ref
                 if any(p in str(Path(r).expanduser().resolve()) for p in FOTOS_DO_CRIADOR)]
    if face_refs:
        print("ERROR: referência do perfil do criador (rosto/avatar) detectada: "
              f"{face_refs}. Imagem com rosto usa generate_openrouter.py "
              "--model openai/gpt-5.4-image-2.", file=sys.stderr)
        sys.exit(2)

    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    elif args.prompt:
        prompt = args.prompt
    else:
        print("ERROR: passe --prompt ou --prompt-file", file=sys.stderr)
        sys.exit(1)

    out = generate(prompt, args.ref, args.model, args.out,
                   aspect_ratio=args.aspect_ratio, image_size=args.image_size)
    print(f"✅ {out}  (modelo: {args.model}, {args.aspect_ratio}, {args.image_size})")


if __name__ == "__main__":
    main()
