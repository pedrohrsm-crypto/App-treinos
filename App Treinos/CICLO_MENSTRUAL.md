# 🌸 Funcionalidade de Ciclo Menstrual - Sistema de Treinamento

## 📋 Visão Geral

O sistema agora inclui **adaptação inteligente de treinos baseada no ciclo menstrual** para atletas do sexo feminino. Esta funcionalidade utiliza IA para ajustar automaticamente volume, intensidade e tipo de treino conforme a fase do ciclo.

---

## 🆕 Novos Recursos Implementados

### 1. **Coleta de Gênero**
- O sistema agora coleta informações sobre o gênero do atleta (Masculino/Feminino)
- Campo obrigatório durante o cadastro do atleta

### 2. **Coleta de Fase Menstrual** (Opcional - Apenas Feminino)
O sistema oferece 4 fases do ciclo menstrual:
- **Menstrual** (Dias 1-5): Período menstrual
- **Folicular** (Dias 6-14): Pós-menstruação, fase ideal para treinos intensos
- **Ovulatória** (Dias 13-16): Pico de performance
- **Lútea** (Dias 17-28): Fase pré-menstrual

---

## 🤖 Análise de IA por Fase do Ciclo

### Fase Menstrual (Dias 1-5)
**Características**: Menstruação, baixos níveis hormonais

**Recomendações da IA**:
- ✅ Reduza intensidade e volume em 20-30% se houver desconforto
- ✅ Priorize treinos de baixa/moderada intensidade (Z1-Z2)
- ✅ Alongamentos e yoga podem ajudar com cólicas
- ✅ Hidratação extra é importante
- ✅ Considere suplementação de ferro se fluxo for intenso

**Ajustes Automáticos**:
- 📉 Volume: 75% do normal
- 📉 Intensidade: Treinos Z4-Z5 convertidos para Z2-Z3
- ⏱️ Recuperação: +30%

### Fase Folicular (Dias 6-14)
**Características**: Pós-menstruação, estrogênio crescente

**Recomendações da IA**:
- ✅ Fase ideal para treinos de alta intensidade
- ✅ Aproveite para trabalhos de força e potência
- ✅ Ótima fase para intervalados e VO2max
- ✅ Recuperação muscular é mais rápida
- ✅ Tolerância à dor está aumentada

**Ajustes Automáticos**:
- ✅ Volume: 100% (normal)
- ✅ Intensidade: Normal
- ✅ Sem redução de recuperação

### Fase Ovulatória (Dias 13-16)
**Características**: Ovulação, pico de estrogênio

**Recomendações da IA**:
- ✅ Excelente fase para performance máxima
- ✅ Aproveite para testes e treinos chave
- ✅ Força e coordenação estão no auge
- ⚠️ Atenção: ligeiro aumento no risco de lesões ligamentares
- ✅ Aquecimento mais completo é recomendado

**Ajustes Automáticos**:
- ✅ Volume: 100% (normal)
- ✅ Intensidade: Normal
- ⚠️ Atenção extra ao aquecimento

### Fase Lútea (Dias 17-28)
**Características**: Pré-menstrual, progesterona alta

**Recomendações da IA**:
- ⚠️ Possível retenção de líquidos e fadiga
- ⚠️ Reduza intensidade em 10-15% se necessário
- ✅ Priorize treinos aeróbicos de base (Z2)
- ✅ Aumente carboidratos (metabolismo mais acelerado)
- ⚠️ TPM pode afetar motivação - seja flexível
- ✅ Temperatura corporal mais elevada - hidrate-se mais

**Ajustes Automáticos**:
- 📉 Volume: 90% do normal
- 📉 Intensidade: Z5 → Z3, preferência por Z2
- ⏱️ Recuperação: +20%

---

## 📊 Exemplo de Uso

### Cenário: Corredora na Fase Menstrual

**Input**:
```
Nome: Juliana Lima
Gênero: Feminino
Idade: 26 anos
Esporte: Corrida
Distância: 10K
Fase do Ciclo: Menstrual
```

**Output - Treino Original vs Ajustado**:

| Dia | Treino Original | Treino Ajustado (Fase Menstrual) |
|-----|----------------|----------------------------------|
| Terça | Intervalado 60min Z5 | Base Moderada 45min Z2 🌸 |
| Quinta | Tempo Run 50min Z4 | Base 37min Z3 🌸 |
| Domingo | Long Run 90min Z2 | Long Run 67min Z2 🌸 |

**Marcação Visual**: Treinos ajustados recebem o símbolo 🌸

---

