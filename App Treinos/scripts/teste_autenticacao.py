"""
Script de Teste - Fluxo de Cadastro e Login
============================================

Teste automatizado do sistema de autenticação.
"""

import sys
from pathlib import Path

# Adicionar diretórios ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.database import db_manager

print("=" * 60)
print("TESTE DO SISTEMA DE AUTENTICAÇÃO")
print("=" * 60)

# 1. Verificar banco de dados
print("\n1️⃣ Verificando banco de dados...")
usuarios = db_manager.listar_usuarios()
print(f"   ✅ {len(usuarios)} usuários cadastrados")

# 2. Cadastrar usuário de teste
print("\n2️⃣ Cadastrando usuário de teste...")
sucesso, msg = db_manager.cadastrar_usuario(
    cpf="12345678901",
    cref="123456-G/SP",
    nome="João Silva",
    senha="senha123",
    email="joao@teste.com"
)

if sucesso:
    print(f"   ✅ {msg}")
else:
    print(f"   ⚠️ {msg}")

# 3. Listar usuários novamente
print("\n3️⃣ Listando usuários cadastrados...")
usuarios = db_manager.listar_usuarios()
for user in usuarios:
    print(f"   👤 {user['nome']} - CPF: {user['cpf']} - CREF: {user['cref']}")

# 4. Testar autenticação
print("\n4️⃣ Testando autenticação...")

# Teste com CPF
print("\n   Teste 1: Login com CPF correto")
sucesso, usuario = db_manager.autenticar_usuario("12345678901", "senha123")
if sucesso:
    print(f"   ✅ Login bem-sucedido! Bem-vindo, {usuario['nome']}")
else:
    print("   ❌ Falha no login")

# Teste com senha errada
print("\n   Teste 2: Login com senha incorreta")
sucesso, usuario = db_manager.autenticar_usuario("12345678901", "senhaerrada")
if sucesso:
    print("   ❌ ERRO: Login deveria ter falhado!")
else:
    print("   ✅ Login bloqueado corretamente")

# Teste com CREF
print("\n   Teste 3: Login com CREF")
sucesso, usuario = db_manager.autenticar_usuario("123456-G/SP", "senha123")
if sucesso:
    print(f"   ✅ Login bem-sucedido! Bem-vindo, {usuario['nome']}")
else:
    print("   ❌ Falha no login")

# 5. Testar admin
print("\n5️⃣ Testando acesso administrativo...")
if db_manager.autenticar_admin("admin", "adminDB"):
    print("   ✅ Acesso admin autorizado")
else:
    print("   ❌ Acesso admin negado")

print("\n" + "=" * 60)
print("TESTE CONCLUÍDO!")
print("=" * 60)

print("\n📋 INSTRUÇÕES PARA TESTAR NA GUI:")
print("\n1. Execute: python gui/main_gui.py")
print("\n2. Aguarde a splash screen")
print("\n3. Na tela de login, clique em 'Criar Nova Conta'")
print("\n4. Preencha:")
print("   - Nome Completo: Seu Nome")
print("   - CPF: 98765432109")
print("   - CREF: 654321-G/RJ")
print("   - Senha: teste123")
print("\n5. Clique em '✅ Registrar'")
print("\n6. Veja a mensagem: 'Usuário cadastrado com sucesso!'")
print("\n7. Na tela de login:")
print("   - CPF/CREF: 98765432109")
print("   - Senha: teste123")
print("\n8. Clique em 'Entrar'")
print("\n9. Dashboard será exibido com seu nome!")
print("\n" + "=" * 60)
