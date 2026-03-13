"""
Exemplo interativo mostrando os dois fluxos de configuração de semanas
"""

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                   SISTEMA DE PLANEJAMENTO DE TREINAMENTO                       ║
║                    📅 DOIS MODOS DE CONFIGURAÇÃO 📅                            ║
╚════════════════════════════════════════════════════════════════════════════════╝

Este exemplo mostra como o sistema oferece DOIS MODOS para configurar o período
de treinamento, garantindo flexibilidade para diferentes situações:

""")

print("═"*90)
print("MODO 1: INFORMAR NÚMERO DE SEMANAS DIRETAMENTE")
print("═"*90)
print("""
👤 QUANDO USAR:
   • Você quer planejar as "próximas X semanas" (sem data específica)
   • A prova ainda não tem data definida
   • Você prefere trabalhar com período flexível
   • Está fazendo preparação base (sem evento confirmado)

💬 FLUXO:
   ═══════════════════════════════════════════════════════════════════
   📅 CONFIGURAÇÃO DO PERÍODO DE TREINAMENTO
   ═══════════════════════════════════════════════════════════════════
   
   Você sabe quantas semanas faltam até a prova? (s/n): s
   
   Quantas semanas faltam até a prova? (1-52): 16
   
   ✅ Configurado: 16 semanas de treinamento

✨ RESULTADO:
   • Sistema cria periodização para 16 semanas
   • Distribuição automática: Base (5) + Resistência (4) + Velocidade (3) + 
     Potência (2) + Polimento (2)
   • Semanas de recuperação: 4, 8, 12
   • Total de treinos: ~80 (16 semanas x 5 dias)
""")

print("\n" + "═"*90)
print("MODO 2: CALCULAR AUTOMATICAMENTE PELA DATA DA PROVA")
print("═"*90)
print("""
👤 QUANDO USAR:
   • Você sabe a DATA EXATA da prova
   • Quer precisão absoluta (não aproximações)
   • Prefere informar data ao invés de contar semanas
   • Quer que o plano se ajuste automaticamente com o tempo

💬 FLUXO:
   ═══════════════════════════════════════════════════════════════════
   📅 CONFIGURAÇÃO DO PERÍODO DE TREINAMENTO
   ═══════════════════════════════════════════════════════════════════
   
   Você sabe quantas semanas faltam até a prova? (s/n): n
   
   💡 Vamos calcular automaticamente baseado na data da prova!
   
   Qual a data da prova? (DD/MM/AAAA): 15/09/2026
   
   ──────────────────────────────────────────────────────────────────
   ✅ Cálculo realizado com sucesso!
      📅 Data da prova: 15/09/2026 (Tuesday)
      📊 Dias até a prova: 186 dias
      📆 Semanas de treinamento: 27 semanas
   ──────────────────────────────────────────────────────────────────

✨ RESULTADO:
   • Sistema calcula AUTOMATICAMENTE: 186 dias ÷ 7 = 26.57 → 27 semanas
   • Arredondamento para CIMA garante tempo suficiente
   • Periodização criada para 27 semanas exatas
   • Distribuição: Base (9) + Resistência (7) + Velocidade (5) + 
     Potência (4) + Polimento (2)
   • Semanas de recuperação: 4, 8, 12, 16, 20, 24
   • Total de treinos: ~135 (27 semanas x 5 dias)
""")

print("\n" + "═"*90)
print("COMPARAÇÃO DOS DOIS MODOS")
print("═"*90)

comparacao = """
┌────────────────────────────┬──────────────────────┬──────────────────────────┐
│      CARACTERÍSTICA        │   MODO 1 (Manual)    │  MODO 2 (Automático)     │
├────────────────────────────┼──────────────────────┼──────────────────────────┤
│ Input do usuário           │ Número de semanas    │ Data da prova (DD/MM/AA) │
│ Precisão                   │ Aproximada           │ Absoluta (timestamp)     │
│ Validação de data passada  │ ❌ Não              │ ✅ Sim                   │
│ Atualização automática     │ ❌ Não              │ ✅ Sim (cada execução)   │
│ Facilidade de lembrar      │ ⭐⭐ Média          │ ⭐⭐⭐ Alta             │
│ Flexibilidade              │ ⭐⭐⭐ Alta         │ ⭐⭐ Média              │
│ Adequado para evento fixo  │ ⭐⭐ Adequado        │ ⭐⭐⭐ Ideal            │
│ Adequado para base geral   │ ⭐⭐⭐ Ideal        │ ⭐⭐ Adequado           │
└────────────────────────────┴──────────────────────┴──────────────────────────┘
"""
print(comparacao)

print("\n" + "═"*90)
print("CENÁRIOS DE USO RECOMENDADOS")
print("═"*90)

cenarios = """
📌 CENÁRIO 1: Maratona de São Paulo confirmada para 15/09/2026
   ✅ RECOMENDADO: Modo 2 (Automático)
   ❓ POR QUÊ: Data fixa, precisão crítica, long-term planning
   
📌 CENÁRIO 2: Preparação base de 12 semanas (sem evento específico)
   ✅ RECOMENDADO: Modo 1 (Manual)
   ❓ POR QUÊ: Período flexível, foco em condicionamento geral

📌 CENÁRIO 3: Ironman Florianópolis em 10/08/2026
   ✅ RECOMENDADO: Modo 2 (Automático)
   ❓ POR QUÊ: Evento importante, necessita periodização exata

📌 CENÁRIO 4: "Quero melhorar meu 10K nos próximos 2 meses"
   ✅ RECOMENDADO: Modo 1 (Manual - 8 semanas)
   ❓ POR QUÊ: Objetivo de prazo, não evento específico

📌 CENÁRIO 5: Prova local daqui a 60 dias (data conhecida)
   ✅ RECOMENDADO: Modo 2 (Automático)
   ❓ POR QUÊ: Evita erro de cálculo (60 dias = 8.57 semanas → 9)
"""
print(cenarios)

print("\n" + "═"*90)
print("DICAS PARA ESCOLHER O MODO CERTO")
print("═"*90)

dicas = """
💡 Use MODO 2 (Automático) se:
   ✓ Você tem a data exata do evento
   ✓ O evento é fixo e não vai mudar
   ✓ Você quer precisão máxima
   ✓ Prefere informar data (mais intuitivo)
   ✓ Quer que o plano se atualize automaticamente

💡 Use MODO 1 (Manual) se:
   ✓ O evento ainda não tem data definida
   ✓ Você está fazendo preparação base
   ✓ Prefere trabalhar com "blocos de semanas"
   ✓ Quer flexibilidade para ajustar depois
   ✓ Está planejando múltiplos eventos

⚠️  ATENÇÃO: Ambos os modos geram a mesma qualidade de periodização!
   A única diferença é COMO você informa o período de tempo.
"""
print(dicas)

print("\n" + "═"*90)
print("🎯 CONCLUSÃO")
print("═"*90)
print("""
O sistema oferece DOIS MODOS para atender diferentes necessidades:

🎯 MODO 1 (Manual): Máxima flexibilidade para planejamento aberto
🎯 MODO 2 (Automático): Máxima precisão para eventos com data fixa

💪 RESULTADO FINAL: Plano de treinamento personalizado e periodizado
   independente do modo escolhido!

""")

print("═"*90)
print("✅ SISTEMA COMPLETO E PRONTO PARA USO!")
print("═"*90 + "\n")
