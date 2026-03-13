#!/bin/bash
# Menu de exemplos para macOS

clear
echo "=========================================="
echo "  🍎 App Treinos - Menu de Exemplos"
echo "=========================================="
echo ""
echo "Escolha um exemplo para executar:"
echo ""
echo "1. Periodização (8/20/40 semanas)"
echo "2. Cálculo automático de semanas"
echo "3. Demonstração de mensagens de limite"
echo "4. Comparação de modos de configuração"
echo "5. Teste de cálculo de semanas"
echo "6. Teste da IA de saúde"
echo "7. Exemplos diversos de atletas"
echo "8. Resumo da implementação"
echo "0. Sair"
echo ""
read -p "Digite sua escolha (0-8): " choice

cd ..

# Configurar locale para UTF-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

case $choice in
    1)
        echo ""
        python3 exemplo_periodizacao.py
        ;;
    2)
        echo ""
        python3 exemplo_calculo_automatico.py
        ;;
    3)
        echo ""
        python3 demo_mensagens_limite.py
        ;;
    4)
        echo ""
        python3 comparacao_modos_configuracao.py
        ;;
    5)
        echo ""
        python3 teste_calculo_semanas.py
        ;;
    6)
        echo ""
        python3 teste_ia_saude.py
        ;;
    7)
        echo ""
        python3 exemplos.py
        ;;
    8)
        echo ""
        python3 resumo_implementacao.py
        ;;
    0)
        echo "Até logo!"
        exit 0
        ;;
    *)
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Pressione ENTER para voltar ao menu..."
read
./macos/exemplos.sh
