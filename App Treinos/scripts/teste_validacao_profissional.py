"""
Teste da Identificação do Profissional - Validação de CPF e CREF
==================================================================

Testa as funções de validação de CPF e CREF do profissional.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from training_planner import TrainerInfo


def testar_validacoes():
    """Testa validações de CPF e CREF."""
    
    print("\n" + "="*80)
    print(" TESTE DE VALIDAÇÃO - DADOS DO PROFISSIONAL")
    print("="*80 + "\n")
    
    # Teste 1: CPF Válido
    print("📋 Teste 1: CPF Válido")
    cpf_valido = "12345678909"  # CPF válido (exemplo)
    if TrainerInfo._validar_cpf(cpf_valido):
        print(f"   ✅ CPF {cpf_valido} - VÁLIDO")
    else:
        print(f"   ❌ CPF {cpf_valido} - INVÁLIDO (erro!)")
    
    # Teste 2: CPF Inválido
    print("\n📋 Teste 2: CPF Inválido")
    cpf_invalido = "12345678900"
    if not TrainerInfo._validar_cpf(cpf_invalido):
        print(f"   ✅ CPF {cpf_invalido} - INVÁLIDO (como esperado)")
    else:
        print(f"   ❌ CPF {cpf_invalido} - VÁLIDO (erro!)")
    
    # Teste 3: CPF com todos dígitos iguais
    print("\n📋 Teste 3: CPF com dígitos iguais")
    cpf_igual = "11111111111"
    if not TrainerInfo._validar_cpf(cpf_igual):
        print(f"   ✅ CPF {cpf_igual} - INVÁLIDO (como esperado)")
    else:
        print(f"   ❌ CPF {cpf_igual} - VÁLIDO (erro!)")
    
    # Teste 4: CREF Válido - Formato 1
    print("\n📋 Teste 4: CREF Válido - Formato 123456-G/SP")
    cref_valido1 = "123456-G/SP"
    if TrainerInfo._validar_cref(cref_valido1):
        print(f"   ✅ CREF {cref_valido1} - VÁLIDO")
    else:
        print(f"   ❌ CREF {cref_valido1} - INVÁLIDO (erro!)")
    
    # Teste 5: CREF Válido - Formato 2
    print("\n📋 Teste 5: CREF Válido - Formato CREF1 123456-G/RJ")
    cref_valido2 = "CREF1 123456-G/RJ"
    if TrainerInfo._validar_cref(cref_valido2):
        print(f"   ✅ CREF {cref_valido2} - VÁLIDO")
    else:
        print(f"   ❌ CREF {cref_valido2} - INVÁLIDO (erro!)")
    
    # Teste 6: CREF Inválido
    print("\n📋 Teste 6: CREF Inválido")
    cref_invalido = "ABC-123"
    if not TrainerInfo._validar_cref(cref_invalido):
        print(f"   ✅ CREF {cref_invalido} - INVÁLIDO (como esperado)")
    else:
        print(f"   ❌ CREF {cref_invalido} - VÁLIDO (erro!)")
    
    # Teste 7: Criar TrainerInfo válido
    print("\n📋 Teste 7: Criar TrainerInfo com dados válidos")
    try:
        trainer = TrainerInfo(
            nome_completo="Dr. João Silva Santos",
            cpf="12345678909",
            cref="123456-G/SP"
        )
        print(f"   ✅ TrainerInfo criado com sucesso!")
        print(f"   Nome: {trainer.nome_completo}")
        print(f"   CPF: {trainer.formatar_cpf()}")
        print(f"   CREF: {trainer.formatar_cref()}")
    except ValueError as e:
        print(f"   ❌ Erro ao criar TrainerInfo: {e}")
    
    # Teste 8: Criar TrainerInfo com CPF inválido
    print("\n📋 Teste 8: Criar TrainerInfo com CPF inválido")
    try:
        trainer = TrainerInfo(
            nome_completo="Dr. Maria Silva",
            cpf="12345678900",  # CPF inválido
            cref="123456-G/SP"
        )
        print(f"   ❌ TrainerInfo criado (deveria falhar!)")
    except ValueError as e:
        print(f"   ✅ Erro esperado capturado: {e}")
    
    # Teste 9: Criar TrainerInfo com CREF inválido
    print("\n📋 Teste 9: Criar TrainerInfo com CREF inválido")
    try:
        trainer = TrainerInfo(
            nome_completo="Dr. Pedro Santos",
            cpf="12345678909",
            cref="ABC123"  # CREF inválido
        )
        print(f"   ❌ TrainerInfo criado (deveria falhar!)")
    except ValueError as e:
        print(f"   ✅ Erro esperado capturado: {e}")
    
    print("\n" + "="*80)
    print(" ✅ TESTES CONCLUÍDOS!")
    print("="*80 + "\n")


if __name__ == "__main__":
    testar_validacoes()
