# Sistema de Geração de Planilhas de Treinamento Esportivo

## 📋 Descrição

Sistema completo para criação de planilhas de treinamento personalizadas para atletas de **Triathlon**, **Corrida**, **Natação** e **Ciclismo**, com **inteligência artificial integrada** para adequação de treinos baseados em condições de saúde.

## ✨ Funcionalidades

- ✅ Coleta completa de dados do atleta (idade, peso, altura, esporte, disponibilidade)
- ✅ **Análise de saúde com IA**: Coleta detalhada de problemas ortopédicos e sistêmicos
- ✅ **Adequações automáticas de treino**: Sistema inteligente que ajusta treinos baseado em:
  - Lesões ortopédicas (joelho, ombro, lombar, tornozelo, quadril, etc.)
  - Problemas sistêmicos (diabetes, asma, hipertensão)
  - Gravidade e membro específico afetado
- ✅ Personalização baseada em:
  - Distância da prova
  - Limiar de lactato e VO2 Max
  - IMC e dados antropométricos
  - Dias disponíveis para treino
- ✅ **Recomendações médicas personalizadas** por IA
- ✅ Geração automática de treinos semanais
- ✅ Cálculo de zonas de treinamento
- ✅ Exportação para Excel com até 5 abas
- ✅ Interface amigável via terminal

## 🤖 Sistema de Inteligência Artificial

O sistema possui um **HealthAdvisor** que funciona como uma IA especializada em medicina esportiva:

### Análise Ortopédica Detalhada
- Identifica a região específica afetada (ex: joelho_direito, ombro_esquerdo)
- Fornece recomendações personalizadas por tipo de lesão
- Ajusta automaticamente volume e intensidade dos treinos
- Sugere alternativas seguras por modalidade

### Condições Sistêmicas Suportadas
- **Diabetes**: Orientações sobre monitoramento de glicemia e ajustes de insulina
- **Asma**: Recomendações sobre aquecimento e ambiente de treino
- **Hipertensão**: Adaptações de intensidade e monitoramento
- **Problemas cardíacos**: Alertas críticos e restrições

### Adequações Inteligentes
- **Volume reduzido**: 20-50% dependendo da lesão
- **Intensidade ajustada**: Conversão de treinos intensos para base
- **Substituições seguras**: Alternativas de baixo impacto
- **Alertas visuais**: Marcação ⚕️ em treinos adaptados

## 🏃 Modalidades Suportadas

### Triathlon
- Sprint
- Olímpico
- Meio Ironman
- Ironman

### Corrida
- 5K
- 10K
- Meia Maratona
- Maratona

### Natação
- 1500m
- 3000m
- 5000m

### Ciclismo
- 40K
- 80K
- 160K

## 📊 Estrutura da Planilha Exportada

O arquivo Excel gerado contém até **5 abas**:

1. **Informações do Atleta**: Dados completos incluindo IMC
2. **Plano Semanal**: Treinos detalhados (com ajustes médicos marcados)
3. **Zonas de Treinamento**: Referência de intensidades
4. **Problemas de Saúde**: Lista de condições médicas (se houver)
5. **Recomendações Médicas**: Orientações da IA (se houver)

## 🚀 Instalação

### 1. Certifique-se de ter Python instalado (3.8 ou superior)

```bash
python --version
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Execute o programa:

```bash
python training_planner.py
```

### Siga as instruções na tela:

1. Digite o nome do atleta
2. Informe a idade
3. Escolha o esporte
4. Defina quantos dias pode treinar por semana
5. Selecione a distância da prova
6. Informe o limiar de lactato (bpm)
7. Informe o VO2 Max (ml/kg/min)

O sistema gerará automaticamente um plano de treinamento personalizado!

## 📝 Exemplo de Uso

```
Nome do atleta: João Silva
Idade: 35
Peso: 75 kg
Altura: 178 cm
Esporte: Corrida
Dias por semana: 5
Distância: Maratona
Limiar de Lactato: 168 bpm
VO2 Max: 52 ml/kg/min

Possui problema de saúde? Sim
Tipo: Ortopédico
Descrição: Condromalácia patelar
Membro afetado: joelho_direito
Gravidade: Moderado

