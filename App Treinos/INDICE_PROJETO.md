# 📚 Índice do Projeto - App Treinos

## 📁 Estrutura Principal

### 🚀 Executáveis
- `App_Treinos_GUI.bat` - Executável Windows (GUI)
- `App_Treinos_GUI.py` - Launcher Python (GUI)
- `App_Treinos.bat` - Executável Windows (CLI)
- `training_planner.py` - Aplicação CLI principal

### 💻 Código Fonte

#### GUI (Interface Gráfica)
- `gui/main_gui.py` - **Interface principal unificada**
- `gui/theme.py` - Paleta de cores e estilos
- `gui/wizard_steps.py` - Etapas do wizard (placeholder)

#### Core (Lógica de Negócio)
- `core/training_engine.py` - Engine de geração de treinos
- `training_planner.py` - CLI e lógica principal

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

### 🧪 Scripts de Teste (Ativos)
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

### Executar GUI
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

**Última atualização:** 18/03/2026  
**Versão:** 2.0
