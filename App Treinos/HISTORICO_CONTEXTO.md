# Histórico de Contexto — App Treinos

**Última atualização:** 28/03/2026  
**Versão atual:** 3.0.0  
**Branch:** main  
**Último commit:** `09c2897` — "fix: corrigir chamada register_training no wizard e typo entry.details no progress" (28/03/2026)

---

## 1. O Que É o Projeto

App Treinos é um **planejador inteligente de treinos esportivos** com interface gráfica moderna (Flet/Flutter), voltado para profissionais de Educação Física. Gera planilhas personalizadas de treinamento para 6 modalidades:

- Corrida
- Ciclismo
- Natação
- Triathlon
- Duathlon (Natação + Corrida)
- Duathlon (Ciclismo + Corrida)

### Diferenciais
- Interface Flet moderna (material design, animações, mobile-ready)
- Wizard de 6 passos para criação de treinos
- Dashboard atleta-cêntrico com hero cards
- Calendário mensal interativo com drag & drop
- Adaptação automática ao ciclo menstrual
- Sistema de saúde com IA (HealthAdvisor)
- Periodização de 1 a 52 semanas
- Isolamento de dados por profissional (CREF)
- Exportação para Excel e PDF profissional
- Integração Strava/Garmin
- Sistema de notificações inteligente
- Modo escuro / claro
- Internacionalização (PT-BR, EN, ES)
- Empacotamento como executável standalone

---

## 2. Arquitetura do Projeto

```
D:\GitHub\App Treinos\Python\App Treinos\
│
├── App_Treinos_Flet.py         # ★ Launcher principal (Flet v3.0)
├── AppTreinos.bat              # Launcher Windows (duplo clique)
├── AppTreinos.sh               # Launcher Linux/macOS
├── build.py                    # Script de build (flet pack + PyInstaller)
├── AppTreinos.spec             # Spec PyInstaller
├── version.py                  # Versão semântica (3.0.0)
├── requirements.txt            # Dependências Python
│
├── assets/                     # ★ Ícones e assets visuais
│   ├── icon.ico                # Ícone Windows (16-256px)
│   ├── icon.png                # Ícone alta resolução (512px)
│   └── icon-192.png            # Ícone web/mobile (192px)
│
├── flet_app/                   # ★ Interface Flet (v3.0)
│   ├── main.py                 # Ponto de entrada + 13 rotas
│   ├── theme.py                # Tema visual (cores, tipografia)
│   ├── state.py                # Estado global (AppState)
│   ├── router.py               # Navegação entre ecrãs
│   ├── screens/                # 11 ecrãs
│   │   ├── splash.py           # Splash screen animado
│   │   ├── login.py            # Autenticação
│   │   ├── register.py         # Registo de treinador
│   │   ├── dashboard.py        # Painel principal (hero cards)
│   │   ├── athlete_dashboard.py# Dashboard individual do atleta
│   │   ├── training_wizard.py  # Wizard 6 passos
│   │   ├── templates.py        # Biblioteca de templates
│   │   ├── progress.py         # Estatísticas e changelog
│   │   ├── fitness.py          # Integração Strava/Garmin
│   │   ├── config.py           # Configurações (tema, idioma)
│   │   └── admin.py            # Administração de utilizadores
│   ├── components/             # 7 componentes reutilizáveis
│   │   ├── nav_bar.py          # Barra de navegação inferior
│   │   ├── athlete_card.py     # Hero card de atleta
│   │   ├── plan_card.py        # Card de plano de treino
│   │   ├── calendar_view.py    # Calendário mensal + drag & drop
│   │   ├── workout_editor.py   # Editor inline de treino
│   │   ├── template_card.py    # Card de template
│   │   └── notification_panel.py # Painel de notificações
│   └── services/
│       └── notification_engine.py # Motor de notificações
│
├── core/                       # Lógica de negócio
│   ├── training_engine.py      # Motor de geração de treinos
│   └── database.py             # SQLite/MySQL + autenticação
│
├── training_planner.py         # CLI + classes base (Athlete, TrainerInfo, etc.)
├── training_manager.py         # Gestão de planos, calendário, templates
├── pdf_exporter.py             # Exportação PDF (reportlab)
├── fitness_connectors.py       # Conectores Strava/Garmin
├── i18n.py                     # Internacionalização (PT-BR, EN, ES)
│
├── gui/                        # Interface Tkinter (v2.0 — legado)
│   ├── main_gui.py, theme.py, wizard_steps.py, ...
│
├── tests/                      # ★ 189 testes automatizados
│   ├── test_app_treinos.py     # Testes de integração
│   ├── test_funcionalidades.py # 84 testes funcionalidades
│   └── test_flet_backend.py    # 31 testes backend Flet
│
├── data/
│   ├── exports/                # Planilhas exportadas
│   └── trainers/               # Diretórios por treinador (CREF)
│
├── docs/                       # 23 documentos técnicos
├── scripts/                    # Scripts utilitários + gerador de ícone
├── linux/                      # Launcher + .desktop Linux
└── macos/                      # Scripts macOS
```

