# 📚 Índice do Projeto — App Treinos v3.0.0

## 📁 Estrutura Principal

### 🚀 Executáveis e Launchers
- `App_Treinos_Flet.py` — **Launcher principal** (Flet v3.0)
- `AppTreinos.bat` — Launcher Windows (duplo clique)
- `AppTreinos.sh` — Launcher Linux/macOS
- `build.py` — Gera executável standalone (flet pack + PyInstaller)
- `AppTreinos.spec` — Spec PyInstaller
- `training_planner.py` — CLI (modo terminal)
- `dist/AppTreinos.exe` — Executável Windows (standalone)

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

### 📊 Dados
- `data/exports/` — Planilhas exportadas
- `data/trainers/` — Diretórios por treinador (CREF)
- `requirements.txt` — Dependências Python

### 📖 Documentação
- `HISTORICO_CONTEXTO.md` — Histórico completo do projeto
- `README.md` — Visão geral
- `docs/` — Documentação técnica (periodização, ciclo menstrual, etc.)

### 🧪 Testes Automatizados (192 testes)
- `tests/test_app_treinos.py` — Testes de integração
- `tests/test_funcionalidades.py` — Funcionalidades completas
- `tests/test_flet_backend.py` — Backend Flet

### 🔧 Scripts Utilitários
- `scripts/generate_icon.py` — Gerador de ícone do aplicativo

### 🖥️ Plataformas
- `linux/App_Treinos.desktop` — Atalho desktop Linux
- `macos/` — Recursos macOS

## 🎯 Como Começar

### Instalação
```bash
pip install -r requirements.txt
```

### Executar Interface Flet (v3.0)
```bash
python App_Treinos_Flet.py
```

### Executar como Software (Windows)
Duplo clique em `AppTreinos.bat` ou `dist/AppTreinos.exe`

### Executar CLI
```bash
python training_planner.py
```

### Gerar Executável
```bash
python build.py --onefile
```

## 📚 Documentação por Tópico

### Para Usuários
1. **Identificação Profissional** → `docs/IDENTIFICACAO_PROFISSIONAL.md`
2. **Periodização** → `docs/PERIODIZACAO_COMPLETA.md`
3. **Ciclo Menstrual** → `docs/CICLO_MENSTRUAL.md`

### Para Desenvolvedores
1. **Novas Funcionalidades** → `docs/NOVAS_FUNCIONALIDADES.md`
2. **Sistema de Autenticação** → `docs/SISTEMA_AUTENTICACAO.md`
3. **Validações** → `docs/MENSAGENS_LIMITE_SISTEMA.md`

## 🔧 Manutenção

### Testes
```bash
# Executar todos os testes (192)
python -m pytest tests/ -v

# Apenas testes do backend Flet
python -m pytest tests/test_flet_backend.py -v
```

---

**Última atualização:** Julho 2025  
**Versão:** 3.0.0
