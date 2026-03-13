#!/bin/bash
# ===============================================
# App Treinos - Sistema de Planejamento de Treino
# Launcher para Linux (.desktop)
# ===============================================

# Obter diretório do script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MAIN_DIR="$(dirname "$SCRIPT_DIR")"
cd "$MAIN_DIR"

# Configurar UTF-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Limpar tela
clear

# Banner de inicialização
echo ""
echo "==============================================="
echo "   APP TREINOS - SISTEMA PROFISSIONAL"
echo "==============================================="
echo ""
echo "Iniciando sistema..."
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 não encontrado!"
    echo ""
    echo "Por favor, instale Python 3.8+:"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get install python3 python3-pip"
    echo ""
    echo "Fedora/RedHat:"
    echo "  sudo yum install python3 python3-pip"
    echo ""
    echo "Arch Linux:"
    echo "  sudo pacman -S python python-pip"
    echo ""
    read -p "Pressione ENTER para sair..."
    exit 1
fi

# Verificar se o arquivo principal existe
if [ ! -f "training_planner.py" ]; then
    echo "[ERRO] Arquivo training_planner.py não encontrado!"
    echo ""
    echo "Diretório atual: $(pwd)"
    echo ""
    echo "Certifique-se de que o arquivo está no local correto."
    echo ""
    read -p "Pressione ENTER para sair..."
    exit 1
fi

# Verificar dependências
echo "Verificando dependências..."
python3 -c "import pandas, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "[AVISO] Dependências não encontradas."
    echo "Instalando pandas e openpyxl..."
    echo ""
    python3 -m pip install --user pandas openpyxl
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERRO] Falha ao instalar dependências."
        echo "Tente executar manualmente:"
        echo "  pip3 install --user pandas openpyxl"
        echo ""
        read -p "Pressione ENTER para sair..."
        exit 1
    fi
fi

# Executar o sistema
echo ""
echo "==============================================="
echo ""
python3 training_planner.py

# Verificar se houve erro na execução
if [ $? -ne 0 ]; then
    echo ""
    echo "==============================================="
    echo "[ERRO] O sistema encontrou um problema."
    echo "==============================================="
    echo ""
fi

# Manter janela aberta
echo ""
echo "==============================================="
echo "Execução concluída."
echo "==============================================="
echo ""
read -p "Pressione ENTER para sair..."
