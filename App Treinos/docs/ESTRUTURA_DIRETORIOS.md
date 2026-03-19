# 📁 Estrutura de Diretórios - App Treinos

## 🗂️ Organização do Projeto

```
App Treinos/
│
├── 📱 gui/                       # Interface Gráfica
│   ├── __init__.py              # Módulo GUI
│   ├── theme.py                 # Tema acessível (WCAG AAA)
│   ├── main_gui.py              # Interface principal wizard
│   └── wizard_steps.py          # Etapas adicionais do assistente
│
├── ⚙️ core/                      # Motor do Aplicativo
│   ├── __init__.py
│   └── training_engine.py       # Lógica de treinamento (copiado de training_planner.py)
│
├── 💾 data/                      # Dados e Exportações
│   └── exports/                 # Planilhas Excel geradas
│       └── *.xlsx               # Planos de treinamento
│
├── 📚 docs/                      # Documentação
│   ├── GUI_MANUAL.md            # Manual da interface gráfica
│   ├── CALCULO_AUTOMATICO_SEMANAS.md
│   ├── PERIODIZACAO_COMPLETA.md
│   ├── CICLO_MENSTRUAL.md
│   ├── MENSAGENS_LIMITE_SISTEMA.md
│   ├── COMPATIBILIDADE_MULTIPLATAFORMA.md
│   ├── EXECUCAO_DUPLO_CLIQUE.md
│   └── INDICE_PROJETO.md
│
├── 🔧 scripts/                   # Scripts Auxiliares
│   ├── teste_calculo_semanas.py
│   ├── teste_ia_saude.py
│   ├── demo_mensagens_limite.py
│   ├── demo_melhorias_entrada.py
│   ├── demo_execucao_rapida.py
│   ├── exemplo_calculo_automatico.py
│   ├── comparacao_modos_configuracao.py
│   ├── resumo_implementacao.py
│   └── exemplos.py
│
├── 🐧 linux/                     # Scripts Linux
│   ├── instalar.sh
│   ├── executar.sh
│   ├── exemplos.sh
│   ├── app_treinos_launcher.sh
│   ├── App_Treinos.desktop
│   └── README.md
│
├── 🍎 macos/                     # Scripts macOS
│   ├── instalar.sh
│   ├── executar.sh
│   ├── exemplos.sh
│   └── README.md
│
├── 🚀 Launchers (EXECUTAR AQUI)
│   ├── App_Treinos_GUI.py       # 🖥️ Launcher GUI (Python)
│   ├── App_Treinos_GUI.bat      # 🖥️ Launcher GUI (Windows)
│   ├── App_Treinos.bat          # 💻 Launcher CLI (Windows)
│   ├── App_Treinos.command      # 💻 Launcher CLI (macOS)
│   └── training_planner.py      # 💻 CLI Original
│
└── 📄 Arquivos de Configuração
    ├── requirements.txt         # Dependências Python
    ├── AppTreinosCode.code-workspace
    ├── README.md                # Este arquivo
    └── LEIA-ME_EXECUCAO_RAPIDA.txt
```

---

## 🎯 Onde Executar

### Interface Gráfica (GUI) - RECOMENDADO
```
Windows: App_Treinos_GUI.bat (duplo clique)
Linux/Mac: python3 App_Treinos_GUI.py
```

### Linha de Comando (CLI) - Legado
```
Windows: App_Treinos.bat (duplo clique)
macOS: App_Treinos.command (duplo clique)
Linux: ./linux/executar.sh
```

---

## 📂 Propósito de Cada Diretório

### `/gui` - Interface Gráfica
**Contém:** Código da interface visual moderna e acessível
**Quando usar:** Código relacionado à apresentação visual

### `/core` - Lógica Principal
**Contém:** Motor de treinamento, algoritmos de periodização, IA de saúde
**Quando usar:** Código de negócio independente da interface

### `/data` - Dados e Exportações
**Contém:** Arquivos Excel gerados, cache (futuro), histórico (futuro)
**Quando usar:** Armazenar dados persistentes

