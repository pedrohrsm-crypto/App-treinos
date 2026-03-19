# 🖥️ Guia da Interface Gráfica (GUI)

## Visão Geral

A interface gráfica do **App Treinos** utiliza um sistema de wizard (assistente) com múltiplas etapas para coletar informações de forma organizada e intuitiva.

---

## 🎯 Estrutura do Wizard

### Total de Etapas: 3

1. **👨‍⚕️ Identificação do Profissional de Educação Física** (NOVA - OBRIGATÓRIA)
2. **📝 Dados Básicos do Atleta**
3. **🏃 Modalidade e Disponibilidade**

---

## 📋 Etapa 1: Identificação do Profissional

### Objetivo
Garantir que todo plano de treinamento seja elaborado por um profissional de Educação Física credenciado, conforme exigências legais e éticas da profissão.

### Campos Obrigatórios

| Campo | Formato | Exemplo | Validação |
|-------|---------|---------|-----------|
| **Nome Completo** | Texto livre | Dr. João Silva Santos | Mínimo 5 caracteres |
| **CPF** | Somente números | 12345678909 | Algoritmo oficial (11 dígitos) |
| **CREF** | Formato específico | 123456-G/SP | Regex: NNNNNN-G/UF |

### Avisos Visuais

A interface exibe dois avisos importantes:

**Aviso Superior:**
```
⚠️ ATENÇÃO
Todo plano de treinamento deve ser elaborado por um profissional
de Educação Física credenciado (CREF). Preencha os dados abaixo:
```

**Informações Inferior:**
```
ℹ️ Informações sobre os campos:
• CPF: Cadastro de Pessoa Física (validado automaticamente)
• CREF: Conselho Regional de Educação Física
  Formato: NNNNNN-G/UF (ex: 123456-G/SP)
```

### Processo de Validação

1. **Usuário preenche os campos**
2. **Clica em "Próximo →"**
3. **Sistema valida automaticamente:**
   - Nome tem pelo menos 5 caracteres?
   - CPF é válido matematicamente?
   - CREF está no formato correto?

4. **Se válido:**
   - ✅ Mensagem de sucesso aparece
   - Dados formatados são exibidos
   - Usuário pode avançar para próxima etapa

5. **Se inválido:**
   - ❌ Mensagem de erro específica aparece
   - Usuário corrige o campo com problema
   - Tenta novamente

### Exemplos de Validação

#### ✅ Validação Bem-Sucedida

```
┌──────────────────────────────────────────┐
│  ✅ Dados Validados                      │
├──────────────────────────────────────────┤
│                                          │
│  ✅ Profissional validado com sucesso!  │
│                                          │
│  Nome: Dr. João Silva Santos            │
│  CPF: 123.456.789-09                    │
│  CREF: 123456-G/SP                      │
│                                          │
│              [ OK ]                      │
└──────────────────────────────────────────┘
```

#### ❌ Erro: CPF Inválido

```
┌──────────────────────────────────────────┐
│  ❌ Erro de Validação                    │
├──────────────────────────────────────────┤
│                                          │
│  CPF inválido. Verifique os números     │
│  digitados.                              │
│                                          │
│              [ OK ]                      │
└──────────────────────────────────────────┘
```

#### ❌ Erro: CREF Inválido

```
┌──────────────────────────────────────────┐
│  ❌ Erro de Validação                    │
├──────────────────────────────────────────┤
│                                          │
│  CREF inválido. Use o formato:          │
│  123456-G/UF (ex: 123456-G/SP)          │
│                                          │
│              [ OK ]                      │
└──────────────────────────────────────────┘
```

#### ❌ Erro: Nome Muito Curto

```
┌──────────────────────────────────────────┐
│  ❌ Erro de Validação                    │
├──────────────────────────────────────────┤
│                                          │
│  Nome muito curto. Digite o nome        │
│  completo (mínimo 5 caracteres).        │
│                                          │
│              [ OK ]                      │
└──────────────────────────────────────────┘
```

---

## 📝 Etapa 2: Dados Básicos do Atleta

### Campos

- **Nome do Atleta:** Texto livre
- **Idade:** 10-100 anos
- **Peso:** 30-200 kg
- **Altura:** 100-250 cm
- **Gênero:** Masculino/Feminino (radio buttons)

---

## 🏃 Etapa 3: Modalidade e Disponibilidade

### Campos

- **Esporte:** Dropdown (Triathlon, Corrida, Natação, Ciclismo)
- **Dias de treino por semana:** Slider 2-7 dias

---

## 🎨 Design e Tema

