# 📱 App Treinos - Planejador de Treinos Personalizado

**Versão 3.0 — Interface Flet (Flutter/Python)**

Sistema inteligente de planejamento de treinos esportivos com UI atleta-cêntrica, calendário interativo, drag & drop, templates reutilizáveis e notificações.

---

## 🎯 Características Principais

### ✨ Interface Flet — Atleta-Cêntrica
- **Hero Cards** por atleta com status em tempo real
- **Calendário mensal** com chips coloridos por zona de treino
- **Edição inline** de treinos via modal/popup
- **Drag & Drop** para reorganizar sessões entre dias
- **Templates reutilizáveis** de treinos (pessoais + sistema)
- **Notificações** inteligentes (treinos hoje/amanhã, prazos, inativos)

### 🏃 Planejamento Inteligente
- Periodização de **1 a 52 semanas**
- **Wizard de 6 passos** para criação de planos
- **Adaptação automática** ao ciclo menstrual
- Consideração de **problemas de saúde** ortopédicos/sistêmicos
- **Múltiplas modalidades:** Corrida, Ciclismo, Triathlon, Natação

### 📊 Exportação Profissional
- Planilhas Excel completas
- Semanas, dias e treinos detalhados
- Zonas de treinamento (FC, velocidade, potência)
- Observações de adaptação ao ciclo

---

## 🚀 Como Usar

### Interface Flet (v3.0 — recomendado)
```bash
python App_Treinos_Flet.py
```

### Interface Tkinter (v2.0 — legado)
```batch
# Windows — Duplo clique em:
App_Treinos_GUI.bat
```

### Linux/macOS
```bash
python3 App_Treinos_Flet.py   # Flet
python3 App_Treinos_GUI.py    # Tkinter
```

📖 **[Guia Completo de Execução](docs/COMO_EXECUTAR.md)**

---

## 📋 Requisitos

- **Python 3.8+** (testado até 3.14)
- **Bibliotecas:**
  - flet >= 0.25.0
  - pandas >= 2.0.0
  - openpyxl >= 3.1.0

### Instalação

```bash
pip install -r requirements.txt
```

---

## 📁 Estrutura do Projeto

```
App Treinos/
├── flet_app/                # Interface Flet (v3.0)
│   ├── main.py              # Ponto de entrada + rotas
│   ├── theme.py             # Tema visual (cores, tipografia)
│   ├── state.py             # Estado global (AppState)
│   ├── router.py            # Navegação entre ecrãs
│   ├── screens/             # Ecrãs da aplicação
│   │   ├── splash.py        # Splash screen
│   │   ├── login.py         # Autenticação
│   │   ├── register.py      # Registo de treinador
│   │   ├── dashboard.py     # Painel principal (hero cards)
│   │   ├── athlete_dashboard.py  # Dashboard individual
│   │   ├── training_wizard.py    # Wizard de criação de plano
│   │   ├── templates.py     # Biblioteca de templates
│   │   ├── progress.py      # Estatísticas e changelog
│   │   ├── fitness.py       # Integração Strava/Garmin
│   │   ├── config.py        # Configurações
│   │   └── admin.py         # Administração
│   ├── components/          # Componentes reutilizáveis
│   │   ├── nav_bar.py       # Barra de navegação
│   │   ├── athlete_card.py  # Hero card de atleta
│   │   ├── plan_card.py     # Card de plano
│   │   ├── calendar_view.py # Calendário mensal + drag & drop
│   │   ├── workout_editor.py # Editor inline de treino
│   │   ├── template_card.py # Card de template
│   │   └── notification_panel.py # Painel de notificações
│   └── services/            # Serviços de backend UI
│       └── notification_engine.py # Motor de notificações
├── gui/                     # Interface Tkinter (v2.0 legado)
├── core/                    # Lógica de treinos
├── data/                    # Exportações
├── tests/                   # Testes automatizados (189 testes)
├── docs/                    # Documentação
├── scripts/                 # Utilitários
├── linux/                   # Scripts Linux
└── macos/                   # Scripts macOS
```

---

## 🎨 Wizard de 6 Passos

1. **Dados Básicos** → Nome, idade, peso, altura, gênero
2. **Modalidade** → Esporte e disponibilidade
3. **Período** → Data da prova ou semanas
4. **Distância** → Distância e fisiologia (limiar, VO2 max)
5. **Saúde** → Problemas ortopédicos/sistêmicos
6. **Ciclo Menstrual** → Adaptações para mulheres

---

## 💡 Principais Funcionalidades

### 🔬 Adaptação ao Ciclo Menstrual
- **Fase Folicular:** Treinos de alta intensidade
- **Ovulação:** Pico de performance
- **Fase Lútea:** Redução de intensidade, foco em volume
- **Menstruação:** Recuperação ativa

