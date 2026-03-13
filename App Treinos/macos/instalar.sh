#!/bin/bash
# Script de instalação para macOS

echo "=================================================="
echo "  🍎 App Treinos - Instalação para macOS"
echo "=================================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo ""
    echo "   Opções de instalação:"
    echo "   1. Homebrew (recomendado):"
    echo "      brew install python3"
    echo ""
    echo "   2. Download direto:"
    echo "      https://www.python.org/downloads/macos/"
    echo ""
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "⚠️  pip3 não encontrado, instalando..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py --user
    rm get-pip.py
fi

echo "✅ pip encontrado: $(pip3 --version)"
echo ""

# Verificar Homebrew (opcional, mas recomendado)
if command -v brew &> /dev/null; then
    echo "✅ Homebrew detectado: $(brew --version | head -n1)"
else
    echo "💡 Dica: Considere instalar Homebrew para gerenciar dependências:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
fi
echo ""

# Instalar dependências
echo "📦 Instalando dependências Python..."
pip3 install --user pandas>=2.0.0 openpyxl>=3.1.0

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✅ Instalação concluída com sucesso!"
    echo "=================================================="
    echo ""
    echo "🚀 Para executar o sistema:"
    echo "   ./macos/executar.sh"
    echo ""
    echo "📚 Para ver exemplos:"
    echo "   ./macos/exemplos.sh"
    echo ""
    echo "💡 Dica: Adicione permissões de execução se necessário:"
    echo "   chmod +x macos/*.sh"
    echo ""
else
    echo ""
    echo "❌ Erro ao instalar dependências!"
    echo "   Tente executar manualmente:"
    echo "   pip3 install --user pandas openpyxl"
    exit 1
fi
