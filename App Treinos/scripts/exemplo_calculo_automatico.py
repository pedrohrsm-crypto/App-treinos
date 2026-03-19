"""
Exemplo de uso da funcionalidade de cálculo automático de semanas
Demonstra como o sistema calcula automaticamente o período de treinamento
baseado na data da prova.
"""

from training_planner import calcular_semanas_ate_prova
from datetime import datetime, timedelta

print("\n" + "═"*80)
print("📅 DEMONSTRAÇÃO: CÁLCULO AUTOMÁTICO DE SEMANAS ATÉ A PROVA")
print("═"*80)

print("\n💡 CONTEXTO:")
print("-"*80)
print("O atleta não sabe quantas semanas faltam até a prova,")
print("mas sabe a DATA EXATA do evento. O sistema calcula automaticamente!")
print("-"*80)

# Cenário 1: Maratona daqui a 6 meses
print("\n📌 CENÁRIO 1: Maratona de São Paulo")
print("─"*80)
data_maratona = (datetime.now() + timedelta(days=180)).strftime('%d/%m/%Y')
print(f"🏃 Atleta: João Silva")
print(f"📅 Data da prova: {data_maratona}")
print(f"🏁 Evento: Maratona de São Paulo")

semanas_maratona = calcular_semanas_ate_prova(data_maratona)
dias_maratona = (datetime.strptime(data_maratona, '%d/%m/%Y') - datetime.now()).days

print(f"\n✅ CÁLCULO AUTOMÁTICO:")
print(f"   • Dias até a prova: {dias_maratona} dias")
print(f"   • Semanas de treinamento: {semanas_maratona} semanas")
print(f"   • Periodização recomendada: 5 fases completas")
print(f"   • Semanas de recuperação: {semanas_maratona // 4} semanas")

# Cenário 2: Ironman daqui a 5 meses
print("\n📌 CENÁRIO 2: Ironman Florianópolis")
print("─"*80)
data_ironman = (datetime.now() + timedelta(days=150)).strftime('%d/%m/%Y')
print(f"🏊‍♂️🚴‍♂️🏃 Atleta: Maria Oliveira")
print(f"📅 Data da prova: {data_ironman}")
print(f"🏁 Evento: Ironman Florianópolis")

semanas_ironman = calcular_semanas_ate_prova(data_ironman)
dias_ironman = (datetime.strptime(data_ironman, '%d/%m/%Y') - datetime.now()).days

print(f"\n✅ CÁLCULO AUTOMÁTICO:")
print(f"   • Dias até a prova: {dias_ironman} dias")
print(f"   • Semanas de treinamento: {semanas_ironman} semanas")
print(f"   • Periodização recomendada: 5 fases completas")
print(f"   • Total de treinos estimados: {semanas_ironman * 6} treinos (3 modalidades)")

# Cenário 3: 10K daqui a 2 meses
print("\n📌 CENÁRIO 3: Corrida 10K Local")
print("─"*80)
data_10k = (datetime.now() + timedelta(days=60)).strftime('%d/%m/%Y')
print(f"🏃‍♀️ Atleta: Ana Costa")
print(f"📅 Data da prova: {data_10k}")
print(f"🏁 Evento: Corrida de Rua 10K")

semanas_10k = calcular_semanas_ate_prova(data_10k)
dias_10k = (datetime.strptime(data_10k, '%d/%m/%Y') - datetime.now()).days

print(f"\n✅ CÁLCULO AUTOMÁTICO:")
print(f"   • Dias até a prova: {dias_10k} dias")
print(f"   • Semanas de treinamento: {semanas_10k} semanas")
print(f"   • Periodização recomendada: 3 fases (velocidade + potência + polimento)")
print(f"   • Total de treinos estimados: {semanas_10k * 5} treinos")

# Cenário 4: Data muito próxima (1 semana)
print("\n📌 CENÁRIO 4: Prova Muito Próxima")
print("─"*80)
data_proxima = (datetime.now() + timedelta(days=6)).strftime('%d/%m/%Y')
print(f"🏃 Atleta: Carlos Mendes")
print(f"📅 Data da prova: {data_proxima}")
print(f"🏁 Evento: Meia Maratona (sem tempo para treinar)")

semanas_proxima = calcular_semanas_ate_prova(data_proxima)
dias_proxima = (datetime.strptime(data_proxima, '%d/%m/%Y') - datetime.now()).days

print(f"\n✅ CÁLCULO AUTOMÁTICO:")
print(f"   • Dias até a prova: {dias_proxima} dias")
print(f"   • Semanas de treinamento: {semanas_proxima} semana")
print(f"   • ⚠️  ATENÇÃO: Tempo insuficiente para periodização completa")
print(f"   • Recomendação: Foco em polimento/taper apenas")

# Comparação: Manual vs Automático
print("\n" + "═"*80)
print("📊 VANTAGENS DO CÁLCULO AUTOMÁTICO:")
print("═"*80)
print("✅ Precisão absoluta (não depende do cálculo mental do atleta)")
print("✅ Considera a data exata (não arredondamentos aproximados)")
print("✅ Valida automaticamente se a data não está no passado")
print("✅ Arredonda para cima (garante tempo suficiente)")
print("✅ Atualiza automaticamente conforme o tempo passa")
print("✅ Evita erros de contagem de semanas")

print("\n💡 FLUXO NO APLICATIVO:")
print("─"*80)
print("1. Sistema pergunta: 'Você sabe quantas semanas faltam até a prova?'")
print("2. Se NÃO souber → Pede a data da prova (DD/MM/AAAA)")
print("3. Sistema calcula automaticamente usando timestamp")
print("4. Mostra resultado detalhado (data, dias, semanas)")
print("5. Gera periodização ideal baseada no cálculo")

print("\n" + "═"*80)
print("✅ DEMONSTRAÇÃO CONCLUÍDA!")
print("═"*80 + "\n")
