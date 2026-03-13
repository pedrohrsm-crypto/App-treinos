# 📚 Índice Completo do Projeto - App Treinos

## 📂 Estrutura de Arquivos

### 🔧 Arquivos Principais

| Arquivo | Descrição | Linhas | Status |
|---------|-----------|--------|--------|
| **training_planner.py** | Sistema principal de geração de treinos | ~1500 | ✅ Funcional |
| **requirements.txt** | Dependências do projeto | 2 | ✅ Atual |
| **README.md** | Documentação principal do sistema | 254 | ✅ Atualizado |
| **AppTreinosCode.code-workspace** | Configuração do workspace VS Code | - | ✅ Ativo |

---

### 📖 Documentação

| Arquivo | Conteúdo | Criado em |
|---------|----------|-----------|
| **CALCULO_AUTOMATICO_SEMANAS.md** | Cálculo automático por data da prova | 13/03/2026 |
| **PERIODIZACAO_COMPLETA.md** | Sistema de periodização multi-semanas | 13/03/2026 |
| **CICLO_MENSTRUAL.md** | Adaptações para ciclo menstrual | 12/03/2026 |
| **EXEMPLO_USO_CICLO_MENSTRUAL.md** | Casos práticos de uso do ciclo | 12/03/2026 |
| **NOVAS_FUNCIONALIDADES.md** | Histórico de features adicionadas | 12/03/2026 |

---

### 🧪 Arquivos de Teste

| Arquivo | Tipo | Testes | Resultado |
|---------|------|--------|-----------|
| **teste_calculo_semanas.py** | Unitário | 6 testes | ✅ Todos passaram |
| **teste_ia_saude.py** | Integração | 7+ casos | ✅ Funcional |

---

### 💡 Exemplos Práticos

| Arquivo | Demonstração | Casos |
|---------|--------------|-------|
| **exemplo_periodizacao.py** | Periodização multi-semanas | 3 (8/20/40 semanas) |
| **exemplo_calculo_automatico.py** | Cálculo por data | 4 cenários |
| **comparacao_modos_configuracao.py** | Comparação manual vs automático | 2 modos |
| **resumo_implementacao.py** | Resumo visual da implementação | Resumo completo |
| **exemplos.py** | Casos diversos de atletas | 6+ exemplos |

---

### 📊 Planilhas Geradas (Exemplos)

| Arquivo Excel | Origem | Conteúdo |
|---------------|--------|----------|
| **Maratona_40_Semanas_Completo.xlsx** | exemplo_periodizacao.py | 200 treinos, 4 abas |
| **Ironman_20_Semanas_Completo.xlsx** | exemplo_periodizacao.py | 120 treinos, 4 abas |
| **Exemplo_Corrida_Ciclo_Menstrual.xlsx** | exemplos.py | 1 semana, adaptações menstruais |
| **Exemplo_Triathlon.xlsx** | exemplos.py | 1 semana, 3 modalidades |

---

## 🎯 Funcionalidades por Arquivo

### training_planner.py

**Classes Principais:**
- `Athlete`: Dados do atleta (idade, peso, esporte, gênero, semanas, etc.)
- `HealthIssue`: Problemas de saúde (ortopédicos, sistêmicos)
- `HealthAdvisor`: IA para adaptações médicas e menstruais
- `PeriodizationPlanner`: Gerenciamento de fases de treinamento
- `TrainingZones`: Cálculo de zonas de frequência cardíaca
- `TrainingPlanGenerator`: Geração de treinos personalizados
- `ExcelExporter`: Exportação para planilhas Excel

**Funções Principais:**
- `calcular_semanas_ate_prova(data_str)`: Cálculo automático de semanas 🆕
- `main()`: Fluxo principal do aplicativo

**Capacidades:**
- ✅ Coleta de dados do atleta (18+ campos)
- ✅ Análise de saúde com IA (7+ regiões ortopédicas)
- ✅ Adaptação para ciclo menstrual (4 fases)
- ✅ Periodização profissional (5 fases)
- ✅ Cálculo por data da prova 🆕
- ✅ Geração de 1 a 52 semanas (até 250+ treinos)
- ✅ Exportação Excel multi-aba

---

### teste_calculo_semanas.py

**Casos Testados:**
1. ✅ Data futura válida (84 dias → 12 semanas)
2. ✅ Data distante (280 dias → 40 semanas)
3. ✅ Data próxima (5 dias → 1 semana arredondada)
4. ✅ Data no passado (ValueError)
5. ✅ Formato inválido (ValueError)
6. ✅ Data de hoje (mínimo 1 semana)

---

### exemplo_periodizacao.py

**Exemplos Disponíveis:**
1. **Maratona 40 semanas**: Plano completo de longo prazo
2. **10K 8 semanas**: Plano curto para corrida rápida
3. **Ironman 20 semanas**: Triathlon de distância longa

