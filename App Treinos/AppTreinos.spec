# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\GitHub\\App Treinos\\Python\\App Treinos\\App_Treinos_Flet.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\GitHub\\App Treinos\\Python\\App Treinos\\data', 'data'), ('D:\\GitHub\\App Treinos\\Python\\App Treinos\\version.py', '.'), ('D:\\GitHub\\App Treinos\\Python\\App Treinos\\i18n.py', '.'), ('D:\\GitHub\\App Treinos\\Python\\App Treinos\\flet_app', 'flet_app'), ('D:\\GitHub\\App Treinos\\Python\\App Treinos\\core', 'core'), ('D:\\GitHub\\App Treinos\\Python\\App Treinos\\assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AppTreinos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='C:\\Users\\Pedro Marques\\AppData\\Local\\Temp\\5c7c2499-e04c-4c3f-886f-9205a5ccec14',
    icon=['D:\\GitHub\\App Treinos\\Python\\App Treinos\\assets\\icon.ico'],
)
