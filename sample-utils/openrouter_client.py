#!/usr/bin/env python3
"""
openrouter_client.py — small client for image generation via the OpenRouter API.

Model: google/gemini-3.1-flash-image-preview.

The exact shape of the image response can vary between providers/models; this code
tries to extract the image from the most common response shapes (base64-encoded in
the message, or a URL). Adjust `_extract_image()` if a given model's response format
differs — check OpenRouter's docs for that specific model.

Generated images should be reviewed before being used in production.

Usage:
    python openrouter_client.py "image prompt" output/path/image.png

As a library:
    from openrouter_client import generar_imagen
    path = generar_imagen("a photorealistic warehouse worker wearing a harness",
                           "output/path/image.png")
"""
from __future__ import annotations

import base64
import sys
from pathlib import Path

import requests  # type: ignore

from _common import env, load_env

MODEL = "google/gemini-3.1-flash-image-preview"
URL = "https://openrouter.ai/api/v1/chat/completions"


def _extract_image(data: dict) -> bytes | None:
    """Intenta sacar los bytes de la imagen de la respuesta de OpenRouter."""
    try:
        msg = data["choices"][0]["message"]
    except Exception:
        return None
    # (a) formato 'images' con data URL base64
    for img in msg.get("images", []) or []:
        u = (img.get("image_url") or {}).get("url", "") if isinstance(img, dict) else ""
        if u.startswith("data:") and "base64," in u:
            return base64.b64decode(u.split("base64,", 1)[1])
        if u.startswith("http"):
            return requests.get(u, timeout=120).content
    # (b) content como lista con partes de imagen
    content = msg.get("content")
    if isinstance(content, list):
        for part in content:
            u = (part.get("image_url") or {}).get("url", "") if isinstance(part, dict) else ""
            if u.startswith("data:") and "base64," in u:
                return base64.b64decode(u.split("base64,", 1)[1])
            if u.startswith("http"):
                return requests.get(u, timeout=120).content
    return None


def generar_imagen(prompt: str, dest: str | Path) -> Path:
    load_env()
    api_key = env("OPENROUTER_API_KEY", required=True)
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        # Algunos modelos requieren pedir explícitamente modalidad imagen:
        "modalities": ["image", "text"],
    }
    r = requests.post(URL, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # OpenRouter recomienda estos headers de atribución (opcionales):
        "HTTP-Referer": "https://previx.local",
        "X-Title": "Previx Videos",
    }, json=payload, timeout=180)
    r.raise_for_status()
    img_bytes = _extract_image(r.json())
    if not img_bytes:
        raise SystemExit("[ERROR] No se pudo extraer imagen de la respuesta. "
                         "Revisa el formato con la doc de OpenRouter y ajusta "
                         "_extract_image().")
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(img_bytes)
    print(f"[ok] image generated -> {dest}")
    return dest


def _cli() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        return
    generar_imagen(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    _cli()