### `/docs` - Documentação
**Contém:** Manuais, guias, documentação técnica
**Quando usar:** Ler sobre funcionalidades ou buscar ajuda

### `/scripts` - Utilitários
**Contém:** Testes, demos, exemplos, ferramentas auxiliares
**Quando usar:** Testar funcionalidades ou ver exemplos práticos

### `/linux` e `/macos` - Scripts Específicos de OS
**Contém:** Scripts de instalação e execução otimizados
**Quando usar:** Executar em Linux ou macOS

---

## 🔄 Caminhos Atualizados

### Importações (Python)
```python
# Antes
import training_planner

# Agora
from core import training_engine
from gui import theme, main_gui
```

### Exportação de Dados
```python
# Antes
arquivo = f"{nome_atleta}_treinamento.xlsx"

# Agora
from pathlib import Path
data_dir = Path(__file__).parent / 'data' / 'exports'
arquivo = data_dir / f"{nome_atleta}_treinamento.xlsx"
```

---

## 📊 Tipos de Arquivo por Diretório

| Diretório | Tipos de Arquivo | Exemplo |
|-----------|------------------|---------|
| `/gui` | `.py` (Interface) | `theme.py`, `main_gui.py` |
| `/core` | `.py` (Lógica) | `training_engine.py` |
| `/data` | `.xlsx`, `.db` (futuro) | `*.xlsx` |
| `/docs` | `.md`, `.pdf` (futuro) | `GUI_MANUAL.md` |
| `/scripts` | `.py` (Auxiliar) | `teste_*.py`, `demo_*.py` |
| `/linux` | `.sh`, `.desktop` | `instalar.sh` |
| `/macos` | `.sh`, `.command` | `executar.sh` |

---

## 🎨 Organização por Função

### 🎯 **Executáveis Principais** (Raiz)
- `App_Treinos_GUI.py` / `.bat` - Interface gráfica
- `training_planner.py` / `App_Treinos.bat` - CLI

### 🧠 **Lógica de Negócio** (`/core`)
- Classes de dados (Athlete, HealthIssue)
- Algoritmos de periodização
- IA de saúde
- Cálculos de zonas de treinamento
- Exportação Excel

### 🖼️ **Interface** (`/gui`)
- Tema acessível
- Wizard de coleta
- Validações visuais
- Diálogos e mensagens

### 💾 **Dados** (`/data`)
- Planilhas Excel exportadas
- Cache (futuro)
- Histórico de atletas (futuro)

### 📖 **Documentação** (`/docs`)
- Manuais de usuário
- Guias técnicos
- Tutoriais

### 🔧 **Utilitários** (`/scripts`)
- Testes unitários
- Demonstrações
- Exemplos de uso
- Ferramentas de desenvolvimento

---

## ✅ Checklist de Organização

### Arquivos no Lugar Certo?
- [ ] GUI em `/gui`
- [ ] Lógica em `/core`
- [ ] Exportações em `/data/exports`
- [ ] Docs em `/docs`
- [ ] Testes em `/scripts`

### Importações Atualizadas?
- [ ] Imports relativos corretos
- [ ] Paths absolutos quando necessário
- [ ] `sys.path` configurado em launchers

### Funcionalidade Preservada?
- [ ] CLI funciona
- [ ] GUI funciona
- [ ] Exportação para local correto
- [ ] Documentação acessível

---

## 🚀 Próximos Passos

1. **Finalizar migração** de arquivos `.md` para `/docs`
2. **Mover scripts** de teste/demo para `/scripts`
3. **Atualizar importações** no código legado
4. **Testar todos** os caminhos de arquivo
5. **Criar** subdiretor em `/data/exports`

---

## 📞 Suporte

Para dúvidas sobre a estrutura de diretórios, consulte:
- [docs/GUI_MANUAL.md](docs/GUI_MANUAL.md) - Manual da GUI
- [docs/INDICE_PROJETO.md](docs/INDICE_PROJETO.md) - Índice completo

---

**Versão:** 3.0 (Estrutura Organizada)  
**Data:** 13/03/2026  
**Organização:** Por tipo e função de arquivo