🤖 ANÁLISE DE IA - RECOMENDAÇÕES:
⚠️ Condromalácia patelar (Joelho Direito):
  • Prefira terrenos planos ou levemente ondulados
  • Substitua corridas longas por ciclismo ou natação
  • Use tênis com amortecimento adequado
  • Fortaleça musculatura do quadríceps
  • Evite aumentos súbitos de volume

📋 Plano Semanal:
✅ Treinos automaticamente ajustados
✅ Volume reduzido em 30%
✅ Intensidade adaptada
✅ Alertas ⚕️ em treinos modificados
```

## 🎯 Zonas de Treinamento

O sistema calcula automaticamente 5 zonas de treinamento:

- **Z1 - Recuperação**: 50-65% do limiar
- **Z2 - Aeróbico**: 65-80% do limiar
- **Z3 - Tempo**: 80-90% do limiar
- **Z4 - Limiar**: 90-100% do limiar
- **Z5 - VO2max**: 100-110% do limiar

## 📦 Estrutura do Código

```
training_planner.py
├── HealthIssue: Classe para problemas de saúde
├── Athlete: Classe para dados do atleta (com IMC)
├── HealthAdvisor: 🤖 IA para análise e adequações médicas
│   ├── Knowledge Base: 7+ regiões ortopédicas
│   ├── Systemic Conditions: 4+ condições sistêmicas
│   ├── analyze_health_issues(): Análise completa
│   └── adjust_training(): Ajustes automáticos
├── TrainingZones: Cálculo de zonas de treinamento
├── TrainingPlanGenerator: Geração de treinos personalizados
│   └── Integração automática com HealthAdvisor
└── ExcelExporter: Exportação para Excel (5 abas)
```

## 🔧 Personalização

Os treinos são ajustados automaticamente com base em:

- **Volume de treino**: Calculado pela distância da prova
- **Frequência semanal**: Adapta quantidade e duração dos treinos
- **Nível do atleta**: Baseado em limiar, VO2 e IMC
- **Especificidade**: Treinos específicos para cada modalidade
- **🆕 Condições de saúde**: Ajustes inteligentes por lesão/doença
- **🆕 Gravidade**: Adequação proporcional ao nível da restrição

## 🏥 Regiões Ortopédicas Suportadas

- Joelho (direito/esquerdo)
- Ombro (direito/esquerdo)
- Tornozelo (direito/esquerdo)
- Lombar
- Quadril (direito/esquerdo)
- Pé (direito/esquerdo)
- Coxa (direito/esquerdo)

Cada região possui:
- ✅ Recomendações específicas
- ✅ Restrições de movimento
- ✅ Alternativas por modalidade
- ✅ Ajustes automáticos de volume/intensidade

## 📄 Formato da Planilha

Cada treino contém:

- Dia da semana
- Modalidade
- Duração
- Tipo de treino
- Zona de intensidade
- Frequência cardíaca alvo
- Descrição detalhada

## 🤝 Para Treinadores

Este sistema é ideal para:

- ✅ Economizar tempo na criação de planilhas
- ✅ Padronizar metodologia de treino
- ✅ Personalizar para cada atleta
- ✅ **🆕 Gerenciar atletas com restrições médicas de forma segura**
- ✅ **🆕 Documentar adequações e justificativas médicas**
- ✅ **🆕 Fornecer orientações profissionais sobre lesões**
- ✅ Documentar progressão dos clientes
- ✅ Fornecer material profissional aos atletas

## 🎯 Diferenciais do Sistema

1. **IA Integrada**: Sistema inteligente que realmente ajusta treinos
2. **Base de Conhecimento Médico**: 7+ regiões ortopédicas mapeadas
3. **Análise Imediata**: Feedback instantâneo ao cadastrar problemas
4. **Marcação Visual**: Treinos adaptados claramente identificados
5. **Documentação Completa**: Tudo registrado na planilha Excel
6. **Segurança**: Reduz risco de agravamento de lesões

## 📞 Suporte

Para dúvidas ou melhorias, entre em contato com o desenvolvedor.

## 📜 Licença

Este projeto pode ser usado livremente para fins educacionais e profissionais.

---

**Desenvolvido para auxiliar treinadores na preparação de atletas** 🏆
