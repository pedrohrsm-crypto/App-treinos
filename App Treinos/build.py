#!/usr/bin/env python3
"""
Script de Build — App Treinos
==============================

Gera executável standalone usando PyInstaller.
Uso:  python build.py          (build normal)
      python build.py --onefile (executável único)
      python build.py --clean   (limpa build anterior)
"""

import subprocess
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SPEC_FILE = ROOT / "AppTreinos.spec"
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"


def clean():
    """Remove artefatos de build anteriores."""
    for d in [DIST_DIR, BUILD_DIR]:
        if d.exists():
            shutil.rmtree(d)
            print(f"  Removido: {d}")


def build(onefile: bool = False):
    """Executa PyInstaller."""
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    if onefile:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--noconsole",
            "--name", "AppTreinos",
            "--add-data", f"{ROOT / 'data'}{os.pathsep}data",
            "--add-data", f"{ROOT / 'version.py'}{os.pathsep}.",
            "--add-data", f"{ROOT / 'i18n.py'}{os.pathsep}.",
            str(ROOT / "App_Treinos_GUI.py"),
        ]
    else:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            str(SPEC_FILE),
        ]

    print(f"\n  Executando: {' '.join(cmd)}\n")
    subprocess.check_call(cmd, cwd=str(ROOT))

    exe_name = "AppTreinos.exe" if sys.platform == "win32" else "AppTreinos"
    if onefile:
        exe_path = DIST_DIR / exe_name
    else:
        exe_path = DIST_DIR / "AppTreinos" / exe_name

    if exe_path.exists():
        print(f"\n  ✅ Build concluído: {exe_path}")
        print(f"  Tamanho: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    else:
        print("\n  ⚠️  Build concluído mas executável não encontrado.")


if __name__ == "__main__":
    import os

    args = set(sys.argv[1:])

    if "--clean" in args:
        print("🧹 Limpando artefatos...")
        clean()
        if args == {"--clean"}:
            sys.exit(0)

    print("🔨 Gerando executável App Treinos...")
    build(onefile="--onefile" in args)
