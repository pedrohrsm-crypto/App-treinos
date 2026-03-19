# 📚 Índice Completo - App Treinos v2.0

**Guia rápido de navegação no projeto**

---

## 🚀 Início Rápido

### Para Usar o Aplicativo
1. **[README.md](README.md)** - Visão geral do projeto
2. **[COMO_EXECUTAR.md](docs/COMO_EXECUTAR.md)** - Guia de instalação e execução
3. **Execute:** `App_Treinos_GUI.bat` (Windows) ou `python3 App_Treinos_GUI.py` (Linux/macOS)

### Para Desenvolvedores
1. **[ESTRUTURA_DIRETORIOS.md](docs/ESTRUTURA_DIRETORIOS.md)** - Organização do código
2. **[RESUMO_IMPLEMENTACAO.md](docs/RESUMO_IMPLEMENTACAO.md)** - Detalhes técnicos
3. **[GUI_MANUAL.md](docs/GUI_MANUAL.md)** - Documentação da interface

---

## 📁 Estrutura de Arquivos

```
App Treinos/
│
├── 📄 README.md                          # Visão geral do projeto
├── 🚀 App_Treinos_GUI.py                 # Launcher Python (GUI)
├── 🪟 App_Treinos_GUI.bat                # Launcher Windows (GUI)
├── 🪟 App_Treinos.bat                    # Launcher Windows (CLI)
├── 🍎 App_Treinos.command                # Launcher macOS
├── 📜 training_planner.py                # Versão CLI (original)
├── 📋 requirements.txt                   # Dependências Python
│
├── 🎨 gui/                               # Interface Gráfica
│   ├── __init__.py                       # Inicialização do módulo
│   ├── theme.py                          # Tema acessível WCAG AAA
│   ├── main_gui.py                       # Aplicação principal
│   └── wizard_steps.py                   # Passos do wizard
│
├── ⚙️ core/                              # Motor do Aplicativo
│   ├── __init__.py                       # Inicialização do módulo
│   └── training_engine.py                # Lógica de geração de treinos
│
├── 💾 data/                              # Dados e Exportações
│   └── exports/                          # Planilhas Excel geradas
│       ├── Exemplo_Corrida_Ciclo_Menstrual.xlsx
│       ├── Exemplo_Triathlon.xlsx
│       ├── Ironman_20_Semanas_Completo.xlsx
│       └── Maratona_40_Semanas_Completo.xlsx
│
├── 📚 docs/                              # Documentação
│   ├── README.md                         # Índice da documentação
│   ├── RESUMO_IMPLEMENTACAO.md           # Resumo técnico v2.0
│   ├── COMO_EXECUTAR.md                  # Guia de execução
│   ├── GUI_MANUAL.md                     # Manual da interface
│   ├── ESTRUTURA_DIRETORIOS.md           # Organização do projeto
│   ├── NOVAS_FUNCIONALIDADES.md          # Histórico de recursos
│   ├── INDICE_PROJETO.md                 # Índice geral (este arquivo)
│   │
│   ├── 📖 Funcionalidades:
│   ├── CICLO_MENSTRUAL.md                # Adaptação ao ciclo
│   ├── PERIODIZACAO_COMPLETA.md          # Sistema de periodização
│   ├── CALCULO_AUTOMATICO_SEMANAS.md     # Cálculo de semanas
│   ├── MENSAGENS_LIMITE_SISTEMA.md       # Limites educacionais
│   │
│   └── 📖 Guias de Uso:
│       ├── EXEMPLO_USO_CICLO_MENSTRUAL.md    # Exemplo prático
│       ├── COMPATIBILIDADE_MULTIPLATAFORMA.md # Suporte OS
│       └── EXECUCAO_DUPLO_CLIQUE.md          # Execução fácil
│
├── 🧪 scripts/                           # Scripts Auxiliares
│   ├── teste_estrutura.py                # Teste de estrutura
│   ├── teste_ia_saude.py                 # Teste IA saúde
│   ├── teste_calculo_semanas.py          # Teste cálculos
│   ├── exemplos.py                       # Exemplos de uso
│   ├── exemplo_periodizacao.py           # Exemplo periodização
│   ├── exemplo_calculo_automatico.py     # Exemplo cálculos
│   ├── demo_execucao_rapida.py           # Demo execução
│   ├── demo_melhorias_entrada.py         # Demo entrada dados
│   ├── demo_mensagens_limite.py          # Demo mensagens
│   ├── resumo_implementacao.py           # Resumo features
│   └── comparacao_modos_configuracao.py  # Comparação modos
│
├── 🐧 linux/                             # Scripts Linux
│   ├── README.md                         # Guia Linux
│   ├── instalar.sh                       # Instalador
│   ├── executar.sh                       # Executor
│   ├── exemplos.sh                       # Exemplos
│   ├── app_treinos_launcher.sh           # Launcher
│   └── App_Treinos.desktop               # Desktop entry
│
└── 🍎 macos/                             # Scripts macOS
    ├── README.md                         # Guia macOS
    ├── instalar.sh                       # Instalador
    ├── executar.sh                       # Executor
    └── exemplos.sh                       # Exemplos
```

