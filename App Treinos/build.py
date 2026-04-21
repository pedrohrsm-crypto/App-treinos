#!/usr/bin/env python3
"""
Script de Build — App Treinos v3.1
====================================

Gera executável standalone usando ``flet pack`` (wrapper PyInstaller optimizado
para apps Flet).

Uso:
    python build.py --setup        # instala todas as dependências de build
    python build.py              # build padrão (one-folder)
    python build.py --onefile    # executável único
    python build.py --clean      # limpa artefatos anteriores
    python build.py --installer  # gera instalador Windows (requer Inno Setup 6+)

Fluxo completo (primeiro deploy):
    python build.py --setup --clean --onefile --installer

Requisitos (instalados automaticamente com --setup):
    Python: flet, pyinstaller, pandas, openpyxl, reportlab, cryptography, etc.
    Externo: Inno Setup 6+ (apenas para --installer, download automático)
"""

import os
import subprocess
import shutil
import sys
import urllib.request
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
ICON = ROOT / "assets" / "icon.ico"
ENTRY = ROOT / "App_Treinos_Flet.py"
REQUIREMENTS = ROOT / "requirements.txt"

PRODUCT_NAME = "App Treinos"
PRODUCT_VERSION = "3.1.0"
COMPANY_NAME = "App Treinos"
FILE_DESCRIPTION = "Planejador inteligente de treinos esportivos"
COPYRIGHT = f"© 2026 {COMPANY_NAME}"

INNO_SETUP_URL = "https://jrsoftware.org/download.php/is.exe"


# ── Setup / Instalação de dependências ─────────────────────────

def setup():
    """Instala todas as dependências necessárias para build e deploy."""
    print("[SETUP] Instalando dependencias de build...\n")

    # 1. Dependências Python via requirements.txt
    _install_python_deps()

    # 2. Ferramentas de build (flet CLI + PyInstaller)
    _install_build_tools()

    # 3. Inno Setup (Windows — apenas se não estiver instalado)
    if sys.platform == "win32":
        _install_inno_setup()

    print("\n[OK] Setup concluido. Pronto para build.")


def _install_python_deps():
    """Instala dependências Python do requirements.txt."""
    print("  [1/3] Dependencias Python (requirements.txt)...")

    if not REQUIREMENTS.exists():
        print(f"    [WARN] {REQUIREMENTS} nao encontrado. Pulando.")
        return

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS),
             "--quiet", "--disable-pip-version-check"],
            stdout=subprocess.DEVNULL,
        )
        # Contar pacotes instalados
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=columns"],
            capture_output=True, text=True,
        )
        n_pkgs = max(0, len(result.stdout.strip().splitlines()) - 2)
        print(f"    [OK] {n_pkgs} pacotes disponiveis")
    except subprocess.CalledProcessError as e:
        print(f"    [ERRO] Falha ao instalar dependencias: {e}")
        sys.exit(1)


def _install_build_tools():
    """Garante que flet CLI e PyInstaller estão disponíveis."""
    print("  [2/3] Ferramentas de build (flet, pyinstaller)...")

    missing = []
    if shutil.which("flet") is None:
        missing.append("flet")
    try:
        __import__("PyInstaller")
    except ImportError:
        missing.append("pyinstaller")

    if missing:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + missing
            + ["--quiet", "--disable-pip-version-check"],
            stdout=subprocess.DEVNULL,
        )
        print(f"    [OK] Instalados: {', '.join(missing)}")
    else:
        print("    [OK] Ja instalados")


