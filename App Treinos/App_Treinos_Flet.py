"""
App Treinos — Launcher Flet
============================

Script de arranque rápido para a interface Flet (Flutter em Python).
Executa: python App_Treinos_Flet.py
"""

import sys
import os

# Garantir que o diretório do script está no path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

try:
    import flet as ft
except ImportError:
    print("❌ Flet não está instalado. Execute: pip install flet>=0.25.0")
    sys.exit(1)

from flet_app.main import main

if __name__ == "__main__":
    ft.app(target=main)
