# 📚 Índice do Projeto — App Treinos v3.0.0

## 📁 Estrutura Principal

### 🚀 Executáveis e Launchers
- `App_Treinos_Flet.py` — **Launcher principal** (Flet v3.0)
- `AppTreinos.bat` — Launcher Windows (duplo clique)
- `AppTreinos.sh` — Launcher Linux/macOS
- `build.py` — Gera executável standalone (flet pack + PyInstaller)
- `AppTreinos.spec` — Spec PyInstaller
- `training_planner.py` — CLI (modo terminal)

### 🎨 Assets
- `assets/icon.ico` — Ícone Windows (16–256px)
- `assets/icon.png` — Ícone alta resolução (512px)
- `assets/icon-192.png` — Ícone web/mobile (192px)

### 💻 Código Fonte

#### Flet (Interface v3.0 — ativa)
- `flet_app/main.py` — **Ponto de entrada + 13 rotas**
- `flet_app/theme.py` — Tema visual (cores, tipografia, modo escuro)
- `flet_app/state.py` — Estado global (AppState)
- `flet_app/router.py` — Navegação entre ecrãs

##### Ecrãs (`flet_app/screens/`)
- `splash.py` — Splash screen animado
- `login.py` — Autenticação de treinador
- `register.py` — Registo de novo treinador
- `dashboard.py` — Painel principal (hero cards + busca)
- `athlete_dashboard.py` — Dashboard individual do atleta
- `training_wizard.py` — Wizard de criação de plano (6 passos)
- `templates.py` — Biblioteca de templates
- `progress.py` — Estatísticas e changelog
- `fitness.py` — Integração Strava/Garmin
- `config.py` — Configurações (tema, idioma, logout)
- `admin.py` — Administração de utilizadores

##### Componentes (`flet_app/components/`)
- `nav_bar.py` — Barra de navegação inferior
- `athlete_card.py` — Hero card de atleta
- `plan_card.py` — Card de plano de treino
- `calendar_view.py` — Calendário mensal + drag & drop
- `workout_editor.py` — Editor modal de treino
- `template_card.py` — Card de template
- `notification_panel.py` — Painel de notificações (bell icon + BottomSheet)

##### Serviços (`flet_app/services/`)
- `notification_engine.py` — Motor de notificações inteligente

#### Core (Lógica de Negócio)
- `core/training_engine.py` — Engine de geração de treinos
- `core/database.py` — SQLite/MySQL + autenticação
- `training_planner.py` — CLI + classes base (Athlete, TrainerInfo, HealthIssue)
- `training_manager.py` — Gestão de planos, calendário, templates, changelog
- `fitness_connectors.py` — Conectores Strava/Garmin
- `pdf_exporter.py` — Exportação PDF profissional (reportlab)
- `i18n.py` — Internacionalização (PT-BR, EN, ES)
- `version.py` — Versão semântica

#### GUI Tkinter (Interface v2.0 — legado)
- `gui/` — Interface anterior (mantido para referência)

### 📊 Dados
- `data/exports/` — Planilhas exportadas
- `data/trainers/` — Diretórios por treinador (CREF)
- `requirements.txt` — Dependências Python

### 📖 Documentação
- `HISTORICO_CONTEXTO.md` — Histórico completo do projeto
- `README.md` — Visão geral
- `docs/` — 23 documentos técnicos (periodização, ciclo menstrual, etc.)

### 🧪 Testes Automatizados (189 testes)
- `tests/test_app_treinos.py` — Testes de integração (74 testes)
- `tests/test_funcionalidades.py` — Funcionalidades completas (84 testes)
- `tests/test_flet_backend.py` — Backend Flet (31 testes)

### 🧪 Scripts de Teste (Manuais)
- `scripts/teste_estrutura.py` - Valida estrutura de pastas
- `scripts/teste_validacao_profissional.py` - Testa validação CPF/CREF
- `scripts/teste_gui_final.py` - Testa GUI completa
- `scripts/teste_calculo_semanas.py` - Testa cálculo de datas

### 🧪 Scripts de Demonstração
- `scripts/demo_execucao_rapida.py` - Demo de uso rápido
- `scripts/demo_melhorias_entrada.py` - Demo de validações
- `scripts/exemplo_periodizacao.py` - Exemplo de periodização
- `scripts/exemplo_calculo_automatico.py` - Exemplo de cálculo

### 📦 Arquivados
- `docs/archived/` - Documentação antiga (referência)
- `scripts/archived/` - Scripts antigos (referência)

## 🎯 Como Começar

### Instalação
```bash
pip install -r requirements.txt
```

### Executar Interface Flet (v3.0)
```bash
python App_Treinos_Flet.py
```

### Executar GUI Tkinter (v2.0)
```bash
python gui/main_gui.py
```
ou duplo-clique em:
- Windows: `App_Treinos_GUI.bat`
- macOS: `App_Treinos.command`
- Linux: `linux/App_Treinos.sh`

### Executar CLI
```bash
python training_planner.py
```

## 📚 Documentação por Tópico

### Para Usuários
1. **Como Executar** → `docs/COMO_EXECUTAR.md`
2. **Interface Visual** → `docs/GUI_V2_DESIGN.md`
3. **Identificação Profissional** → `docs/IDENTIFICACAO_PROFISSIONAL.md`

### Para Desenvolvedores
1. **Estrutura do Projeto** → `docs/ESTRUTURA_DIRETORIOS.md`
2. **Compatibilidade** → `docs/COMPATIBILIDADE_MULTIPLATAFORMA.md`
3. **Periodização** → `docs/PERIODIZACAO_COMPLETA.md`
4. **Validações** → `docs/MENSAGENS_LIMITE_SISTEMA.md`

## 🔧 Manutenção

### Testes
```bash
# Executar todos os testes (189)
python -m pytest tests/ test_cli.py -v

# Apenas testes do backend Flet (31)
python -m pytest tests/test_flet_backend.py -v

# Testar estrutura
python scripts/teste_estrutura.py

# Testar validações
python scripts/teste_validacao_profissional.py

# Testar GUI
python scripts/teste_gui_final.py
```

### Limpeza
```bash
# Remover cache Python
python scripts/otimizar_projeto.py
```

---

**Última atualização:** Julho 2025  
**Versão:** 3.0
