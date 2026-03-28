# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec — App Treinos
===============================

Gera executável standalone multiplataforma.
Uso: pyinstaller AppTreinos.spec
"""

import sys
from pathlib import Path

block_cipher = None
ROOT = Path(SPECPATH)

a = Analysis(
    [str(ROOT / 'App_Treinos_GUI.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / 'data'), 'data'),
        (str(ROOT / 'version.py'), '.'),
        (str(ROOT / 'i18n.py'), '.'),
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'reportlab',
        'reportlab.lib',
        'reportlab.lib.pagesizes',
        'reportlab.platypus',
        'reportlab.lib.styles',
        'reportlab.lib.units',
        'reportlab.graphics',
        'sqlite3',
        'tkinter',
        'json',
        'csv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy.testing', 'scipy', 'PIL'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AppTreinos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,     # GUI app — sem janela de console
    icon=None,         # Substituir por ícone .ico quando disponível
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AppTreinos',
)
