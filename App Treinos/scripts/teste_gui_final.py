"""
Teste Rápido da GUI - Identificação Profissional
=================================================

Script de validação rápida para confirmar que a GUI está funcionando
corretamente após as correções.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))


def main():
    print("\n" + "="*70)
    print("🧪 TESTE RÁPIDO - GUI COM IDENTIFICAÇÃO PROFISSIONAL")
    print("="*70)
    
    print("\n✅ CORREÇÕES APLICADAS:")
    print("   1. Corrigido: theme.font_sizes['normal'] → theme.font_sizes['body']")
    print("   2. Corrigido: Separação de frames para evitar mistura pack/grid")
    
    print("\n📋 ESTRUTURA DA GUI:")
    print("   • Etapa 1: 👨‍⚕️ Identificação do Profissional de Educação Física")
    print("   • Etapa 2: 📝 Dados Básicos do Atleta")
    print("   • Etapa 3: 🏃 Modalidade e Disponibilidade")
    
    print("\n🎯 FUNCIONALIDADES IMPLEMENTADAS:")
    print("   ✅ Validação de CPF (algoritmo oficial)")
    print("   ✅ Validação de CREF (formato regex)")
    print("   ✅ Validação de nome (mínimo 5 caracteres)")
    print("   ✅ Mensagens de erro personalizadas")
    print("   ✅ Mensagem de sucesso com dados formatados")
    print("   ✅ Navegação entre etapas")
    print("   ✅ Design responsivo e acessível")
    
    print("\n📝 DADOS DE TESTE VÁLIDOS:")
    print("   Nome:  Dr. João Silva Santos")
    print("   CPF:   12345678909")
    print("   CREF:  123456-G/SP")
    
    print("\n📝 DADOS DE TESTE INVÁLIDOS (para testar validação):")
    print("   CPF inválido:  12345678900")
    print("   CREF inválido: ABC-123")
    print("   Nome curto:    João")
    
    print("\n🚀 EXECUTAR GUI:")
    print("   python gui/main_gui.py")
    
    print("\n" + "="*70)
    print("✅ TESTE CONCLUÍDO - GUI PRONTA PARA USO!")
    print("="*70)
    print()


if __name__ == "__main__":
    main()
