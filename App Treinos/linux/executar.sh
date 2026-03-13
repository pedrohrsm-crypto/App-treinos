#!/bin/bash
# Script de execução do App Treinos para Linux

clear
echo "=================================================="
echo "  🏃 App Treinos - Sistema de Planejamento"
echo "=================================================="
echo ""

# Verificar se está no diretório correto
if [ ! -f "../training_planner.py" ]; then
    echo "❌ Erro: training_planner.py não encontrado!"
    echo "   Execute este script a partir do diretório linux/"
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

# Executar o sistema
cd ..
python3 training_planner.py