### Cores
- **Primária:** Azul (#2563EB)
- **Fundo:** Cinza claro (#F9FAFB)
- **Cards:** Branco (#FFFFFF)
- **Texto:** Cinza escuro (#111827)
- **Desabilitado:** Cinza médio (#9CA3AF)

### Tipografia
- **Fonte:** Segoe UI (Windows), SF Pro (Mac)
- **Tamanhos:**
  - Título: 24px
  - Heading: 16px (negrito)
  - Normal: 10px
  - Small: 9px

### Espaçamento
- **XS:** 4px
- **SM:** 8px
- **MD:** 12px
- **LG:** 16px
- **XL:** 24px

---

## 🔄 Fluxo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                         APP TREINOS                             │
│     Sistema Profissional de Planejamento de Treinamento        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Etapa 1 de 3                                                   │
│  👨‍⚕️ Identificação do Profissional de Educação Física          │
│                                                                 │
│  [Nome Completo: _________________________________]             │
│  [CPF: ___________________________________________]             │
│  [CREF: __________________________________________]             │
│                                                                 │
│                              [← Anterior]  [Próximo →]          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                       [Validação CPF/CREF]
                              ↓
                    [✅ Mensagem de Sucesso]
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Etapa 2 de 3                                                   │
│  📝 Dados Básicos do Atleta                                     │
│                                                                 │
│  [Nome: __________________________________________]             │
│  [Idade: _________________________________________]             │
│  [Peso: ___________________________________________]            │
│  [Altura: _________________________________________]            │
│  [Gênero: ⚪ Masculino  ⚪ Feminino]                            │
│                                                                 │
│                              [← Anterior]  [Próximo →]          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Etapa 3 de 3                                                   │
│  🏃 Modalidade e Disponibilidade                                │
│                                                                 │
│  [Esporte: ▼ Triathlon____________________________]             │
│  [Dias/semana: ━━━━━━●━━━━  5 dias]                            │
│                                                                 │
│                              [← Anterior]  [Finalizar ✓]        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    [Processar Dados Coletados]
                              ↓
                    [Gerar Plano de Treinamento]
                              ↓
                    [Exportar para Excel]
```

---

## 🎯 Recursos Especiais

### Navegação Inteligente

- **Botão "Anterior":**
  - Desabilitado na primeira etapa
  - Permite voltar sem perder dados preenchidos

- **Botão "Próximo":**
  - Valida dados antes de avançar
  - Muda para "Finalizar ✓" na última etapa

### Indicador de Progresso

Mostra no rodapé: `Etapa X de Y`

### Validação em Tempo Real

- CPF: Algoritmo oficial da Receita Federal
- CREF: Expressão regular para formato
- Campos numéricos: Validação de intervalo

---

## 🧪 Testando a GUI

### Teste Manual

1. **Executar:**
   ```bash
   python gui/main_gui.py
   ```

2. **Preencher Etapa 1 (com dados válidos):**
   - Nome: Dr. João Silva Santos
   - CPF: 12345678909
   - CREF: 123456-G/SP

3. **Clicar "Próximo →"**
   - Deve aparecer mensagem de validação bem-sucedida

4. **Preencher Etapa 2:**
   - Nome: Maria Silva
   - Idade: 30
   - Peso: 65
   - Altura: 170
   - Gênero: Feminino

5. **Preencher Etapa 3:**
   - Esporte: Triathlon
   - Dias: 5

6. **Clicar "Finalizar ✓"**

### Teste de Validação

1. **Testar CPF inválido:**
   - CPF: 12345678900
   - Deve rejeitar com mensagem de erro

2. **Testar CREF inválido:**
   - CREF: ABC-123
   - Deve rejeitar com mensagem de erro

3. **Testar nome muito curto:**
   - Nome: João
   - Deve rejeitar com mensagem de erro

---

## 📊 Dados Coletados

Ao finalizar o wizard, os dados são armazenados em:

```python
collected_data = {
    # Etapa 1 - Profissional
    'nome_completo': StringVar(),
    'cpf': StringVar(),
    'cref': StringVar(),
    'trainer_obj': TrainerInfo,  # Objeto validado
    
    # Etapa 2 - Atleta
    'nome': StringVar(),
    'idade': StringVar(),
    'peso': StringVar(),
    'altura': StringVar(),
    'genero': StringVar(),
    
    # Etapa 3 - Modalidade
    'esporte': StringVar(),
    'dias_semana': IntVar()
}
```

---

## 🔧 Personalização

### Modificar Validações

Edite [gui/main_gui.py](../gui/main_gui.py) na classe `DadosProfissionalStep`:

```python
def validate(self):
    """Valida dados do profissional."""
    # Adicione validações personalizadas aqui
```

### Adicionar Novos Campos

```python
def _create_body(self):
    # Adicione novos campos aqui
    row = 0
    self._create_field(body, row, "Novo Campo:", "campo_novo", "text", "Placeholder")
```

---

## ✅ Checklist de Funcionalidades

- [x] Etapa de identificação profissional
- [x] Validação de CPF (algoritmo oficial)
- [x] Validação de CREF (formato regex)
- [x] Validação de nome (mínimo 5 caracteres)
- [x] Mensagens de erro personalizadas
- [x] Mensagem de sucesso com dados formatados
- [x] Navegação entre etapas (Anterior/Próximo)
- [x] Indicador de progresso
- [x] Design responsivo e acessível
- [x] Tema moderno e profissional

---

## 📚 Referências

- **training_planner.py:** Interface CLI
- **core/training_engine.py:** Backend com TrainerInfo
- **gui/main_gui.py:** Interface gráfica principal
- **gui/theme.py:** Configurações de tema
- **docs/IDENTIFICACAO_PROFISSIONAL.md:** Documentação técnica

---

**Atualizado em:** 18/03/2026  
**Versão:** 2.1
