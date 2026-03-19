"""
Testes para a função calcular_semanas_ate_prova()
"""

from training_planner import calcular_semanas_ate_prova
from datetime import datetime, timedelta

print("\n" + "="*70)
print("🧪 TESTES DA FUNÇÃO calcular_semanas_ate_prova()")
print("="*70)

# Teste 1: Data futura válida (12 semanas)
print("\n📋 Teste 1: Data futura válida (84 dias = 12 semanas)")
print("-"*70)
data_futura_1 = (datetime.now() + timedelta(days=84)).strftime('%d/%m/%Y')
print(f"Data de hoje: {datetime.now().strftime('%d/%m/%Y')}")
print(f"Data da prova: {data_futura_1}")
semanas_1 = calcular_semanas_ate_prova(data_futura_1)
print(f"Resultado: {semanas_1} semanas")
print(f"Esperado: 12 semanas")
print(f"Status: {'✅ PASSOU' if semanas_1 == 12 else '❌ FALHOU'}")

# Teste 2: Data muito distante (40 semanas)
print("\n📋 Teste 2: Data muito distante (280 dias = 40 semanas)")
print("-"*70)
data_futura_2 = (datetime.now() + timedelta(days=280)).strftime('%d/%m/%Y')
print(f"Data da prova: {data_futura_2}")
semanas_2 = calcular_semanas_ate_prova(data_futura_2)
print(f"Resultado: {semanas_2} semanas")
print(f"Esperado: 40 semanas")
print(f"Status: {'✅ PASSOU' if semanas_2 == 40 else '❌ FALHOU'}")

# Teste 3: Próxima semana (5 dias = 1 semana)
print("\n📋 Teste 3: Próxima semana (5 dias → arredonda para 1 semana)")
print("-"*70)
data_futura_3 = (datetime.now() + timedelta(days=5)).strftime('%d/%m/%Y')
print(f"Data da prova: {data_futura_3}")
semanas_3 = calcular_semanas_ate_prova(data_futura_3)
print(f"Resultado: {semanas_3} semanas")
print(f"Esperado: 1 semana (arredondado para cima)")
print(f"Status: {'✅ PASSOU' if semanas_3 == 1 else '❌ FALHOU'}")

# Teste 4: Data no passado (deve lançar exceção)
print("\n📋 Teste 4: Data no passado (deve lançar ValueError)")
print("-"*70)
try:
    calcular_semanas_ate_prova('01/01/2020')
    print("❌ FALHOU: Deveria ter lançado exceção!")
except ValueError as e:
    print(f"✅ PASSOU: Exceção capturada corretamente")
    print(f"   Mensagem: {e}")

# Teste 5: Formato de data inválido (deve lançar exceção)
print("\n📋 Teste 5: Formato inválido (deve lançar ValueError)")
print("-"*70)
try:
    calcular_semanas_ate_prova('2026-03-20')
    print("❌ FALHOU: Deveria ter lançado exceção!")
except ValueError as e:
    print(f"✅ PASSOU: Exceção capturada corretamente")
    print(f"   Mensagem: {e}")

# Teste 6: Data de hoje (0 dias → 1 semana mínima)
print("\n📋 Teste 6: Data de hoje (0 dias → mínimo 1 semana)")
print("-"*70)
data_hoje = datetime.now().strftime('%d/%m/%Y')
print(f"Data da prova: {data_hoje}")
semanas_6 = calcular_semanas_ate_prova(data_hoje)
print(f"Resultado: {semanas_6} semanas")
print(f"Esperado: 1 semana (valor mínimo)")
print(f"Status: {'✅ PASSOU' if semanas_6 == 1 else '❌ FALHOU'}")

print("\n" + "="*70)
print("✅ TODOS OS TESTES CONCLUÍDOS!")
print("="*70 + "\n")
