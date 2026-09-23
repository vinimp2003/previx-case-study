"""
_common.py — small shared helpers (env loading, JSON I/O) used across the project's
Python scripts. Not meant to be run directly.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_env() -> None:
    """Loads a .env file if present and python-dotenv is installed; silent otherwise."""
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(ROOT / ".env")
    except Exception:
        # Without dotenv, fall back to whatever environment variables are already set.
        pass


def env(name: str, required: bool = False, default: str | None = None) -> str | None:
    """Reads an environment variable, raising a clear error if required and missing."""
    val = os.environ.get(name, default)
    if required and not val:
        raise SystemExit(
            f"[ERROR] Missing environment variable '{name}'. "
            f"Add it to your .env (copy .env.example)."
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
    print(f"[ok] wrote {path}")
