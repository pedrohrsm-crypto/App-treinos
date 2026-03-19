# 🌸 Guia Prático - Uso da Funcionalidade de Ciclo Menstrual

## 🚀 Início Rápido

### Exemplo Completo de Uso Interativo

```bash
python training_planner.py
```

### Fluxo de Cadastro:

```
=======================================================================
SISTEMA DE GERAÇÃO DE PLANILHAS DE TREINAMENTO ESPORTIVO
=======================================================================

Nome do atleta: Juliana Silva
Idade: 28
Peso (kg): 58
Altura (cm): 165
Gênero (Masculino/Feminino): Feminino    ← NOVO CAMPO
Esporte: Corrida
Quantos dias por semana pode treinar? (2-7): 5
Distância da prova: 10K
Limiar de Lactato (bpm): 172
VO2 Max (ml/kg/min): 48

O atleta possui algum problema de saúde? (s/n): n

=======================================================================
INFORMAÇÕES SOBRE CICLO MENSTRUAL                      ← NOVA SEÇÃO
=======================================================================

A IA pode ajustar os treinos baseado na fase do ciclo menstrual.
Isso ajuda a otimizar performance e prevenir overtraining.

Deseja informar a fase do ciclo menstrual? (s/n): s

Fases do ciclo menstrual:
1. Menstrual (Dias 1-5) - Período menstrual
2. Folicular (Dias 6-14) - Fase ideal para treinos intensos
3. Ovulatória (Dias 13-16) - Pico de performance
4. Lútea (Dias 17-28) - Fase pré-menstrual

Em qual fase você está atualmente? (1-4): 1

✅ Fase registrada: Menstrual
Os treinos serão ajustados automaticamente pela IA.

=======================================================================
GERANDO PLANO DE TREINAMENTO...
=======================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌸 RECOMENDAÇÕES BASEADAS NO CICLO MENSTRUAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌸 FASE: MENSTRUAL (Dias 1-5 do ciclo)
   Menstruação, baixos níveis hormonais

  • Reduza intensidade e volume em 20-30% se houver desconforto
  • Priorize treinos de baixa/moderada intensidade (Z1-Z2)
  • Alongamentos e yoga podem ajudar com cólicas
  • Hidratação extra é importante (maior perda de fluidos)
  • Considere suplementação de ferro se fluxo for intenso
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Plano de treinamento para Juliana Silva:
Esporte: Corrida - Distância: 10K
Treinos por semana: 5

📅 Segunda - Corrida
   ⏱️  Duração: 30 min
   🎯 Tipo: Recuperação (Z1 - Recuperação)
   📝 Corrida leve e regenerativa | 🌸 Fase menstrual - mantenha conforto

📅 Terça - Corrida
   ⏱️  Duração: 45 min
   🎯 Tipo: Base Moderada (Z2 - Aeróbico)
   📝 15min aquec + 10x400m (rec 90s) + 10min desaq | 🌸 AJUSTADO: Intensidade reduzida (fase menstrual)

📅 Quarta - Corrida
   ⏱️  Duração: 33 min
   🎯 Tipo: Base (Z2 - Aeróbico)
   📝 Corrida contínua em ritmo confortável | 🌸 AJUSTADO: Volume reduzido (fase menstrual)

📅 Quinta - Corrida
   ⏱️  Duração: 37 min
   🎯 Tipo: Tempo Run (Z4 - Limiar)
   📝 15min aquec + 20min no limiar + 15min desaq | 🌸 Fase menstrual - mantenha conforto

📅 Domingo - Corrida
   ⏱️  Duração: 67 min
   🎯 Tipo: Long Run (Z2 - Aeróbico)
   📝 Corrida longa em ritmo controlado | 🌸 AJUSTADO: Volume reduzido (fase menstrual)

Deseja exportar para Excel? (s/n): s

✅ Planilha exportada com sucesso: Plano_Treinamento_Juliana_Silva_20260312_143522.xlsx
```

---

## 📊 Comparação de Treinos por Fase

### Exemplo: Corrida 10K - 5 dias/semana

| Fase | Volume Total/Semana | Intensidade Máxima | Recuperação |
|------|-------------------|-------------------|-------------|
| **Menstrual** | 212 min (75%) | Z2-Z3 | +30% |
| **Folicular** | 280 min (100%) | Z4-Z5 | Normal |
| **Ovulatória** | 280 min (100%) | Z4-Z5 | Normal |
| **Lútea** | 252 min (90%) | Z2-Z4 | +20% |

---

## 🎯 Casos de Uso Específicos

### Caso 1: Atleta Competitiva - Planejamento de Prova

**Situação**: Competição importante em 4 semanas

**Estratégia com IA de Ciclo**:
```
Semana 1 (Fase Menstrual):
  → Volume reduzido, foco em recuperação
  → 75% do volume normal
  
Semana 2 (Fase Folicular):
  → SEMANA CHAVE! Treinos intensos
  → 100% do volume, Z4-Z5
  → Intervalados, VO2max, força
  
Semana 3 (Fase Ovulatória):
  → Simulação de prova
  → Performance máxima
  → Teste de ritmo
  
Semana 4 (Fase Lútea):
  → Taper/Polimento
  → Volume reduzido naturalmente
  → Dia da prova próximo ao fim da fase lútea
```