---

## 3. Histórico de Commits

| Data | Commit | Versão | Descrição |
|---|---|---|---|
| 12/03/2026 | `e252a92` | — | Arquivos base — estrutura inicial |
| 13/03/2026 | `5cf00a0` | — | Atualizações de 13/03 |
| 19/03/2026 | `bd9cade` | — | GUI e sistema de identificação profissional |
| 22/03/2026 | `2f68ba7` | — | Refatoração completa: remover duplicação |
| 22/03/2026 | `1d576e7` | — | Modernização GUI: animações, bordas arredondadas |
| 22/03/2026 | `599a271` | — | Modernização GUI (continuação) |
| 22/03/2026 | `e0cc841` | — | Documentação da modernização da GUI |
| 27/03/2026 | `6fdcb21` | — | Dívida técnica: unificação, testes, .gitignore |
| 27/03/2026 | `7489aee` | **v2.0.0** | CI/CD pipeline e versionamento semântico |
| 27/03/2026 | `05f922f` | — | Dashboard de progresso com estatísticas |
| 27/03/2026 | `c9eaa01` | — | Histórico de alterações (changelog) |
| 27/03/2026 | `11c04e5` | — | Internacionalização (PT-BR, EN, ES) |
| 27/03/2026 | `4610042` | — | Modo escuro acessível |
| 27/03/2026 | `c733bac` | — | Integração Strava/Garmin |
| 27/03/2026 | `b69cf9f` | **v2.1.0** | Empacotamento PyInstaller + bump v2.1.0 |
| 27/03/2026 | `b1ee6ce` | — | Suite completa de testes (84 testes) |
| 27/03/2026 | `468c3d5` | **v3.0.0** | Migração completa para Flet — UI atleta-cêntrica |
| 28/03/2026 | `09c2897` | — | Fix: register_training no wizard + entry.details |
| 28/03/2026 | `71f1357` | — | Organização raiz, ícone, build executável |
| 28/03/2026 | *pendente* | — | Limpeza: remover gui/ legado, scripts/docs redundantes, fix theme ← **HEAD** |

---

## 4. Estado Atual (28/03/2026)

### O que está PRONTO (✅)

- [x] Motor de geração de treinos (6 modalidades, periodização completa)
- [x] Interface Flet v3.0 com 11 ecrãs e 7 componentes reutilizáveis
- [x] Dashboard atleta-cêntrico com hero cards e busca
- [x] Calendário mensal interativo com drag & drop
- [x] Wizard de 6 passos para criação de planos
- [x] Sistema de notificações inteligente
- [x] Tema material com modo escuro/claro
- [x] Sistema de autenticação (CPF + CREF + senha)
- [x] Banco de dados SQLite com suporte a MySQL
- [x] Isolamento de dados por profissional (diretórios por CREF)
- [x] Exportação Excel (openpyxl) e PDF profissional (reportlab)
- [x] Adaptação ao ciclo menstrual
- [x] Sistema de saúde com IA (HealthAdvisor)
- [x] Cálculo automático de semanas até a prova
- [x] Integração Strava/Garmin
- [x] Internacionalização (PT-BR, EN, ES)
- [x] Biblioteca de templates reutilizáveis
- [x] Painel de administração de utilizadores
- [x] Suporte multiplataforma (Windows, Linux, macOS)
- [x] 192 testes automatizados passando (pytest)
- [x] Ícone profissional (.ico + .png, múltiplas resoluções)
- [x] Launchers: Windows (.bat), Linux/macOS (.sh), .desktop
- [x] Build system (flet pack + PyInstaller) com ícone
- [x] Documentação curada (9 documentos técnicos essenciais em docs/)

