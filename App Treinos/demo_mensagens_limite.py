"""
Demonstração das Mensagens de Limite de Planejamento
Mostra como o sistema responde quando usuário excede 52 semanas
"""
import sys
import io

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "="*90)
print("🛡️ DEMONSTRAÇÃO: MENSAGENS DE LIMITE DE PLANEJAMENTO")
print("="*90)

print("""
O sistema possui um limite de 52 semanas (aproximadamente 1 ano) para planejamento
de treinamento. Quando o usuário tenta exceder esse limite, mensagens claras e
informativas são exibidas.
""")

print("\n" + "─"*90)
print("📌 CENÁRIO 1: Modo Manual - Usuário Informa 60 Semanas")
print("─"*90)

print("""
ENTRADA DO USUÁRIO:
   Você sabe quantas semanas faltam até a prova? (s/n): s
   Quantas semanas faltam até a prova? (1-52): 60

SAÍDA DO SISTEMA:
   ⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠
   ⚠️  LIMITE DE PLANEJAMENTO EXCEDIDO
   ⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠
      Valor informado: 60 semanas
      Limite do sistema: 52 semanas (aproximadamente 1 ano)

   📋 MOTIVO DA LIMITAÇÃO:
      • O sistema foi projetado para periodização de até 1 ano
      • Planejamentos acima de 52 semanas requerem reavaliações periódicas
      • Fatores imprevisíveis aumentam significativamente após 1 ano
      • Recomenda-se criar planos em ciclos anuais

   💡 SUGESTÃO:
      Planeje até a próxima reavaliação (máximo 52 semanas)
      Após esse período, gere um novo plano atualizado.
   ⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠

   Por favor, insira um valor entre 1 e 52 semanas.
""")

print("\n" + "─"*90)
print("📌 CENÁRIO 2: Modo Automático - Data Resulta em 75 Semanas")
print("─"*90)

from datetime import datetime, timedelta

# Calcular uma data daqui a 75 semanas (525 dias)
data_futura = (datetime.now() + timedelta(days=525)).strftime('%d/%m/%Y')
dias_calculados = 525
semanas_calculadas = 75
meses_aproximados = round(75 / 4.33, 1)

print(f"""
ENTRADA DO USUÁRIO:
   Você sabe quantas semanas faltam até a prova? (s/n): n
   Qual a data da prova? (DD/MM/AAAA): {data_futura}

SAÍDA DO SISTEMA:
   ⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠
   ⚠️  LIMITE DE PLANEJAMENTO EXCEDIDO
   ⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠
      📅 Data da prova informada: {data_futura}
      📊 Dias até a prova: {dias_calculados} dias
      📆 Semanas calculadas: {semanas_calculadas} semanas (~{meses_aproximados} meses)
      🚫 Limite do sistema: 52 semanas (aproximadamente 1 ano)

   📋 MOTIVO DA LIMITAÇÃO:
      • O sistema não está capacitado para planejamentos acima de 1 ano
      • Periodização acima de 52 semanas requer acompanhamento profissional contínuo
      • Mudanças fisiológicas e de objetivos são muito prováveis nesse período
      • A ciência do treinamento recomenda ciclos anuais com reavaliações

   💡 OPÇÕES DISPONÍVEIS:
      1. Ajustar para 52 semanas (planejamento até próxima avaliação)
      2. Informar uma data mais próxima (até 1 ano a partir de hoje)
   ⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠

   Deseja usar o limite máximo de 52 semanas? (s/n): s

   ✅ Configurado: 52 semanas de treinamento (máximo permitido)
      Após esse período, recomenda-se gerar um novo plano atualizado.
""")

print("\n" + "─"*90)
print("📌 CENÁRIO 3: Modo Automático - Data Daqui a 2 Anos")
print("─"*90)

# Calcular uma data daqui a 2 anos (730 dias)
data_2_anos = (datetime.now() + timedelta(days=730)).strftime('%d/%m/%Y')
dias_2_anos = 730
semanas_2_anos = 105
meses_2_anos = round(105 / 4.33, 1)

