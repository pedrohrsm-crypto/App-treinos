"""
Teste de Caminhos e Estrutura - App Treinos
===========================================

Verifica se todos os diretórios e arquivos estão nos lugares corretos.
"""

import os
import sys
from pathlib import Path

def verificar_estrutura():
    """Verifica estrutura de diretórios."""
    
    print("\n" + "="*80)
    print(" VERIFICAÇÃO DA ESTRUTURA DE DIRETÓRIOS - APP TREINOS")
    print("="*80 + "\n")
    
    # Diretório raiz é o pai do diretório scripts
    root_dir = Path(__file__).parent.parent
    print(f"📁 Diretório raiz: {root_dir}\n")
    
    # Estrutura esperada
    estrutura = {
        'gui': {
            'tipo': 'dir',
            'descricao': 'Interface Gráfica',
            'arquivos': ['__init__.py', 'theme.py', 'main_gui.py', 'wizard_steps.py']
        },
        'core': {
            'tipo': 'dir',
            'descricao': 'Motor do Aplicativo',
            'arquivos': ['__init__.py', 'training_engine.py']
        },
        'data': {
            'tipo': 'dir',
            'descricao': 'Dados e Exportações',
            'arquivos': []
        },
        'docs': {
            'tipo': 'dir',
            'descricao': 'Documentação',
            'arquivos': ['GUI_MANUAL.md']
        },
        'scripts': {
            'tipo': 'dir',
            'descricao': 'Scripts Auxiliares',
            'arquivos': []
        },
        'linux': {
            'tipo': 'dir',
            'descricao': 'Scripts Linux',
            'arquivos': ['instalar.sh', 'executar.sh']
        },
        'macos': {
            'tipo': 'dir',
            'descricao': 'Scripts macOS',
            'arquivos': ['instalar.sh', 'executar.sh']
        }
    }
    
    # Arquivos principais na raiz
    arquivos_raiz = [
        'App_Treinos_GUI.py',
        'App_Treinos_GUI.bat',
        'App_Treinos.bat',
        'App_Treinos.command',
        'training_planner.py',
        'requirements.txt'
    ]
    
    resultados = {
        'diretorios_ok': 0,
        'diretorios_faltando': 0,
        'arquivos_ok': 0,
        'arquivos_faltando': 0
    }
    
    # Verificar diretórios
    print("🔍 VERIFICANDO DIRETÓRIOS:\n")
    
    for nome_dir, info in estrutura.items():
        dir_path = root_dir / nome_dir
        if dir_path.exists() and dir_path.is_dir():
            print(f"  ✅ /{nome_dir}/ - {info['descricao']}")
            resultados['diretorios_ok'] += 1
            
            # Verificar arquivos dentro
            if info['arquivos']:
                for arquivo in info['arquivos']:
                    arquivo_path = dir_path / arquivo
                    if arquivo_path.exists():
                        print(f"     ✅ {arquivo}")
                        resultados['arquivos_ok'] += 1
                    else:
                        print(f"     ❌ {arquivo} (FALTANDO)")
                        resultados['arquivos_faltando'] += 1
        else:
            print(f"  ❌ /{nome_dir}/ - {info['descricao']} (FALTANDO)")
            resultados['diretorios_faltando'] += 1
    
    print("\n" + "─"*80)
    print("\n🔍 VERIFICANDO ARQUIVOS PRINCIPAIS:\n")
    
    for arquivo in arquivos_raiz:
        arquivo_path = root_dir / arquivo
        if arquivo_path.exists():
            tamanho = arquivo_path.stat().st_size
            print(f"  ✅ {arquivo} ({tamanho:,} bytes)")
            resultados['arquivos_ok'] += 1
        else:
            print(f"  ❌ {arquivo} (FALTANDO)")
            resultados['arquivos_faltando'] += 1
    
    print("\n" + "─"*80)
    print("\n📊 RESUMO:\n")
    
    total_dirs = resultados['diretorios_ok'] + resultados['diretorios_faltando']
    total_arqs = resultados['arquivos_ok'] + resultados['arquivos_faltando']
    
    print(f"  Diretórios: {resultados['diretorios_ok']}/{total_dirs} OK")
    print(f"  Arquivos: {resultados['arquivos_ok']}/{total_arqs} OK")
    
    if resultados['diretorios_faltando'] == 0 and resultados['arquivos_faltando'] == 0:
        print("\n  ✅ ESTRUTURA COMPLETA E CORRETA!")
        status = True
    else:
        print("\n  ⚠️  ALGUNS ITENS ESTÃO FALTANDO")
        status = False
    
    print("\n" + "="*80 + "\n")
    
    return status


