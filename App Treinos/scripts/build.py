#!/usr/bin/env python3
"""
Build Script — Gera executável Windows com PyInstaller.

Uso:
    python scripts/build.py

Resultado:
    dist/App_Treinos.exe (executável standalone)
"""

import sys
import subprocess
from pathlib import Path


def build_executable():
    """Gera executável Windows com PyInstaller."""

    project_root = Path(__file__).parent.parent

    # Validar PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("[ERROR] PyInstaller não instalado")
        print("  Execute: pip install pyinstaller")
        return 1

    print("[BUILD] Compilando App Treinos v3.2.0...")
    print()

    # Opções do PyInstaller
    pyinstaller_args = [
        "PyInstaller",
        "--onefile",                          # Gerar um único executável
        "--windowed",                         # Sem janela de console
        "--name=AppTreinos",                  # Nome do executável
        "--add-data=data:data",
        "--hidden-import=flet",
        "--hidden-import=pandas",
        "--hidden-import=reportlab",
        "--hidden-import=openpyxl",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=.",
        str(project_root / "app_treinos" / "__main__.py"),
    ]

    try:
        result = subprocess.run(pyinstaller_args, cwd=project_root)

        if result.returncode == 0:
            exe_path = project_root / "dist" / "AppTreinos.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print()
                print("[OK] Executável gerado com sucesso!")
                print(f"  Localização: {exe_path}")
                print(f"  Tamanho: {size_mb:.1f} MB")
                print()
                return 0

        print("[ERROR] Falha ao compilar", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"[ERROR] Erro: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(build_executable())