def _install_inno_setup():
    """Verifica e oferece instalação do Inno Setup no Windows."""
    print("  [3/3] Inno Setup (instalador Windows)...")

    if shutil.which("iscc") is not None:
        print("    [OK] Inno Setup ja instalado")
        return

    # Procurar em caminhos comuns
    common_paths = [
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Inno Setup 6" / "ISCC.exe",
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Inno Setup 6" / "ISCC.exe",
    ]
    for p in common_paths:
        if p.exists():
            print(f"    [OK] Encontrado em {p.parent}")
            print(f"    [DICA] Adicione ao PATH: set PATH=%PATH%;{p.parent}")
            return

    # Não encontrado — fazer download
    print("    [DOWNLOAD] Inno Setup nao encontrado. Baixando instalador...")
    try:
        tmp = Path(tempfile.gettempdir()) / "innosetup_installer.exe"
        urllib.request.urlretrieve(INNO_SETUP_URL, str(tmp))
        size_mb = tmp.stat().st_size / (1024 * 1024)
        print(f"    [OK] Download concluido: {tmp} ({size_mb:.1f} MB)")
        print(f"    [ACAO] Execute o instalador manualmente: {tmp}")
        print("    [DICA] Apos instalar, adicione ao PATH ou reinicie o terminal.")
    except Exception as e:
        print(f"    [WARN] Falha no download: {e}")
        print(f"    [ACAO] Baixe manualmente: {INNO_SETUP_URL}")


def clean():
    """Remove artefatos de build anteriores."""
    for d in [DIST_DIR, BUILD_DIR]:
        if d.exists():
            shutil.rmtree(d)
            print(f"  Removido: {d}")
    print("  [OK] Limpeza concluida.")


def build(onefile: bool = False):
    """Gera executável via ``flet pack``."""
    if shutil.which("flet") is None:
        print("  [ERRO] flet CLI nao encontrado. Execute: python build.py --setup")
        sys.exit(1)

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
        print(f"\n  [OK] Build concluido: {exe_path}")
        print(f"  Tamanho: {size_mb:.1f} MB")
    else:
        # Flet pack pode colocar em local diferente
        candidates = list(DIST_DIR.rglob(exe_name))
        if candidates:
            exe_path = candidates[0]
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n  [OK] Build concluido: {exe_path}")
            print(f"  Tamanho: {size_mb:.1f} MB")
        else:
            print("\n  [WARN] Build concluido mas executavel nao encontrado em dist/.")
            print("  Verifique a saida acima para localizar o artefato.")


def build_installer():
    """Gera instalador Windows via Inno Setup (requer iscc no PATH)."""
    iscc = shutil.which("iscc")
    if iscc is None:
        print("  [ERRO] Inno Setup (iscc) nao encontrado no PATH.")
        print("  Instale em: https://jrsoftware.org/isinfo.php")
        sys.exit(1)

    iss_file = ROOT / "installer.iss"
    if not iss_file.exists():
        print(f"  [ERRO] {iss_file} nao encontrado.")
        sys.exit(1)

    print(f"\n  [BUILD] Gerando instalador com Inno Setup...")
    subprocess.check_call([iscc, str(iss_file)], cwd=str(ROOT))

    setup_exe = DIST_DIR / f"AppTreinos_Setup_{PRODUCT_VERSION}.exe"
    if setup_exe.exists():
        size_mb = setup_exe.stat().st_size / (1024 * 1024)
        print(f"\n  [OK] Instalador gerado: {setup_exe}")
        print(f"  Tamanho: {size_mb:.1f} MB")
    else:
        print("\n  [WARN] Instalador gerado mas nao encontrado em dist/.")


if __name__ == "__main__":
    args = set(sys.argv[1:])

    if "--help" in args or "-h" in args:
        print(__doc__)
        sys.exit(0)

    if "--setup" in args:
        setup()
        args.discard("--setup")
        if not args:
            sys.exit(0)

    if "--clean" in args:
        print("[CLEAN] Limpando artefatos...")
        clean()
        args.discard("--clean")
        if not args:
            sys.exit(0)

    print(f"[BUILD] Gerando executavel {PRODUCT_NAME} v{PRODUCT_VERSION}...")
    build(onefile="--onefile" in args)

    if "--installer" in args:
        build_installer()
