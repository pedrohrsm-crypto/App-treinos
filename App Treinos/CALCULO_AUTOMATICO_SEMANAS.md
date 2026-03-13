# 📅 Cálculo Automático de Semanas até a Prova

## 🎯 Objetivo

Permitir que atletas que **não sabem quantas semanas faltam** até sua prova possam simplesmente informar a **data do evento** e o sistema calcula automaticamente o período de treinamento ideal.

---

## 🚀 Como Funciona

### Fluxo de Uso

1. **Sistema pergunta:** "Você sabe quantas semanas faltam até a prova? (s/n)"
   
2. **Se o usuário responder 'n' (não sabe):**
   - Sistema pede: "Qual a data da prova? (DD/MM/AAAA)"
   - Usuário informa: `15/09/2026`
   - Sistema calcula automaticamente usando o timestamp do computador
   - Exibe resultado detalhado

3. **Se o usuário responder 's' (sabe):**
   - Segue o fluxo tradicional
   - Usuário informa diretamente: `26 semanas`

---

## 📐 Lógica de Cálculo

### Função: `calcular_semanas_ate_prova(data_prova_str: str) -> int`

```python
def calcular_semanas_ate_prova(data_prova_str: str) -> int:
    """
    Calcula quantas semanas faltam até a data da prova.
    
    Args:
        data_prova_str: Data da prova no formato DD/MM/AAAA
        
    Returns:
        Número de semanas até a prova (arredondado para cima)
        
    Raises:
        ValueError: Se a data for inválida ou estiver no passado
    """
    # 1. Parse da data no formato brasileiro (DD/MM/AAAA)
    data_prova = datetime.strptime(data_prova_str, "%d/%m/%Y")
    
    # 2. Obter data atual do sistema (zerada para comparação justa)
    data_atual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 3. Validar se não está no passado
    if data_prova < data_atual:
        raise ValueError("A data da prova não pode estar no passado!")
    
    # 4. Calcular diferença em dias
    diferenca_dias = (data_prova - data_atual).days
    
    # 5. Converter para semanas (arredondar PARA CIMA)
    semanas = math.ceil(diferenca_dias / 7)
    
    # 6. Garantir pelo menos 1 semana
    return max(1, semanas)
```

---

## 🎨 Exemplo de Interação

### Cenário 1: Usuário NÃO sabe as semanas

```
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
```

### Cenário 2: Usuário SABE as semanas

```
═══════════════════════════════════════════════════════════════════
📅 CONFIGURAÇÃO DO PERÍODO DE TREINAMENTO
═══════════════════════════════════════════════════════════════════

Você sabe quantas semanas faltam até a prova? (s/n): s

Quantas semanas faltam até a prova? (1-52): 27
```

---

## ✅ Validações Implementadas

### 1. **Formato de Data**
- ✅ Aceita apenas: `DD/MM/AAAA`
- ❌ Rejeita formatos inválidos (YYYY-MM-DD, DD-MM-YYYY, etc.)
- **Exemplo válido:** `15/08/2026`
- **Exemplo inválido:** `2026-08-15`

**Mensagem de erro:**
```
❌ Erro: Formato de data inválido! Use DD/MM/AAAA (ex: 15/08/2026)
   Tente novamente.
```

### 2. **Data no Passado**
- ✅ Verifica se data da prova >= data atual
- ❌ Rejeita datas anteriores a hoje

**Mensagem de erro:**
```
❌ Erro: A data da prova não pode estar no passado!
   Tente novamente.
```

### 3. **Limite de 52 Semanas**
- Se resultado > 52 semanas, sistema oferece opção:

```
⚠️  A data informada resulta em 65 semanas.
   O sistema suporta planejamento de até 52 semanas.
   Deseja usar 52 semanas? (s/n): s
```

### 4. **Arredondamento para Cima**
- Usa `math.ceil()` para garantir tempo suficiente
- **Exemplo:** 5 dias → 1 semana (não 0.7)
- **Exemplo:** 15 dias → 3 semanas (não 2.1)

### 5. **Mínimo de 1 Semana**
- Mesmo para data de hoje → retorna 1 semana
- Permite plano de taper/polimento mínimo

---

## 📊 Exemplos Práticos

