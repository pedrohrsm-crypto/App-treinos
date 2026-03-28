# Histórico de Contexto — App Treinos

**Última atualização:** 28/03/2026  
**Versão atual:** 2.0  
**Branch:** main  
**Último commit:** `e0cc841` — "Add GUI modernization documentation" (22/03/2026)

---

## 1. O Que É o Projeto

App Treinos é um **planejador inteligente de treinos esportivos** com interface gráfica, voltado para profissionais de Educação Física. Gera planilhas personalizadas de treinamento para 6 modalidades:

- Corrida
- Ciclismo
- Natação
- Triathlon
- Duathlon (Natação + Corrida)
- Duathlon (Ciclismo + Corrida)

### Diferenciais
- Interface gráfica acessível (WCAG AAA, contraste 21:1)
- Wizard de 6 passos para criação de treinos
- Adaptação automática ao ciclo menstrual
- Sistema de saúde com IA (HealthAdvisor)
- Periodização de 1 a 52 semanas
- Isolamento de dados por profissional (CREF)
- Exportação para Excel e PDF profissional

---

## 2. Arquitetura do Projeto

```
D:\GitHub\App Treinos\Python\App Treinos\
├── App_Treinos_GUI.py          # Launcher principal (GUI)
├── App_Treinos_GUI.bat         # Launcher Windows (duplo clique)
├── App_Treinos.bat             # Launcher CLI (Windows)
├── App_Treinos.command         # Launcher CLI (macOS)
├── training_planner.py         # Motor CLI + classes base (Athlete, TrainerInfo, HealthIssue, etc.)
├── training_manager.py         # Gerenciador de treinos por profissional
├── pdf_exporter.py             # Exportação PDF profissional (reportlab)
├── test_cli.py                 # Testes CLI
├── requirements.txt            # pandas, openpyxl, reportlab
│
├── core/
│   ├── training_engine.py      # Motor de geração de treinos (duplicado do training_planner.py)
│   ├── database.py             # Banco de dados SQLite/MySQL + autenticação
│   └── archived/               # Backup do engine anterior
│
├── gui/
│   ├── main_gui.py             # Janela principal (AppTreinosGUI)
│   ├── theme.py                # Tema acessível (AccessibleTheme)
│   ├── wizard_steps.py         # Passos do wizard (6 etapas)
│   ├── training_wizard.py      # Controlador do wizard
│   ├── modern_widgets.py       # Widgets modernos (AnimatedButton, AnimatedCard, etc.)
│   ├── training_list.py        # Lista de treinos
│   ├── register_screen.py      # Tela de cadastro
│   └── admin_panel.py          # Painel administrativo
│
├── data/
│   ├── app_treinos.db          # Banco SQLite
│   ├── exports/                # Planilhas exportadas (7 arquivos de exemplo)
│   └── trainers/               # Diretórios por treinador (CREF)
│       └── 123456GSP/          # Exemplo: CREF 123456-G/SP
│
├── docs/                       # 23 arquivos de documentação
├── scripts/                    # 16 scripts de teste e utilidades
├── linux/                      # Scripts de instalação/execução Linux
└── macos/                      # Scripts de instalação/execução macOS
```

---

## 3. Histórico de Commits

| Data | Commit | Descrição |
|---|---|---|
| 12/03/2026 | `e252a92` | Arquivos base — estrutura inicial do projeto |
| 13/03/2026 | `5cf00a0` | Atualizações de 13/03 |
| 19/03/2026 | `bd9cade` | GUI e sistema de identificação profissional |
| 22/03/2026 | `2f68ba7` | Refatoração completa: remover duplicação, adicionar novos recursos |
| 22/03/2026 | `1d576e7` | Modernização GUI: animações, bordas arredondadas, efeitos hover |
| 22/03/2026 | `599a271` | Modernização GUI (continuação) |
| 22/03/2026 | `e0cc841` | Documentação da modernização da GUI ← **HEAD** |

---

## 4. Estado Atual (Onde Paramos)

### O que está PRONTO (✅)

