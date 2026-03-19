"""
Script de teste integrado para validação de senha no cadastro
Testa o fluxo completo com o banco de dados
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.database import db_manager
import os

def limpar_banco_teste():
    """Remove banco de dados de teste se existir."""
    db_path = ROOT_DIR / 'data' / 'app_treinos.db'
    if db_path.exists():
        print(f"🗑️  Removendo banco de dados de teste existente...")
        os.remove(db_path)
        print(f"✅ Banco removido\n")

def testar_cadastro_com_senha():
    """Testa cadastro de usuários com diferentes senhas."""
    print("\n" + "="*70)
    print("TESTE DE CADASTRO COM VALIDAÇÃO DE SENHA")
    print("="*70 + "\n")
    
    # Casos de teste
    testes = [
        # (nome, cpf, cref, senha, deveria_passar, motivo)
        ("Usuário 1", "11111111111", "111111-G/SP", "abc123", True, "senha válida (6 chars)"),
        ("Usuário 2", "22222222222", "222222-G/SP", "Senha@1", True, "senha válida (7 chars com especial)"),
        ("Usuário 3", "33333333333", "333333-G/SP", "SenhaForte1!", True, "senha válida (12 chars - máximo)"),
        ("Usuário 4", "44444444444", "444444-G/SP", "abc12", False, "senha muito curta (5 chars)"),
        ("Usuário 5", "55555555555", "555555-G/SP", "SenhaForte123", False, "senha muito longa (13 chars)"),
        ("Usuário 6", "66666666666", "666666-G/SP", "senha espaco", False, "senha com espaços"),
        ("Usuário 7", "77777777777", "777777-G/SP", "MAIUSC1", True, "senha válida (maiúsculas)"),
        ("Usuário 8", "88888888888", "888888-G/SP", "!@#$%^&*", True, "senha válida (especiais)"),
    ]
    
    passou = 0
    falhou = 0
    
    for nome, cpf, cref, senha, deveria_passar, motivo in testes:
        # Validar senha primeiro (mesma lógica do RegisterScreen)
        tem_espaco = ' ' in senha
        tamanho_valido = 6 <= len(senha) <= 12
        senha_valida = not tem_espaco and tamanho_valido
        
        if not senha_valida:
            # Senha inválida - não deve cadastrar
            if deveria_passar:
                print(f"❌ FALHOU | {nome:12} | senha '{senha}' | {motivo}")
                print(f"           Esperado: deveria passar, mas foi rejeitada na validação")
                falhou += 1
            else:
                print(f"✅ PASSOU | {nome:12} | senha '{senha}' | {motivo}")
                print(f"           Rejeitada corretamente na validação")
                passou += 1
            continue
        
        # Tentar cadastrar no banco
        sucesso, mensagem = db_manager.cadastrar_usuario(cpf, cref, nome, senha, "")
        
        # Verificar resultado
        if sucesso == deveria_passar:
            status = "✅ PASSOU"
            passou += 1
            if sucesso:
                print(f"{status} | {nome:12} | senha '{senha}' | {motivo}")
                print(f"           Cadastrado com sucesso no banco")
            else:
                print(f"{status} | {nome:12} | senha '{senha}' | {motivo}")
                print(f"           Rejeitado corretamente: {mensagem}")
        else:
            status = "❌ FALHOU"
            falhou += 1
            print(f"{status} | {nome:12} | senha '{senha}' | {motivo}")
            print(f"           Esperado: {'sucesso' if deveria_passar else 'falha'}")
            print(f"           Obtido: {'sucesso' if sucesso else 'falha'} - {mensagem}")
        
        print()
    
    # Listar usuários cadastrados
    print("="*70)
    print("USUÁRIOS CADASTRADOS NO BANCO:")
    print("="*70)
    usuarios = db_manager.listar_usuarios()
    if usuarios:
        for usuario in usuarios:
            print(f"👤 {usuario['nome']:20} | CPF: {usuario['cpf']} | CREF: {usuario['cref']}")
    else:
        print("(Nenhum usuário cadastrado)")
    
    # Resumo
    print("\n" + "="*70)
    print(f"RESUMO: {passou} testes passaram, {falhou} testes falharam")
    print("="*70 + "\n")
    
    return passou, falhou

if __name__ == "__main__":
    # Não limpar banco (pode estar em uso)
    # limpar_banco_teste()
    
    print("⚠️  AVISO: Usando banco de dados existente")
    print("          Alguns CPFs/CREFs podem já estar cadastrados\n")
    
    # Executar testes
    passou, falhou = testar_cadastro_com_senha()
    
    # Retornar código de saída apropriado
    sys.exit(0 if falhou == 0 else 1)
