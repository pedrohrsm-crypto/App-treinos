#!/usr/bin/env python3
"""
Script de Build — App Treinos v3.0
====================================

Gera executável standalone usando ``flet pack`` (wrapper PyInstaller optimizado
para apps Flet).

Uso:
    python build.py              # build padrão (one-folder)
    python build.py --onefile    # executável único
    python build.py --clean      # limpa artefatos anteriores

Requisitos:
    pip install flet pyinstaller
"""

import os
import subprocess
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
ICON = ROOT / "assets" / "icon.ico"
ENTRY = ROOT / "App_Treinos_Flet.py"

PRODUCT_NAME = "App Treinos"
PRODUCT_VERSION = "3.0.0"
COMPANY_NAME = "App Treinos"
FILE_DESCRIPTION = "Planejador inteligente de treinos esportivos"
COPYRIGHT = f"© 2026 {COMPANY_NAME}"


def clean():
    """Remove artefatos de build anteriores."""
    for d in [DIST_DIR, BUILD_DIR]:
        if d.exists():
            shutil.rmtree(d)
            print(f"  Removido: {d}")
    print("  ✅ Limpeza concluída.")


def build(onefile: bool = False):
    """Gera executável via ``flet pack``."""
    # Garantir que flet-cli está disponível
    if shutil.which("flet") is None:
        print("flet CLI não encontrado. Instalando flet...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flet"])

    cmd = [
        "flet", "pack",
        str(ENTRY),
        "-n", "AppTreinos",
        "--product-name", PRODUCT_NAME,
        "--product-version", PRODUCT_VERSION,
        "--file-version", PRODUCT_VERSION,
        "--company-name", COMPANY_NAME,
        "--file-description", FILE_DESCRIPTION,
        "--copyright", COPYRIGHT,
        "--add-data", f"{ROOT / 'data'}{os.pathsep}data",
        "--add-data", f"{ROOT / 'version.py'}{os.pathsep}.",
        "--add-data", f"{ROOT / 'i18n.py'}{os.pathsep}.",
        "--add-data", f"{ROOT / 'flet_app'}{os.pathsep}flet_app",
        "--add-data", f"{ROOT / 'core'}{os.pathsep}core",
        "--add-data", f"{ROOT / 'assets'}{os.pathsep}assets",
    ]

    if ICON.exists():
        cmd += ["-i", str(ICON)]

    if not onefile:
        cmd += ["-D"]  # one-folder mode

    cmd += ["-y"]  # confirm overwrite

    print(f"\n  Executando:\n    {' '.join(cmd)}\n")
    subprocess.check_call(cmd, cwd=str(ROOT))

    exe_name = "AppTreinos.exe" if sys.platform == "win32" else "AppTreinos"
    if onefile:
        exe_path = DIST_DIR / exe_name
    else:
        exe_path = DIST_DIR / "AppTreinos" / exe_name

    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n  ✅ Build concluído: {exe_path}")
        print(f"  Tamanho: {size_mb:.1f} MB")
    else:
        # Flet pack pode colocar em local diferente
        candidates = list(DIST_DIR.rglob(exe_name))
        if candidates:
            exe_path = candidates[0]
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n  ✅ Build concluído: {exe_path}")
            print(f"  Tamanho: {size_mb:.1f} MB")
        else:
            print("\n  ⚠️  Build concluído mas executável não encontrado em dist/.")
            print("  Verifique a saída acima para localizar o artefato.")


if __name__ == "__main__":
    args = set(sys.argv[1:])

    if "--help" in args or "-h" in args:
        print(__doc__)
        sys.exit(0)

    if "--clean" in args:
        print("🧹 Limpando artefatos...")
        clean()
        if args == {"--clean"}:
            sys.exit(0)

    print(f"🔨 Gerando executável {PRODUCT_NAME} v{PRODUCT_VERSION}...")
    build(onefile="--onefile" in args)
