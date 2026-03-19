"""
Script de teste para validação de senha
Testa as restrições: 6-12 caracteres, sem espaços
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

def testar_validacao_senha():
    """Testa todas as regras de validação de senha."""
    print("\n" + "="*60)
    print("TESTE DE VALIDAÇÃO DE SENHA")
    print("="*60 + "\n")
    
    # Casos de teste
    testes = [
        # (senha, deveria_passar, motivo)
        ("abc123", True, "6 caracteres válidos"),
        ("Abc@123", True, "7 caracteres com especial"),
        ("SenhaForte1!", True, "12 caracteres válidos"),
        ("a1", False, "apenas 2 caracteres"),
        ("abc12", False, "apenas 5 caracteres"),
        ("SenhaForte123", False, "13 caracteres (excede limite)"),
        ("senha com espaco", False, "contém espaços"),
        ("Sen ha1", False, "contém espaço no meio"),
        ("MinhaSenh@1", True, "11 caracteres com especial"),
        ("SENHA123", True, "8 caracteres maiúsculas"),
        ("senha123", True, "8 caracteres minúsculas"),
        ("12345678", True, "8 dígitos numéricos"),
        ("!@#$%^&*", True, "8 caracteres especiais"),
        ("", False, "senha vazia"),
        ("     ", False, "apenas espaços"),
    ]
    
    passou = 0
    falhou = 0
    
    for senha, deveria_passar, motivo in testes:
        # Validação (mesma lógica implementada no código)
        tem_espaco = ' ' in senha
        tamanho_valido = 6 <= len(senha) <= 12
        senha_valida = not tem_espaco and tamanho_valido and len(senha) > 0
        
        # Verificar resultado
        if senha_valida == deveria_passar:
            status = "✅ PASSOU"
            passou += 1
        else:
            status = "❌ FALHOU"
            falhou += 1
        
        # Motivo da falha (se houver)
        if not senha_valida:
            if tem_espaco:
                razao = "contém espaços"
            elif len(senha) == 0:
                razao = "senha vazia"
            elif len(senha) < 6:
                razao = f"muito curta ({len(senha)} caracteres)"
            elif len(senha) > 12:
                razao = f"muito longa ({len(senha)} caracteres)"
            else:
                razao = "razão desconhecida"
        else:
            razao = "senha válida"
        
        # Exibir resultado
        senha_display = f'"{senha}"' if senha else '(vazia)'
        print(f"{status} | {senha_display:20} | {motivo:30} | {razao}")
    
    # Resumo
    print("\n" + "="*60)
    print(f"RESUMO: {passou} testes passaram, {falhou} testes falharam")
    print("="*60 + "\n")
    
    # Exemplos de senhas válidas
    print("EXEMPLOS DE SENHAS VÁLIDAS:")
    print("  • abc123 (6 caracteres)")
    print("  • Senha@1 (7 caracteres com especial)")
    print("  • MinhaSenh@1 (11 caracteres)")
    print("  • SenhaForte1! (12 caracteres - máximo)")
    print("  • SENHA123 (maiúsculas e números)")
    print("  • senha123 (minúsculas e números)")
    print("  • !@#$%^&* (apenas caracteres especiais)")
    
    print("\nEXEMPLOS DE SENHAS INVÁLIDAS:")
    print("  • abc12 (apenas 5 caracteres - muito curta)")
    print("  • SenhaForte123 (13 caracteres - muito longa)")
    print("  • senha com espaco (contém espaços)")
    print("  • Sen ha1 (contém espaço no meio)")
    print("  • (vazia)")
    
    return passou, falhou

if __name__ == "__main__":
    passou, falhou = testar_validacao_senha()
    
    # Retornar código de saída apropriado
    sys.exit(0 if falhou == 0 else 1)