### Correções aplicadas em 28/03/2026

- **training_wizard.py**: `register_training` era chamado com kwargs inválidos e retorno tratado como tuple — corrigido para `register_training(trainer_info, athlete)` → `TrainingRecord`
- **progress.py**: campo `entry.detail` (sem 's') era sempre vazio — corrigido para `entry.details`

### Limpeza aplicada em 28/03/2026

- **gui/ removido** — Interface Tkinter legada (preservada em histórico Git)
- **scripts/ limpo** — 15 scripts redundantes removidos (mantido `generate_icon.py`)
- **docs/ limpo** — 13 documentos obsoletos removidos (mantidos 9 essenciais)
- **core/archived/, docs/archived/, scripts/archived/ removidos** — Backups antigos
- **theme.py corrigido** — Removido `surface_variant` (deprecated em Flet 0.83)
- **Testes atualizados** — Referências a `gui/` migradas para `flet_app/` (192 testes)

---

## 5. Tecnologias

| Componente | Tecnologia | Versão Requerida |
|---|---|---|
| Linguagem | Python | 3.10+ |
| GUI | **Flet** (Flutter) | >= 0.25.0 |
| Dados tabulares | pandas | >= 2.0.0 |
| Export Excel | openpyxl | >= 3.1.0 |
| Export PDF | reportlab | >= 4.0.0 |
| Banco de dados | SQLite | (nativo) |
| Banco de dados (prod) | MySQL | opcional |
| Build executável | PyInstaller / flet pack | >= 6.0.0 |

---

## 6. Como Executar

### Desenvolvimento (Python)
```bash
# Windows (duplo clique)
AppTreinos.bat

# Windows (terminal)
python App_Treinos_Flet.py

# Linux / macOS
./AppTreinos.sh
# ou: python3 App_Treinos_Flet.py
```

### Gerar Executável
```bash
# Executável em pasta (mais rápido de gerar)
python build.py

# Executável único (um só ficheiro .exe)
python build.py --onefile

# Limpar artefatos de build
python build.py --clean
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

### Correções e Melhorias Técnicas
1. ~~**Resolver duplicação** entre `training_planner.py` e `core/training_engine.py`~~ (mitigado — Flet usa `training_planner.py` diretamente)
2. ~~**Consolidar testes** — suíte com pytest~~ ✅ 189 testes em `tests/`
3. ~~**Dashboard de progresso**~~ ✅ `flet_app/screens/progress.py`
4. ~~**Histórico de alterações**~~ ✅ Changelog system
5. ~~**Integração com APIs de saúde**~~ ✅ Strava/Garmin
6. ~~**Multi-idioma**~~ ✅ PT-BR, EN, ES (i18n.py)
7. ~~**Modo escuro**~~ ✅ Dark/Light toggle
8. ~~**Empacotamento executável**~~ ✅ build.py + flet pack + ícone

### Funcionalidades Potenciais
9. **Sincronização cloud** — backup e sincronização de dados entre dispositivos
10. **Relatórios avançados** — gráficos de evolução e comparação de períodos
11. **Publicação como app mobile** — Flet suporta compilação para Android/iOS
12. **Marketplace de templates** — partilha de templates entre treinadores

### Infraestrutura
13. ~~**CI/CD**~~ ✅ GitHub Actions pipeline
14. ~~**Versionamento semântico**~~ ✅ v3.0.0
15. **Publicação PyPI** — distribuição via `pip install app-treinos`
16. **Assinatura de código** — codesign para distribuição Windows/macOS

---

*Este documento serve como ponto de orientação para retomar o desenvolvimento. Atualize-o ao final de cada sessão de trabalho.*