### Caso 2: Iniciante - Construção de Base

**Situação**: Primeira meia maratona em 3 meses

**Estratégia**:
```
Fase Menstrual:
  ✓ Foco em corridas fáceis Z1-Z2
  ✓ Caminhadas quando necessário
  ✓ Yoga e alongamento
  
Fase Folicular:
  ✓ Aumentar volume gradualmente
  ✓ Incluir 1 treino de velocidade
  ✓ Long run progressivo
  
Fase Ovulatória:
  ✓ Long run mais longo da semana
  ✓ Testar ritmo de prova
  
Fase Lútea:
  ✓ Manter base aeróbica
  ✓ Reduzir expectativas se houver fadiga
  ✓ Priorizar qualidade vs quantidade
```

### Caso 3: Triatleta - Múltiplas Modalidades

**Situação**: Triathlon Olímpico

**Ajustes por Modalidade**:
```
Fase Menstrual:
  Natação: -30% volume, evitar intensidade alta
  Ciclismo: Manter volume, reduzir FTP work
  Corrida: -30% volume, evitar intervalados
  
Fase Folicular:
  Natação: Volume normal + trabalho técnico intenso
  Ciclismo: Sweet spot, FTP intervals
  Corrida: Intervalados de pista, VO2max
  
Fase Ovulatória:
  Natação: Testes de tempo
  Ciclismo: Long rides com simulação
  Corrida: Brick workouts intensos
  
Fase Lútea:
  Natação: Volume moderado, técnica
  Ciclismo: Base aeróbica, evitar sprints
  Corrida: Tempo runs moderados
```

---

## 📈 Resultados Esperados

### Benefícios Imediatos (1-2 meses):
- ✅ Redução de fadiga excessiva
- ✅ Melhor recuperação entre treinos
- ✅ Menos sintomas de overtraining
- ✅ Maior consistência nos treinos

### Benefícios a Médio Prazo (3-6 meses):
- ✅ Melhora significativa de performance
- ✅ Redução de lesões
- ✅ Melhor compreensão do próprio corpo
- ✅ Otimização de periodização

### Benefícios a Longo Prazo (6+ meses):
- ✅ Performance peak em competições
- ✅ Saúde hormonal otimizada
- ✅ Carreira esportiva mais sustentável
- ✅ Relação saudável com treinamento

---

## 🔄 Ajustando ao Longo do Tempo

### Mês 1: Aprendizado
```
Objetivo: Entender como seu corpo responde em cada fase
Ação: Registre como se sente em cada treino
```

### Mês 2-3: Refinamento
```
Objetivo: Ajustar recomendações da IA
Ação: Comunique ao treinador se ajustes são suficientes/excessivos
```

### Mês 4+: Otimização
```
Objetivo: Performance máxima
Ação: Planeje competições em fases favoráveis (folicular/ovulatória)
```

---

## 💡 Dicas Profissionais

### Para Atletas:

1. **Registre Sintomas**
   - Cólicas, fadiga, humor
   - Qualidade do sono
   - Apetite e cravings
   - Performance percebida

2. **Seja Flexível**
   - Nem todos os ciclos são iguais
   - Escute seu corpo acima da IA
   - Ajuste conforme necessário

3. **Nutrição Adaptada**
   - Fase Menstrual: ↑ Ferro, ↑ Hidratação
   - Fase Folicular: ↑ Proteína (anabolismo)
   - Fase Lútea: ↑ Carboidratos (metabolismo acelerado)

### Para Treinadores:

1. **Comunicação Aberta**
   - Crie ambiente confortável para discussão
   - Não assuma que todas as atletas querem compartilhar

2. **Individualização**
   - Algumas atletas são muito afetadas
   - Outras quase não sentem diferença
   - Ajuste as recomendações da IA conforme feedback

3. **Planejamento Estratégico**
   - Marque competições importantes na fase folicular/ovulatória
   - Use fase menstrual para recuperação/regeneração
   - Aproveite fase lútea para trabalho aeróbico

---

## ❓ FAQ

**P: Preciso informar a fase menstrual toda semana?**
R: Não, você pode pular esta etapa. Os treinos serão gerados normalmente.

**P: E se eu usar anticoncepcional?**
R: Anticoncepcionais alteram o ciclo hormonal natural. Consulte seu médico para orientações específicas.

**P: Posso fazer treinos intensos na fase menstrual?**
R: Sim, se você se sentir bem! As recomendações são diretrizes, não regras absolutas.

**P: Como sei em qual fase estou?**
R: Conte a partir do primeiro dia da menstruação. Apps de rastreamento menstrual ajudam.

**P: Os ajustes são muito conservadores/agressivos para mim.**
R: Informe ao seu treinador para ajustar manualmente. Cada atleta é única.

---

## 📞 Próximos Passos

1. **Experimente**: Execute `python exemplos.py` opção 5
2. **Teste**: Execute `python teste_ia_saude.py`
3. **Use**: Execute `python training_planner.py` e cadastre-se
4. **Feedback**: Registre sua experiência após 1 mês

---

**Boa sorte com seus treinos otimizados! 🌸🏃‍♀️💪**