---

## 📖 Documentação por Categoria

### 🎯 Para Usuários

| Documento | Descrição |
|-----------|-----------|
| [README.md](README.md) | Visão geral e introdução |
| [COMO_EXECUTAR.md](docs/COMO_EXECUTAR.md) | Como instalar e executar |
| [GUI_MANUAL.md](docs/GUI_MANUAL.md) | Manual completo da interface |
| [EXEMPLO_USO_CICLO_MENSTRUAL.md](docs/EXEMPLO_USO_CICLO_MENSTRUAL.md) | Exemplo prático |

### 💻 Para Desenvolvedores

| Documento | Descrição |
|-----------|-----------|
| [ESTRUTURA_DIRETORIOS.md](docs/ESTRUTURA_DIRETORIOS.md) | Organização do código |
| [RESUMO_IMPLEMENTACAO.md](docs/RESUMO_IMPLEMENTACAO.md) | Detalhes técnicos v2.0 |
| [NOVAS_FUNCIONALIDADES.md](docs/NOVAS_FUNCIONALIDADES.md) | Histórico de recursos |

### 📚 Funcionalidades

| Documento | Descrição |
|-----------|-----------|
| [CICLO_MENSTRUAL.md](docs/CICLO_MENSTRUAL.md) | Adaptação ao ciclo menstrual |
| [PERIODIZACAO_COMPLETA.md](docs/PERIODIZACAO_COMPLETA.md) | Sistema de periodização |
| [CALCULO_AUTOMATICO_SEMANAS.md](docs/CALCULO_AUTOMATICO_SEMANAS.md) | Cálculo automático |
| [MENSAGENS_LIMITE_SISTEMA.md](docs/MENSAGENS_LIMITE_SISTEMA.md) | Limites educacionais |

### 🖥️ Multiplataforma

| Documento | Descrição |
|-----------|-----------|
| [COMPATIBILIDADE_MULTIPLATAFORMA.md](docs/COMPATIBILIDADE_MULTIPLATAFORMA.md) | Suporte Windows/Linux/macOS |
| [EXECUCAO_DUPLO_CLIQUE.md](docs/EXECUCAO_DUPLO_CLIQUE.md) | Execução simplificada |
| [linux/README.md](linux/README.md) | Guia específico Linux |
| [macos/README.md](macos/README.md) | Guia específico macOS |

---

## 🎨 Arquivos de Código

### Interface Gráfica (`gui/`)

| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| `theme.py` | ~200 | Tema acessível WCAG AAA |
| `main_gui.py` | ~376 | Aplicação principal e wizard |
| `wizard_steps.py` | ~250 | Passos do assistente |

### Lógica de Negócio (`core/`)

| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| `training_engine.py` | ~1500 | Motor de geração de treinos |

### Scripts de Teste (`scripts/`)

