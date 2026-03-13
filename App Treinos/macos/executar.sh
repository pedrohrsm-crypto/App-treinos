#!/bin/bash
# Script de execução do App Treinos para macOS

clear
echo "=================================================="
echo "  🍎 App Treinos - Sistema de Planejamento"
echo "=================================================="
echo ""

# Verificar se está no diretório correto
if [ ! -f "../training_planner.py" ]; then
    echo "❌ Erro: training_planner.py não encontrado!"
    echo "   Execute este script a partir do diretório macos/"
    exit 1
fi

# Verificar dependências
python3 -c "import pandas, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Dependências não instaladas!"
    echo "   Executando instalação..."
    ./instalar.sh
    echo ""
fi

# Configurar locale para UTF-8 (importante no macOS)
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# Executar o sistema
cd ..
python3 training_planner.py