print(f"""
ENTRADA DO USUÁRIO:
   Qual a data da prova? (DD/MM/AAAA): {data_2_anos}

SAÍDA DO SISTEMA:
   ⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠
   ⚠️  LIMITE DE PLANEJAMENTO EXCEDIDO
   ⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠
      📅 Data da prova informada: {data_2_anos}
      📊 Dias até a prova: {dias_2_anos} dias
      📆 Semanas calculadas: {semanas_2_anos} semanas (~{meses_2_anos} meses)
      🚫 Limite do sistema: 52 semanas (aproximadamente 1 ano)

   📋 MOTIVO DA LIMITAÇÃO:
      • O sistema não está capacitado para planejamentos acima de 1 ano
      • Periodização acima de 52 semanas requer acompanhamento profissional contínuo
      • Mudanças fisiológicas e de objetivos são muito prováveis nesse período
      • A ciência do treinamento recomenda ciclos anuais com reavaliações

OBSERVAÇÃO: Neste caso, a data está MUITO além do limite (2 anos).
O usuário deveria informar uma data mais próxima ou planejar em ciclos anuais.
""")

print("\n" + "-"*90)
print("RESUMO DAS MENSAGENS DE LIMITE")
print("="*90)

print("""
✅ INFORMAÇÕES FORNECIDAS AO USUÁRIO:

1. 📏 CLAREZA DO LIMITE:
   • Valor/data informado vs limite do sistema
   • Cálculo exato (dias, semanas, meses aproximados)
   
2. 📋 JUSTIFICATIVA TÉCNICA:
   • Sistema projetado para até 1 ano
   • Necessidade de reavaliações periódicas
   • Fatores imprevisíveis em longo prazo
   • Recomendação científica de ciclos anuais
   
3. 💡 OPÇÕES PRÁTICAS:
   • Usar limite de 52 semanas (com explicação)
   • Informar data mais próxima
   • Planejar em ciclos
   
4. 🎯 ORIENTAÇÃO PROFISSIONAL:
   • Gerar novos planos após 52 semanas
   • Acompanhamento contínuo recomendado
   • Adequação às mudanças fisiológicas
""")

print("\n" + "─"*90)
print("🔍 MOTIVOS CIENTÍFICOS DO LIMITE DE 52 SEMANAS")
print("─"*90)

print("""
1️⃣ FISIOLOGIA DO TREINAMENTO:
   • Adaptações máximas ocorrem em ciclos de 8-12 meses
   • Após 1 ano, necessita reavaliação de capacidades
   • Limiares (lactato, VO2max) mudam significativamente

2️⃣ PERIODIZAÇÃO ESPORTIVA:
   • Modelos clássicos (Matveev, Bompa) usam macrociclos anuais
   • Mesociclos são reavaliados a cada 4-12 semanas
   • Planejamento >1 ano requer adaptações dinâmicas

3️⃣ FATORES PRÁTICOS:
   • Lesões, doenças, mudanças de vida são imprevisíveis
   • Objetivos do atleta podem mudar
   • Condições de treinamento variam (clima, equipamentos)
   • Disponibilidade de tempo pode se alterar

4️⃣ RECOMENDAÇÃO PROFISSIONAL:
   • Treinadores reavaliam atletas a cada 3-6 meses
   • Testes físicos periódicos são essenciais
   • Ajustes contínuos baseados em performance real
   • Planos estáticos >1 ano são inadequados
""")

print("\n" + "="*90)
print("MENSAGENS DE SISTEMA IMPLEMENTADAS COM SUCESSO!")
print("="*90)
print("""
O sistema agora fornece mensagens claras, informativas e profissionais
quando o usuário tenta exceder o limite de 52 semanas, seja no modo
manual ou no modo automático por data.
""")
print("="*90 + "\n")