| Arquivo | Descrição |
|---------|-----------|
| `teste_estrutura.py` | Verifica estrutura e dependências |
| `teste_ia_saude.py` | Testa adaptações de saúde |
| `teste_calculo_semanas.py` | Testa cálculos de período |

### Scripts de Demo (`scripts/`)

| Arquivo | Descrição |
|---------|-----------|
| `exemplos.py` | Exemplos básicos de uso |
| `exemplo_periodizacao.py` | Exemplo de periodização |
| `demo_execucao_rapida.py` | Demo de execução rápida |
| `demo_melhorias_entrada.py` | Demo de entrada de dados |

---

## 🚀 Guias de Início Rápido

### Primeira Vez Usando

1. Leia: [README.md](README.md)
2. Siga: [COMO_EXECUTAR.md](docs/COMO_EXECUTAR.md)
3. Consulte: [GUI_MANUAL.md](docs/GUI_MANUAL.md)

### Desenvolvimento

1. Entenda: [ESTRUTURA_DIRETORIOS.md](docs/ESTRUTURA_DIRETORIOS.md)
2. Estude: [RESUMO_IMPLEMENTACAO.md](docs/RESUMO_IMPLEMENTACAO.md)
3. Explore: Código em `gui/` e `core/`

### Resolução de Problemas

1. Verifique: `python scripts/teste_estrutura.py`
2. Consulte: [COMO_EXECUTAR.md - Solução de Problemas](docs/COMO_EXECUTAR.md#-solução-de-problemas)
3. Execute: `python App_Treinos_GUI.py` para ver erros

---

## 📊 Estatísticas do Projeto

- **Linhas de código:** ~2.500
- **Arquivos de código:** 6 (gui: 3, core: 1, scripts: múltiplos)
- **Documentos:** 15+
- **Exemplos:** 10+
- **Plataformas:** 3 (Windows, Linux, macOS)
- **Versão:** 2.0 - Interface Gráfica

---

## 🔍 Busca Rápida

### Encontrar Informações Sobre:

- **Instalação:** [COMO_EXECUTAR.md](docs/COMO_EXECUTAR.md)
- **Uso da GUI:** [GUI_MANUAL.md](docs/GUI_MANUAL.md)
- **Ciclo Menstrual:** [CICLO_MENSTRUAL.md](docs/CICLO_MENSTRUAL.md)
- **Periodização:** [PERIODIZACAO_COMPLETA.md](docs/PERIODIZACAO_COMPLETA.md)
- **Código:** `gui/` e `core/`
- **Testes:** `scripts/teste_*.py`
- **Exemplos:** `scripts/exemplo_*.py` e `scripts/demo_*.py`
- **Linux:** [linux/README.md](linux/README.md)
- **macOS:** [macos/README.md](macos/README.md)

---

## ✅ Checklist de Documentação

Antes de usar, certifique-se de ler:

- [ ] [README.md](README.md) - Visão geral
- [ ] [COMO_EXECUTAR.md](docs/COMO_EXECUTAR.md) - Instalação
- [ ] [GUI_MANUAL.md](docs/GUI_MANUAL.md) - Uso da interface

Para desenvolvimento adicional:

- [ ] [ESTRUTURA_DIRETORIOS.md](docs/ESTRUTURA_DIRETORIOS.md)
- [ ] [RESUMO_IMPLEMENTACAO.md](docs/RESUMO_IMPLEMENTACAO.md)
- [ ] Código fonte em `gui/` e `core/`

---

## 🆘 Links Úteis

- **Execução Rápida:** [COMO_EXECUTAR.md](docs/COMO_EXECUTAR.md)
- **Problemas:** [COMO_EXECUTAR.md - Solução de Problemas](docs/COMO_EXECUTAR.md#-solução-de-problemas)
- **Teste de Estrutura:** `python scripts/teste_estrutura.py`
- **Exemplos Práticos:** `scripts/exemplos.py`

---

**Última atualização:** Março 2026  
**Versão do Projeto:** 2.0 - Interface Gráfica  
**Status:** ✅ Completo e Testado