### 🏥 Considerações de Saúde
- Adaptação automática para problemas ortopédicos
- Redução de intensidade para condições sistêmicas
- Recomendações médicas integradas

### 📈 Periodização Científica
- Base → Construção → Intensificação → Recuperação → Pico
- Progressão gradual de volume e intensidade
- Zonas de treino baseadas em FC/velocidade/potência

---

## 🎯 Público-Alvo

- **Profissionais de Educação Física**
- **Treinadores esportivos**
- **Preparadores físicos**
- **Atletas autodidatas**

---

## 📚 Documentação

- **[Como Executar](docs/COMO_EXECUTAR.md)** - Guia de instalação e execução
- **[Manual da GUI](docs/GUI_MANUAL.md)** - Documentação completa da interface
- **[Estrutura de Diretórios](docs/ESTRUTURA_DIRETORIOS.md)** - Organização do projeto
- **[Resumo da Implementação](docs/RESUMO_IMPLEMENTACAO.md)** - Detalhes técnicos
- **[Novas Funcionalidades](docs/NOVAS_FUNCIONALIDADES.md)** - Histórico de recursos

---

## ✅ Status de Testes

| Componente | Testes | Status |
|-----------|--------|--------|
| Inserção de dados | 5 | ✅ |
| Isolamento treinadores | 5 | ✅ |
| Remoção de planos | 4 | ✅ |
| Estatísticas & Changelog | 9 | ✅ |
| i18n (PT/EN/ES) | 12 | ✅ |
| Modo Escuro | 4 | ✅ |
| Fitness Connectors | 6 | ✅ |
| Navegação & Dashboard | 7 | ✅ |
| Versionamento | 2 | ✅ |
| Athletes Summary | 6 | ✅ |
| Calendário & Move | 7 | ✅ |
| Workout Overrides | 7 | ✅ |
| Templates CRUD | 6 | ✅ |
| Notificações | 5 | ✅ |
| **Total** | **189** | **✅ 100%** |

---

## 🌟 Diferenciais

### CLI vs GUI

| Característica | CLI | GUI |
|---------------|-----|-----|
| Facilidade de uso | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Acessibilidade | ⭐ | ⭐⭐⭐⭐⭐ |
| Feedback visual | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Navegação | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Profissionalismo | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔧 Desenvolvimento

### Tecnologias

- **Python 3.8+** - Linguagem
- **Flet 0.25+** - Interface gráfica (Flutter/Python)
- **Tkinter** - Interface legada (v2.0)
- **Pandas** - Manipulação de dados
- **OpenPyXL** - Exportação Excel

### Padrões de Projeto

- **Router Pattern** - Navegação entre ecrãs
- **AppState** - Estado global centralizado
- **Wizard Pattern** - Criação de planos passo a passo
- **Theme Pattern** - Centralização de estilos
- **Override Pattern** - Edição inline sobre calendário base

---

## 📊 Métricas de Performance

- **Inicialização:** < 0.5s
- **Validação:** Instantânea
- **Geração de plano:** < 2s
- **Exportação Excel:** < 1s

---

## 🆘 Suporte

### Problemas Comuns

**GUI não abre:**
```bash
# Teste a estrutura
python scripts/teste_estrutura.py

# Verifique dependências
pip install -r requirements.txt
```

**Erros de importação:**
```bash
# Execute do diretório raiz
cd "caminho/para/App Treinos"
python App_Treinos_GUI.py
```

📖 **[Guia Completo de Solução de Problemas](docs/COMO_EXECUTAR.md#-solução-de-problemas)**

---

## 📜 Licença

Desenvolvido para uso educacional e profissional em Educação Física.

---

## 🎉 Versão 3.0 — Flet Migration

✅ Interface Flet atleta-cêntrica (hero cards + dashboard individual)  
✅ Calendário mensal interativo com chips coloridos  
✅ Edição inline de treinos via modal  
✅ Drag & Drop entre dias  
✅ Templates reutilizáveis (pessoais + sistema)  
✅ Motor de notificações inteligentes  
✅ Integração Strava/Garmin (leitura)  
✅ 189 testes automatizados  
✅ i18n em 3 idiomas (PT/EN/ES)  
✅ Navegação por rotas com Router/AppState  

### Versões Anteriores

- **v2.1** — Dashboard, fitness connectors, modo escuro, i18n  
- **v2.0** — Interface gráfica Tkinter completa  
- **v1.0** — CLI interativa  

---

**Desenvolvido com 💙 para profissionais de Educação Física**

**Versão:** 3.0  
**Data:** Julho 2025  
**Status:** ✅ Pronto para produção