**Uso:**
```bash
python exemplo_periodizacao.py
# Menu interativo com 3 opções
```

---

### exemplo_calculo_automatico.py

**Cenários Demonstrados:**
1. Maratona de São Paulo (180 dias → 26 semanas)
2. Ironman Florianópolis (150 dias → 22 semanas)
3. 10K Local (60 dias → 9 semanas)
4. Prova muito próxima (6 dias → 1 semana)

**Aprendizado:**
- Vantagens do cálculo automático
- Comparação com método manual
- Quando usar cada modo

---

### comparacao_modos_configuracao.py

**Conteúdo:**
- Fluxo do Modo 1 (Manual)
- Fluxo do Modo 2 (Automático) 🆕
- Tabela comparativa
- 5 cenários de uso recomendados
- Dicas para escolher o modo certo

---

## 📋 Histórico de Desenvolvimento

### Versão 1.0 (12/03/2026)
- ✅ Sistema base de geração de treinos
- ✅ 4 modalidades (Triathlon, Corrida, Natação, Ciclismo)
- ✅ IA de saúde com 7+ regiões ortopédicas
- ✅ Exportação Excel básica

### Versão 2.0 (12/03/2026)
- ✅ Campo de gênero adicionado
- ✅ Sistema de adaptação menstrual (4 fases)
- ✅ IA ajusta treinos por fase hormonal
- ✅ Documentação completa (CICLO_MENSTRUAL.md)

### Versão 2.1 (13/03/2026)
- ✅ Periodização multi-semanas (1-52 semanas)
- ✅ 5 fases de treinamento progressivas
- ✅ Semanas de recuperação automáticas
- ✅ Exportação de plano completo
- ✅ Documentação (PERIODIZACAO_COMPLETA.md)

### Versão 2.2 (13/03/2026) 🆕
- ✅ **Cálculo automático por data da prova**
- ✅ Validação de datas (passado/formato)
- ✅ Dois modos de configuração (manual/automático)
- ✅ Testes unitários completos
- ✅ Documentação (CALCULO_AUTOMATICO_SEMANAS.md)
- ✅ Exemplos práticos e comparativos

---

## 🚀 Guia Rápido de Uso

### Para Usuários Finais:

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar sistema principal
python training_planner.py

# 3. Seguir prompts interativos
```

### Para Desenvolvedores:

```bash
# Executar testes
python teste_calculo_semanas.py
python teste_ia_saude.py

# Ver exemplos
python exemplo_periodizacao.py
python exemplo_calculo_automatico.py
python comparacao_modos_configuracao.py
```

---

## 📚 Documentação Recomendada por Cenário

| Cenário | Documentos Relevantes |
|---------|----------------------|
| Primeiro uso do sistema | README.md |
| Atleta feminina | CICLO_MENSTRUAL.md, EXEMPLO_USO_CICLO_MENSTRUAL.md |
| Planejamento longo (>12 semanas) | PERIODIZACAO_COMPLETA.md |
| Não sabe quantas semanas faltam | CALCULO_AUTOMATICO_SEMANAS.md |
| Dúvida entre modos | comparacao_modos_configuracao.py |
| Desenvolvimento/testes | teste_*.py, exemplo_*.py |

---

## 🎯 Estatísticas do Projeto

- **Total de arquivos Python**: 8
- **Total de arquivos de documentação**: 5
- **Linhas de código principal**: ~1500
- **Testes implementados**: 13+
- **Funcionalidades principais**: 10+
- **Modalidades suportadas**: 4
- **Semanas máximas**: 52
- **Treinos máximos por plano**: 250+

---

## 🔗 Arquivos Interdependentes

```
training_planner.py (CENTRAL)
    ├── Importado por: exemplo_periodizacao.py
    ├── Importado por: exemplo_calculo_automatico.py
    ├── Importado por: teste_calculo_semanas.py
    ├── Importado por: teste_ia_saude.py
    └── Importado por: exemplos.py

README.md
    ├── Referencia: CALCULO_AUTOMATICO_SEMANAS.md
    ├── Referencia: PERIODIZACAO_COMPLETA.md
    ├── Referencia: CICLO_MENSTRUAL.md
    └── Referencia: EXEMPLO_USO_CICLO_MENSTRUAL.md
```

---

## 📞 Manutenção

**Arquivos que requerem atualização quando modificar:**

| Modificação | Arquivos a atualizar |
|-------------|---------------------|
| Nova funcionalidade | README.md, NOVAS_FUNCIONALIDADES.md |
| Nova dependência | requirements.txt |
| Mudança na API principal | Todos os exemplo_*.py |
| Nova validação | teste_*.py correspondente |

---

**Última atualização**: 13/03/2026  
**Versão atual**: 2.2  
**Status**: ✅ Totalmente funcional e testado