- [x] Motor de geração de treinos (6 modalidades, periodização completa)
- [x] Interface gráfica com wizard de 6 passos
- [x] Tema acessível WCAG AAA (contraste 21:1)
- [x] Widgets modernos com animações (AnimatedButton, AnimatedCard, RoundedFrame, FadeTransition)
- [x] Sistema de autenticação (CPF + CREF + senha)
- [x] Banco de dados SQLite com suporte a MySQL
- [x] Isolamento de dados por profissional (diretórios por CREF)
- [x] Exportação Excel (openpyxl)
- [x] Exportação PDF profissional (reportlab)
- [x] Adaptação ao ciclo menstrual
- [x] Sistema de saúde com IA (HealthAdvisor — problemas ortopédicos e sistêmicos)
- [x] Cálculo automático de semanas até a prova
- [x] Suporte multiplataforma (Windows, Linux, macOS)
- [x] 8/8 testes automatizados passando (relatório de 21/03/2026)
- [x] Documentação extensa (23 arquivos em docs/)
- [x] 16 scripts de teste/utilidade

### O que pode precisar de atenção (⚠️)

- [ ] **Duplicação de código:** `training_planner.py` e `core/training_engine.py` contêm código muito similar — a refatoração do commit `2f68ba7` pode não ter sido completa
- [ ] **Arquivo `data/app_treinos.db` modificado** — há alteração não commitada no banco de dados
- [ ] **Diretório `data/trainers/None/`** — indica que algum treino foi salvo sem treinador identificado
- [ ] **test_cli.py** é apenas informativo (não executa testes reais) — testes reais estão dispersos em `scripts/`

### Funcionalidades documentadas mas não verificadas recentemente

- Painel administrativo (`gui/admin_panel.py`)
- Tela de registro de novos usuários (`gui/register_screen.py`)
- Lista de treinos salvos (`gui/training_list.py`)
- Suporte MySQL (configurado mas sem credenciais reais)

---

## 5. Tecnologias

| Componente | Tecnologia | Versão Requerida |
|---|---|---|
| Linguagem | Python | 3.8+ |
| GUI | Tkinter | (nativo) |
| Dados tabulares | pandas | >= 2.0.0 |
| Export Excel | openpyxl | >= 3.1.0 |
| Export PDF | reportlab | >= 4.0.0 |
| Banco de dados | SQLite | (nativo) |
| Banco de dados (prod) | MySQL | opcional |

---

## 6. Como Executar

```bash
# Windows (duplo clique)
App_Treinos_GUI.bat

# Windows (terminal)
python App_Treinos_GUI.py

# Linux / macOS
python3 App_Treinos_GUI.py
```

---

## 7. Métricas de Performance

| Operação | Tempo |
|---|---|
| Inicialização | < 0.5s |
| Geração de plano | < 2s |
| Exportação Excel | < 1s |
| Exportação PDF | ~1s |

---

## 8. Sugestões de Próximos Passos

Estas são sugestões baseadas na análise do estado atual do projeto. A prioridade e a direção devem ser definidas pelo responsável do projeto.

### Correções e Melhorias Técnicas
1. **Resolver duplicação** entre `training_planner.py` e `core/training_engine.py`
2. **Consolidar testes** — unificar os 16 scripts de teste em uma suíte com pytest
3. **Limpar diretório `data/trainers/None/`** — investigar origem e prevenir recorrência
4. **Commit do `app_treinos.db`** ou adicioná-lo ao `.gitignore`

### Funcionalidades Potenciais
5. **Dashboard de progresso** — visualização de treinos realizados vs. planejados
6. **Histórico de alterações** — log de modificações em cada plano de treino
7. **Integração com APIs de saúde** — importação de dados de dispositivos (Garmin, Strava)
8. **Multi-idioma** — interface em inglês e espanhol além do português
9. **Modo escuro** — tema alternativo mantendo acessibilidade

### Infraestrutura
10. **CI/CD** — pipeline de testes automáticos no GitHub Actions
11. **Empacotamento** — criar executável standalone (PyInstaller ou cx_Freeze)
12. **Versionamento semântico** — tags de release (v2.0.0, v2.1.0, etc.)

---

*Este documento serve como ponto de orientação para retomar o desenvolvimento. Atualize-o ao final de cada sessão de trabalho.*
