"""
App Treinos - Launcher Principal com GUI
=========================================

Duplo clique para executar a interface gráfica.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from gui.main_gui import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se de que todos os arquivos estão no lugar correto.")
    input("Pressione ENTER para sair...")
except Exception as e:
    print(f"Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
    input("Pressione ENTER para sair...")
