# 🍎 App Treinos - Versão para macOS

## 📋 Instalação Rápida

### 1. Tornar os scripts executáveis
```bash
cd "App Treinos"
chmod +x macos/*.sh
```

### 2. Executar instalação
```bash
./macos/instalar.sh
```

### 3. Executar o sistema
```bash
./macos/executar.sh
```

---

## 🚀 Comandos Disponíveis

### Executar o Sistema Principal
```bash
./macos/executar.sh
```

### Menu de Exemplos
```bash
./macos/exemplos.sh
```

### Instalação Manual
```bash
pip3 install --user pandas openpyxl
python3 training_planner.py
```

---

## 🔧 Pré-requisitos para macOS

### Instalar Python (se necessário)

**Opção 1: Homebrew (Recomendado)**
```bash
# Instalar Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python3
```

**Opção 2: Download Direto**
- Baixe de: https://www.python.org/downloads/macos/
- Execute o instalador `.pkg`

---

## 📦 Dependências

- **Python 3.8+**
- **pandas >= 2.0.0**
- **openpyxl >= 3.1.0**

---

## 🐛 Solução de Problemas

### Problema: "permission denied"
```bash
chmod +x macos/*.sh
```

### Problema: "python3 não encontrado"
```bash
# Instalar via Homebrew
brew install python3

# Ou baixar de python.org
```

### Problema: Erro de encoding UTF-8
Os scripts já configuram UTF-8 automaticamente. Se precisar configurar manualmente:
```bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

### Problema: "zsh: command not found: pip3"
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user
rm get-pip.py
```

### Problema: Erro de permissão no Catalina+
```bash
# Se usar Gatekeeper, pode precisar autorizar:
xattr -d com.apple.quarantine macos/*.sh
```

---

## 📁 Estrutura de Arquivos

```
macos/
├── instalar.sh      # Script de instalação
├── executar.sh      # Executa o sistema principal
├── exemplos.sh      # Menu de exemplos
└── README.md        # Este arquivo
```

---

## 💡 Dicas de Uso

### Criar Alias (Opcional)
Adicione ao seu `~/.zshrc` (macOS Catalina+) ou `~/.bash_profile`:
```bash
alias treinos='cd /Users/seu-usuario/App\ Treinos && ./macos/executar.sh'
alias treinos-exemplos='cd /Users/seu-usuario/App\ Treinos && ./macos/exemplos.sh'
```

Depois execute:
```bash
source ~/.zshrc  # ou ~/.bash_profile
```

Agora você pode executar de qualquer lugar:
```bash
treinos
treinos-exemplos
```

### Terminal.app vs iTerm2
Ambos funcionam perfeitamente. Se usar iTerm2, considere:
- Perfil de cores com suporte a emoji
- Fonte com símbolos: Menlo, Monaco ou Fira Code

---

## 🎯 Recursos do Sistema

- ✅ Cálculo automático de semanas por data
- ✅ Periodização profissional (1-52 semanas)
- ✅ Adaptação para ciclo menstrual
- ✅ IA de saúde para lesões
- ✅ Exportação Excel completa
- ✅ Mensagens educativas de limite

---

## 🍎 Específico para macOS

### Versões Testadas
- ✅ macOS Monterey (12.x)
- ✅ macOS Ventura (13.x)
- ✅ macOS Sonoma (14.x)

### Shells Suportados
- ✅ zsh (padrão no macOS Catalina+)
- ✅ bash

### Apple Silicon (M1/M2/M3)
O sistema funciona nativamente em chips Apple Silicon.

---

## 📞 Suporte

Para problemas específicos do macOS, verifique:
1. Versão do macOS: Menu Apple → Sobre este Mac
2. Versão do Python: `python3 --version`
3. Versão do pip: `pip3 --version`
4. Shell ativo: `echo $SHELL`

---

**Versão:** 2.3 macOS  
**Última atualização:** 13/03/2026
