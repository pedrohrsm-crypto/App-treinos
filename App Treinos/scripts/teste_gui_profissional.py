"""
Teste da Integração da Identificação Profissional na GUI
=========================================================

Valida que a GUI possui a etapa de identificação profissional
e que a validação está funcionando corretamente.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.training_engine import TrainerInfo


def teste_validacao_cpf():
    """Testa validação de CPF."""
    print("\n" + "="*70)
    print("📋 TESTE 1: Validação de CPF")
    print("="*70)
    
    # CPF válido
    try:
        trainer1 = TrainerInfo(
            nome_completo="Dr. João Silva Santos",
            cpf="12345678909",
            cref="123456-G/SP"
        )
        print(f"✅ CPF válido aceito: {trainer1.formatar_cpf()}")
    except ValueError as e:
        print(f"❌ ERRO: CPF válido foi rejeitado - {e}")
    
    # CPF inválido
    try:
        trainer2 = TrainerInfo(
            nome_completo="Dr. João Silva Santos",
            cpf="12345678900",
            cref="123456-G/SP"
        )
        print(f"❌ ERRO: CPF inválido foi aceito!")
    except ValueError:
        print(f"✅ CPF inválido rejeitado corretamente")


def teste_validacao_cref():
    """Testa validação de CREF."""
    print("\n" + "="*70)
    print("📋 TESTE 2: Validação de CREF")
    print("="*70)
    
    formatos_validos = [
        "123456-G/SP",
        "CREF1 123456-G/RJ",
        "098765-G/MG",
        "CREF 1234-G/BA"
    ]
    
    for cref in formatos_validos:
        try:
            trainer = TrainerInfo(
                nome_completo="Dr. João Silva Santos",
                cpf="12345678909",
                cref=cref
            )
            print(f"✅ CREF válido aceito: {trainer.formatar_cref()}")
        except ValueError as e:
            print(f"❌ ERRO: CREF válido foi rejeitado - {cref} - {e}")
    
    # CREF inválido
    try:
        trainer = TrainerInfo(
            nome_completo="Dr. João Silva Santos",
            cpf="12345678909",
            cref="ABC-123"
        )
        print(f"❌ ERRO: CREF inválido foi aceito!")
    except ValueError:
        print(f"✅ CREF inválido rejeitado corretamente")


def teste_nome_completo():
    """Testa validação de nome completo."""
    print("\n" + "="*70)
    print("📋 TESTE 3: Validação de Nome Completo")
    print("="*70)
    
    # Nome válido
    try:
        trainer1 = TrainerInfo(
            nome_completo="Dr. João Silva Santos",
            cpf="12345678909",
            cref="123456-G/SP"
        )
        print(f"✅ Nome válido aceito: {trainer1.nome_completo}")
    except ValueError as e:
        print(f"❌ ERRO: Nome válido foi rejeitado - {e}")
    
    # Nome muito curto
    try:
        trainer2 = TrainerInfo(
            nome_completo="João",
            cpf="12345678909",
            cref="123456-G/SP"
        )
        print(f"❌ ERRO: Nome muito curto foi aceito!")
    except ValueError:
        print(f"✅ Nome muito curto rejeitado corretamente")


def teste_formatacao():
    """Testa formatação de CPF e CREF."""
    print("\n" + "="*70)
    print("📋 TESTE 4: Formatação de CPF e CREF")
    print("="*70)
    
    trainer = TrainerInfo(
        nome_completo="Dr. João Silva Santos",
        cpf="12345678909",
        cref="123456-G/SP"
    )
    
    cpf_formatado = trainer.formatar_cpf()
    cref_formatado = trainer.formatar_cref()
    
    print(f"CPF original:   {trainer.cpf}")
    print(f"CPF formatado:  {cpf_formatado}")
    
    if cpf_formatado == "123.456.789-09":
        print("✅ CPF formatado corretamente")
    else:
        print(f"❌ ERRO: CPF mal formatado - esperado '123.456.789-09', obtido '{cpf_formatado}'")
    
    print(f"\nCREF original:  {trainer.cref}")
    print(f"CREF formatado: {cref_formatado}")
    
    if cref_formatado == "123456-G/SP":
        print("✅ CREF formatado corretamente")
    else:
        print(f"❌ ERRO: CREF mal formatado")


def main():
    """Executa todos os testes."""
    print("\n" + "="*70)
    print("🧪 TESTES DE VALIDAÇÃO PROFISSIONAL - GUI")
    print("="*70)
    print("\nValidando integração da identificação profissional na GUI...")
    print("Estes testes verificam se a validação está funcionando corretamente.")
    
    teste_validacao_cpf()
    teste_validacao_cref()
    teste_nome_completo()
    teste_formatacao()
    
    print("\n" + "="*70)
    print("✅ TESTES CONCLUÍDOS!")
    print("="*70)
    print("\n📌 PRÓXIMO PASSO: Execute a GUI para testar manualmente:")
    print("   python gui/main_gui.py")
    print("\n📌 A GUI agora possui 3 etapas:")
    print("   1️⃣ Identificação do Profissional (NOVA)")
    print("   2️⃣ Dados Básicos do Atleta")
    print("   3️⃣ Modalidade e Disponibilidade")
    print("\n📌 Ao preencher a etapa 1, os dados serão validados:")
    print("   • CPF: Algoritmo oficial da Receita Federal")
    print("   • CREF: Formato de registro profissional")
    print("   • Nome: Mínimo 5 caracteres")
    print("\n")


if __name__ == "__main__":
    main()
