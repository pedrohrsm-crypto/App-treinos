"""
Demonstração: Scripts de Execução com Duplo Clique
===================================================

Este script demonstra os arquivos criados para execução
rápida do App Treinos em diferentes sistemas operacionais.
"""

import os
import platform

def mostrar_scripts_disponiveis():
    """Mostra os scripts de execução disponíveis no sistema atual."""
    
    print("\n" + "="*70)
    print(" SCRIPTS DE EXECUÇÃO RÁPIDA - APP TREINOS")
    print("="*70)
    
    sistema = platform.system()
    
    print(f"\n📌 Sistema Operacional Detectado: {sistema}")
    print(f"   Versão: {platform.version()}")
    print(f"   Python: {platform.python_version()}")
    
    print("\n" + "─"*70)
    
    # Windows
    if sistema == "Windows":
        print("\n🪟 WINDOWS - Script Disponível:")
        print("   └─ App_Treinos.bat")
        print("\n   📝 Como usar:")
        print("      1. Duplo clique em: App_Treinos.bat")
        print("      2. Pronto! ✅")
        print("\n   🎯 Criar atalho na Área de Trabalho:")
        print("      1. Clique direito em App_Treinos.bat")
        print("      2. Enviar para → Área de trabalho (criar atalho)")
        
        if os.path.exists("App_Treinos.bat"):
            tamanho = os.path.getsize("App_Treinos.bat")
            print(f"\n   ✅ Arquivo encontrado ({tamanho} bytes)")
        else:
            print("\n   ❌ Arquivo NÃO encontrado!")
    
    # macOS
    elif sistema == "Darwin":
        print("\n🍎 MACOS - Script Disponível:")
        print("   └─ App_Treinos.command")
        print("\n   📝 Como usar:")
        print("      1. Executar: chmod +x App_Treinos.command")
        print("      2. Duplo clique em: App_Treinos.command")
        print("      3. (Primeira vez: permitir em Segurança)")
        print("\n   🎯 Adicionar ao Dock:")
        print("      1. Arraste App_Treinos.command para o Dock")
        
        if os.path.exists("App_Treinos.command"):
            tamanho = os.path.getsize("App_Treinos.command")
            executavel = os.access("App_Treinos.command", os.X_OK)
            print(f"\n   ✅ Arquivo encontrado ({tamanho} bytes)")
            print(f"   {'✅' if executavel else '❌'} Permissão de execução: {'SIM' if executavel else 'NÃO'}")
            if not executavel:
                print("      Execute: chmod +x App_Treinos.command")
        else:
            print("\n   ❌ Arquivo NÃO encontrado!")
    
    # Linux
    elif sistema == "Linux":
        print("\n🐧 LINUX - Scripts Disponíveis:")
        print("   ├─ linux/App_Treinos.desktop")
        print("   └─ linux/app_treinos_launcher.sh")
        print("\n   📝 Como usar:")
        print("      1. chmod +x linux/app_treinos_launcher.sh")
        print("      2. cp linux/App_Treinos.desktop ~/.local/share/applications/")
        print("      3. Procure 'App Treinos' no menu de aplicativos")
        print("\n   🎯 Atalho na Área de Trabalho:")
        print("      1. cp linux/App_Treinos.desktop ~/Desktop/")
        print("      2. chmod +x ~/Desktop/App_Treinos.desktop")
        
        desktop_path = os.path.join("linux", "App_Treinos.desktop")
        launcher_path = os.path.join("linux", "app_treinos_launcher.sh")
        
        if os.path.exists(desktop_path):
            tamanho = os.path.getsize(desktop_path)
            print(f"\n   ✅ App_Treinos.desktop encontrado ({tamanho} bytes)")
        else:
            print("\n   ❌ App_Treinos.desktop NÃO encontrado!")
        
        if os.path.exists(launcher_path):
            tamanho = os.path.getsize(launcher_path)
            executavel = os.access(launcher_path, os.X_OK)
            print(f"   ✅ app_treinos_launcher.sh encontrado ({tamanho} bytes)")
            print(f"   {'✅' if executavel else '❌'} Permissão de execução: {'SIM' if executavel else 'NÃO'}")
            if not executavel:
                print("      Execute: chmod +x linux/app_treinos_launcher.sh")
        else:
            print("   ❌ app_treinos_launcher.sh NÃO encontrado!")
    
    print("\n" + "─"*70)
    
    # Documentação
    print("\n📖 DOCUMENTAÇÃO DISPONÍVEL:")
    
    docs = {
        "EXECUCAO_DUPLO_CLIQUE.md": "Guia completo de execução rápida",
        "LEIA-ME_EXECUCAO_RAPIDA.txt": "Resumo de instalação",
        "COMPATIBILIDADE_MULTIPLATAFORMA.md": "Guia de compatibilidade",
    }
    
    for doc, descricao in docs.items():
        if os.path.exists(doc):
            tamanho = os.path.getsize(doc) / 1024  # KB
            print(f"   ✅ {doc}")
            print(f"      └─ {descricao} ({tamanho:.1f} KB)")
        else:
            print(f"   ❌ {doc}")
    
    print("\n" + "="*70)
    
    # Funcionalidades dos scripts
    print("\n🎨 FUNCIONALIDADES DOS SCRIPTS:\n")
    print("   ✅ Verificação automática de Python instalado")
    print("   ✅ Verificação automática de dependências (pandas, openpyxl)")
    print("   ✅ Instalação automática se necessário")
    print("   ✅ Mensagens de erro claras e orientativas")
    print("   ✅ Banner profissional de inicialização")
    print("   ✅ Janela permanece aberta após execução")
    print("   ✅ Encoding UTF-8 configurado automaticamente")
    
    print("\n" + "="*70)
    
    # Benefícios
    print("\n🎯 BENEFÍCIOS:\n")
    print("   🖱️  Execução com apenas 2 cliques do mouse")
    print("   👥 Acessível para usuários não-técnicos")
    print("   💼 Aparência profissional de aplicativo comercial")
    print("   🔧 Instalação automática de dependências")
    print("   🌍 Funciona em Windows, Linux e macOS")
    print("   📝 Mensagens claras de erro e orientação")
    
    print("\n" + "="*70)
    print("\n💡 DICA: Para instruções detalhadas, abra:")
    print("   📄 EXECUCAO_DUPLO_CLIQUE.md\n")


if __name__ == "__main__":
    mostrar_scripts_disponiveis()
