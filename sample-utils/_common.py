"""
_common.py — utilidades compartidas por los scripts de Previx Videos.

No es un script ejecutable: lo importan los demás (generar-manifiesto,
indexar-banco-empresa, previsualizacion, *_client, etc.).

Decisión de lenguaje: TODO el tooling del proyecto está en Python 3 por su buen
soporte de HTTP (requests), manejo de imágenes (Pillow) y wrapping de ffmpeg.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

# Raíz del proyecto = carpeta padre de scripts/
ROOT = Path(__file__).resolve().parent.parent


def load_env() -> None:
    """Carga .env (si existe y python-dotenv está instalado). Silencioso si no."""
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(ROOT / ".env")
    except Exception:
        # Sin dotenv, se usan las variables de entorno que ya haya en el sistema.
        pass


def env(name: str, required: bool = False, default: str | None = None) -> str | None:
    """Lee una variable de entorno. Si required y falta, lanza un error claro."""
    val = os.environ.get(name, default)
    if required and not val:
        raise SystemExit(
            f"[ERROR] Falta la variable de entorno '{name}'. "
            f"Añádela a tu .env (copia .env.example)."
        )
    return val


def read_json(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[ok] escrito {path}")