| Data da Prova | Dias Calculados | Semanas Resultantes | Observação |
|---------------|-----------------|---------------------|------------|
| Hoje + 5 dias | 5 dias | 1 semana | Arredondado para cima |
| Hoje + 60 dias | 60 dias | 9 semanas | 60/7 = 8.57 → 9 |
| Hoje + 84 dias | 84 dias | 12 semanas | 84/7 = 12.0 |
| Hoje + 180 dias | 180 dias | 26 semanas | ~6 meses |
| Hoje + 280 dias | 280 dias | 40 semanas | ~9 meses |
| Hoje + 400 dias | 400 dias | 52 semanas | Limitado ao máximo |

---

## 🔧 Integração com Periodização

O número de semanas calculado automaticamente é usado **exatamente da mesma forma** que quando informado manualmente:

1. **Distribuição de Fases:**
   - Base Aeróbica
   - Resistência Específica
   - Desenvolvimento de Velocidade
   - Potência e VO2max
   - Polimento/Taper

2. **Semanas de Recuperação:**
   - Automaticamente a cada 4 semanas
   - Volume reduzido para 70%

3. **Exportação Excel:**
   - Tabela completa de periodização
   - Detalhes de cada semana

---

## 🎯 Benefícios

### Para o Atleta:
✅ **Não precisa fazer contas manuais** (dias → semanas)  
✅ **Precisão absoluta** (usa timestamp do sistema)  
✅ **Validação automática** (data não pode estar no passado)  
✅ **Experiência mais intuitiva** (lembra data da prova, não semanas)  

### Para o Treinador:
✅ **Menos erros de cálculo** pelos atletas  
✅ **Padronização do processo**  
✅ **Atualização automática** (cada vez que gera o plano)  
✅ **Integração perfeita** com periodização existente  

---

## 🧪 Testes Realizados

### Cenários Testados:
1. ✅ Data futura válida (84 dias = 12 semanas)
2. ✅ Data muito distante (280 dias = 40 semanas)
3. ✅ Data muito próxima (5 dias = 1 semana)
4. ✅ Data no passado (exceção capturada)
5. ✅ Formato inválido (exceção capturada)
6. ✅ Data de hoje (mínimo 1 semana)

**Arquivo de testes:** `teste_calculo_semanas.py`

---

## 📝 Casos de Uso Reais

### **Caso 1: Maratona Planejada**
```
Atleta: João Silva
Data da prova: Maratona de São Paulo - 15/09/2026
Dias calculados: 186 dias
Semanas: 27 semanas
Periodização: 5 fases completas (9+7+5+4+2)
```

### **Caso 2: Ironman com Antecedência**
```
Atleta: Maria Oliveira
Data da prova: Ironman Florianópolis - 10/08/2026
Dias calculados: 150 dias
Semanas: 22 semanas
Periodização: 5 fases (7+6+4+3+2)
Total treinos: ~132 (3 modalidades)
```

### **Caso 3: 10K Curto**
```
Atleta: Ana Costa
Data da prova: Corrida local - 12/05/2026
Dias calculados: 60 dias
Semanas: 9 semanas
Periodização: 3 fases (velocidade+potência+polimento)
```

---

## 🔮 Implementação Futura (Opcional)

### Possíveis Melhorias:
- [ ] Permitir múltiplas datas de prova (A, B, C)
- [ ] Calcular "prova principal" vs "provas preparatórias"
- [ ] Alertas se data estiver muito próxima (<4 semanas)
- [ ] Sugestão automática de distância baseada no tempo disponível
- [ ] Integração com calendário do Google/Outlook
- [ ] Histórico de provas anteriores

---

## 📚 Arquivos Relacionados

- **Código principal:** `training_planner.py` (função `calcular_semanas_ate_prova()`)
- **Testes:** `teste_calculo_semanas.py`
- **Demonstração:** `exemplo_calculo_automatico.py`
- **Documentação:** Este arquivo (`CALCULO_AUTOMATICO_SEMANAS.md`)

---

## 💡 Dica para Usuários

**Quando usar cada opção:**

| Situação | Opção Recomendada |
|----------|-------------------|
| Sabe a data exata da prova | ❌ Manual ✅ **AUTOMÁTICO** |
| Prova ainda não tem data definida | ✅ Manual ❌ Automático |
| Quer planejar "próximas 12 semanas" | ✅ Manual ❌ Automático |
| Quer periodização flexível | ✅ Manual ❌ Automático |

**🎯 RECOMENDAÇÃO:** Se você **sabe a data da prova**, use o cálculo automático! É mais preciso e fácil.

---

**Implementado em:** 13/03/2026  
**Versão:** 2.1  
**Status:** ✅ Totalmente funcional e testado
