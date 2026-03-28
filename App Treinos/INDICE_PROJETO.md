# 📚 Índice do Projeto - App Treinos

## 📁 Estrutura Principal

### 🚀 Executáveis
- `App_Treinos_Flet.py` - Launcher Flet (v3.0 — recomendado)
- `App_Treinos_GUI.bat` - Executável Windows (GUI Tkinter)
- `App_Treinos_GUI.py` - Launcher Python (GUI Tkinter)
- `App_Treinos.bat` - Executável Windows (CLI)
- `training_planner.py` - Aplicação CLI principal

### 💻 Código Fonte

#### Flet (Interface v3.0)
- `flet_app/main.py` - **Ponto de entrada + rotas**
- `flet_app/theme.py` - Tema visual (cores, tipografia)
- `flet_app/state.py` - Estado global (AppState)
- `flet_app/router.py` - Navegação entre ecrãs

##### Ecrãs (`flet_app/screens/`)
- `splash.py` - Splash screen
- `login.py` - Autenticação de treinador
- `register.py` - Registo de novo treinador
- `dashboard.py` - Painel principal (hero cards)
- `athlete_dashboard.py` - Dashboard individual do atleta
- `training_wizard.py` - Wizard de criação de plano (6 passos)
- `templates.py` - Biblioteca de templates
- `progress.py` - Estatísticas e changelog
- `fitness.py` - Integração Strava/Garmin
- `config.py` - Configurações
- `admin.py` - Administração

##### Componentes (`flet_app/components/`)
- `nav_bar.py` - Barra de navegação inferior
- `athlete_card.py` - Hero card de atleta
- `plan_card.py` - Card de plano de treino
- `calendar_view.py` - Calendário mensal + drag & drop
- `workout_editor.py` - Editor inline de treino
- `template_card.py` - Card de template
- `notification_panel.py` - Painel de notificações

##### Serviços (`flet_app/services/`)
- `notification_engine.py` - Motor de notificações

#### GUI Tkinter (Interface v2.0 — legado)
- `gui/main_gui.py` - Interface principal unificada
- `gui/theme.py` - Paleta de cores e estilos
- `gui/wizard_steps.py` - Etapas do wizard

#### Core (Lógica de Negócio)
- `core/training_engine.py` - Engine de geração de treinos
- `training_planner.py` - CLI e lógica principal
- `training_manager.py` - Gestão de planos, calendário, templates

### 📊 Dados
- `data/exports/` - Planilhas exportadas
- `requirements.txt` - Dependências Python

### 📖 Documentação Ativa

#### Guias de Uso
- `docs/COMO_EXECUTAR.md` - Como executar o app
- `docs/GUI_V2_DESIGN.md` - Design da interface v2.0
- `docs/IDENTIFICACAO_PROFISSIONAL.md` - Sistema de autenticação

#### Funcionalidades
- `docs/PERIODIZACAO_COMPLETA.md` - Sistema de periodização
- `docs/CICLO_MENSTRUAL.md` - Adaptação ao ciclo menstrual
- `docs/CALCULO_AUTOMATICO_SEMANAS.md` - Cálculo de semanas
- `docs/MENSAGENS_LIMITE_SISTEMA.md` - Validações e limites

#### Técnicos
- `docs/COMPATIBILIDADE_MULTIPLATAFORMA.md` - Windows, macOS, Linux
- `docs/ESTRUTURA_DIRETORIOS.md` - Organização de pastas
- `docs/UNIFICACAO_GUI.md` - Unificação da interface

### 🧪 Testes Automatizados
- `tests/test_funcionalidades.py` - 158 testes (inserção, i18n, modo escuro, fitness, etc.)
- `tests/test_flet_backend.py` - 31 testes (summary, calendário, overrides, templates, notificações)
- `tests/test_app_treinos.py` - Testes de integração

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
