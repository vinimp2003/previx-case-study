#!/usr/bin/env python3
"""
openrouter_client.py — helper para generar imágenes con IA vía OpenRouter (PRIORIDAD 3).

Modelo: google/gemini-3.1-flash-image-preview  (Nano Banana 2).

Esqueleto FUNCIONAL. El formato EXACTO de la respuesta de imagen puede variar; el
código intenta extraer la imagen de las formas más comunes (base64 en el mensaje o
URL). Ajusta `_extract_image()` si la respuesta real difiere; consulta la doc de
OpenRouter para el modelo concreto.

🔴 Recuerda: la generación con IA es el ÚLTIMO RECURSO. Toda imagen generada DEBE
verificarse con visión antes de aceptarse (lo hace el agente curador-visual). Este
script solo genera; la verificación/bucle la conduce Claude.

Uso:
    python scripts/openrouter_client.py "prompt de la imagen" videos/<slug>/assets/s7_imagen.png

Como librería:
    from openrouter_client import generar_imagen
    ruta = generar_imagen("operario con arnés en cubierta industrial, foto realista",
                          "videos/<slug>/assets/s7_imagen.png")
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
    print(f"[ok] imagen generada -> {dest}")
    print("     👁  Verifícala con visión antes de aceptarla (curador-visual).")
    return dest


def _cli() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        return
    generar_imagen(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    _cli()