def testar_imports():
    """Testa se os imports funcionam."""
    
    print("\n" + "="*80)
    print(" VERIFICAÇÃO DE IMPORTS")
    print("="*80 + "\n")
    
    # Adicionar o diretório raiz ao path para testar imports
    root_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(root_dir))
    
    imports = [
        ('gui.theme', 'Tema acessível'),
        ('gui', 'Módulo GUI'),
    ]
    
    resultados = {'ok': 0, 'erro': 0}
    
    for modulo, descricao in imports:
        try:
            __import__(modulo)
            print(f"  ✅ {modulo} - {descricao}")
            resultados['ok'] += 1
        except ImportError as e:
            print(f"  ❌ {modulo} - ERRO: {e}")
            resultados['erro'] += 1
    
    print("\n" + "─"*80)
    print(f"\n  Imports: {resultados['ok']}/{len(imports)} OK\n")
    
    if resultados['erro'] == 0:
        print("  ✅ TODOS OS IMPORTS FUNCIONANDO!")
        status = True
    else:
        print("  ⚠️  ALGUNS IMPORTS COM PROBLEMA")
        status = False
    
    print("\n" + "="*80 + "\n")
    
    return status


def verificar_dependencias():
    """Verifica dependências Python."""
    
    print("\n" + "="*80)
    print(" VERIFICAÇÃO DE DEPENDÊNCIAS")
    print("="*80 + "\n")
    
    dependencias = [
        ('tkinter', 'Interface Gráfica'),
        ('pandas', 'Manipulação de Dados'),
        ('openpyxl', 'Exportação Excel'),
    ]
    
    resultados = {'ok': 0, 'faltando': 0}
    
    for modulo, descricao in dependencias:
        try:
            mod = __import__(modulo)
            versao = getattr(mod, '__version__', 'N/A')
            print(f"  ✅ {modulo} ({versao}) - {descricao}")
            resultados['ok'] += 1
        except ImportError:
            print(f"  ❌ {modulo} - FALTANDO - {descricao}")
            resultados['faltando'] += 1
    
    print("\n" + "─"*80)
    print(f"\n  Dependências: {resultados['ok']}/{len(dependencias)} instaladas\n")
    
    if resultados['faltando'] == 0:
        print("  ✅ TODAS AS DEPENDÊNCIAS INSTALADAS!")
        status = True
    else:
        print("  ⚠️  INSTALE AS DEPENDÊNCIAS FALTANTES:")
        print("      pip install pandas openpyxl")
        status = False
    
    print("\n" + "="*80 + "\n")
    
    return status


def main():
    """Executa todas as verificações."""
    
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " TESTE COMPLETO DE ESTRUTURA E CAMINHOS ".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    
    # Executar verificações
    est_ok = verificar_estrutura()
    imp_ok = testar_imports()
    dep_ok = verificar_dependencias()
    
    # Resultado final
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " RESULTADO FINAL ".center(78) + "║")
    print("╚" + "═"*78 + "╝\n")
    
    if est_ok and imp_ok and dep_ok:
        print("  🎉 TUDO OK! O aplicativo está pronto para uso.")
        print("\n  Para executar a GUI:")
        print("     Windows: App_Treinos_GUI.bat")
        print("     Linux/Mac: python3 App_Treinos_GUI.py")
    else:
        print("  ⚠️  Há problemas que precisam ser corrigidos.")
        if not est_ok:
            print("     • Estrutura de diretórios incompleta")
        if not imp_ok:
            print("     • Problemas com imports de módulos")
        if not dep_ok:
            print("     • Dependências Python faltando")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