## 📁 Exportação Excel

A planilha Excel gerada agora inclui:

### 1. **Aba "Informações do Atleta"**
- Novo campo: **Gênero**
- Novo campo: **Fase do Ciclo Menstrual** (se aplicável)

### 2. **Aba "Recomendações Médicas"**
- Inclui seção específica sobre ciclo menstrual
- Recomendações personalizadas por fase
- Orientações científicas baseadas em fisiologia hormonal

### 3. **Aba "Plano Semanal"**
- Treinos marcados com 🌸 quando ajustados por ciclo menstrual
- Descrição detalhada das modificações aplicadas

---

## 🎯 Benefícios da Funcionalidade

### Para Atletas:
✅ **Performance otimizada** conforme fase hormonal  
✅ **Redução de overtraining** em fases críticas  
✅ **Melhor recuperação** muscular  
✅ **Aproveitamento de fases anabólicas** (folicular/ovulatória)  
✅ **Prevenção de lesões** ligamentares  

### Para Treinadores:
✅ **Periodização científica** baseada em fisiologia hormonal  
✅ **Documentação profissional** das adaptações  
✅ **Diferencial competitivo** no mercado  
✅ **Atendimento personalizado** para atletas femininas  
✅ **Base científica** para decisões de treino  

---

## 📖 Base Científica

As adaptações são baseadas em pesquisas sobre:

1. **Variações hormonais** (estrogênio/progesterona) durante o ciclo
2. **Impacto na força muscular** e recuperação
3. **Temperatura corporal basal** e metabolismo
4. **Retenção de líquidos** e peso
5. **Tolerância à dor** e fadiga
6. **Risco de lesões ligamentares** (pico de estrogênio)

---

## 🔧 Como Usar

### 1. Execute o programa:
```bash
python training_planner.py
```

### 2. Durante o cadastro, informe:
- Gênero: **Feminino**
- Quando perguntado: **Sim** para informar fase menstrual
- Escolha a fase atual: **1-4**

### 3. O sistema automaticamente:
- ✅ Analisa a fase e fornece recomendações
- ✅ Ajusta todos os treinos da semana
- ✅ Marca treinos modificados com 🌸
- ✅ Exporta tudo para Excel com documentação completa

---

## 📝 Exemplos Práticos

### Teste Rápido:
```bash
python exemplos.py
# Escolha opção 5: Corrida (10K) - 🌸 Fase menstrual do ciclo
```

### Teste Completo (4 fases):
```bash
python teste_ia_saude.py
# Executa testes automáticos de todas as 4 fases
```

---

## ⚕️ Disclaimer

Esta funcionalidade fornece **orientações gerais** baseadas em fisiologia do exercício e ciclo menstrual.

**NÃO substitui**:
- Avaliação ginecológica
- Orientação médica personalizada
- Tratamento de condições médicas
- Acompanhamento profissional especializado

Cada atleta é única. Recomenda-se:
- ✅ Consulta com ginecologista esportivo
- ✅ Acompanhamento de nutricionista
- ✅ Avaliação hormonal se necessário
- ✅ Ajustes individualizados conforme resposta

---

## 📊 Estatísticas do Sistema

- **4 fases** do ciclo menstrual mapeadas
- **20+ recomendações** específicas por fase
- **3 níveis** de ajuste (volume, intensidade, recuperação)
- **100% dos treinos** são analisados e ajustados
- **Marcação visual** clara em todos os ajustes

---

## 🏆 Diferenciais

1. **Primeira plataforma** de treino com IA para ciclo menstrual
2. **Base científica sólida** em fisiologia hormonal
3. **Ajustes automáticos** em tempo real
4. **Documentação completa** para atleta e treinador
5. **Interface simples** e intuitiva

---

## 🔄 Atualizações Futuras (Roadmap)

- [ ] Rastreamento automático de ciclo (calendário)
- [ ] Integração com apps de rastreamento menstrual
- [ ] Histórico de treinos por fase
- [ ] Análise de performance vs fase do ciclo
- [ ] Alertas de fase ideal para competições
- [ ] Sugestões nutricionais por fase

---

**Desenvolvido com foco em ciência, personalização e performance feminina!** 🌸🏃‍♀️💪

---

## 📞 Suporte

Para dúvidas sobre esta funcionalidade, consulte:
- [README.md](README.md) - Documentação geral
- [NOVAS_FUNCIONALIDADES.md](NOVAS_FUNCIONALIDADES.md) - Histórico de implementações
- [training_planner.py](training_planner.py) - Código fonte

---

*Última atualização: Março 2026*
