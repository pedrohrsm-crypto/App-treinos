#!/bin/bash
# Script de instalação para Linux

echo "=================================================="
echo "  App Treinos - Instalação para Linux"
echo "=================================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "   Por favor, instale Python 3.8 ou superior:"
    echo "   sudo apt-get install python3 python3-pip  # Debian/Ubuntu"
    echo "   sudo yum install python3 python3-pip      # RedHat/CentOS"
    echo "   sudo pacman -S python python-pip          # Arch Linux"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado!"
    echo "   Instalando pip..."
    sudo apt-get install python3-pip -y || sudo yum install python3-pip -y || sudo pacman -S python-pip
fi

echo "✅ pip encontrado: $(pip3 --version)"
echo ""

# Instalar dependências
echo "📦 Instalando dependências..."
pip3 install --user pandas>=2.0.0 openpyxl>=3.1.0

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✅ Instalação concluída com sucesso!"
    echo "=================================================="
    echo ""
    echo "🚀 Para executar o sistema:"
    echo "   ./linux/executar.sh"
    echo ""
    echo "📚 Para ver exemplos:"
    echo "   ./linux/exemplos.sh"
    echo ""
else
    echo ""
    echo "❌ Erro ao instalar dependências!"
    echo "   Tente executar manualmente:"
    echo "   pip3 install pandas openpyxl"
    exit 1
fi
