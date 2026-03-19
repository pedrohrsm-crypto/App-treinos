# 🚀 Como Executar - App Treinos

## Guia Rápido de Execução

---

## 🪟 Windows

### Opção 1: Duplo Clique (Mais Fácil)

1. Localize o arquivo `App_Treinos_GUI.bat` na pasta do projeto
2. Dê **duplo clique** nele
3. A GUI será aberta automaticamente

### Opção 2: Terminal/PowerShell

```batch
# Navegue até a pasta do projeto
cd "d:\GitHub\Python\Python\App Treinos"

# Execute o launcher
App_Treinos_GUI.bat
```

### Opção 3: Python Diretamente

```bash
# Navegue até a pasta do projeto
cd "d:\GitHub\Python\Python\App Treinos"

# Execute com Python
python App_Treinos_GUI.py
```

---

## 🐧 Linux

### Opção 1: Script de Execução

```bash
# Navegue até a pasta do projeto
cd ~/App\ Treinos

# Execute o script Linux
./linux/executar.sh
```

### Opção 2: Python Diretamente

```bash
# Navegue até a pasta do projeto
cd ~/App\ Treinos

# Execute com Python
python3 App_Treinos_GUI.py
```

---

## 🍎 macOS

### Opção 1: Script de Execução

```bash
# Navegue até a pasta do projeto
cd ~/App\ Treinos

# Execute o script macOS
./macos/executar.sh
```

### Opção 2: Launcher .command

```bash
# Duplo clique em:
App_Treinos.command
```

### Opção 3: Python Diretamente

```bash
# Navegue até a pasta do projeto
cd ~/App\ Treinos

# Execute com Python
python3 App_Treinos_GUI.py
```

---

## 📋 Pré-requisitos

### Python

- **Versão mínima:** Python 3.8
- **Versão testada:** Python 3.14.0
- **Recomendado:** Python 3.10+

### Verificar Versão Python

```bash
# Windows
python --version

# Linux/macOS
python3 --version
```

### Instalar Dependências

```bash
# Windows
pip install -r requirements.txt

# Linux/macOS
pip3 install -r requirements.txt
```

**Dependências necessárias:**
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- tkinter (já vem com Python)

---

## 🔧 Solução de Problemas

### "Python não encontrado"

**Windows:**
```batch
# Instale Python do site oficial
https://www.python.org/downloads/

# Durante instalação, marque:
☑ Add Python to PATH
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

**macOS:**
```bash
brew install python@3.11
```

### "ModuleNotFoundError: No module named 'pandas'"

```bash
# Instale as dependências
pip install pandas openpyxl

# Ou use o requirements.txt
pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'tkinter'"

**Linux:**
```bash
sudo apt install python3-tk
```

**macOS:**
```bash
# Reinstale Python com suporte tk
brew reinstall python-tk@3.11
```

**Windows:**
- Tkinter já vem instalado com Python
- Se não funcionar, reinstale Python marcando "tcl/tk and IDLE"

### GUI não abre / Fecha imediatamente

1. Execute via terminal para ver erros:
   ```bash
   python App_Treinos_GUI.py
   ```

2. Verifique se todas dependências estão instaladas:
   ```bash
   python scripts/teste_estrutura.py
   ```

3. Verifique permissões dos arquivos (Linux/macOS):
   ```bash
   chmod +x linux/*.sh
   chmod +x macos/*.sh
   ```

### Caracteres estranhos no Windows (encoding)

O arquivo `.bat` já está configurado com UTF-8. Se ainda houver problemas:

1. Abra PowerShell como Administrador
2. Execute:
   ```powershell
   Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Nls\CodePage' -Name 'ACP' -Value '65001'
   Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Nls\CodePage' -Name 'OEMCP' -Value '65001'
   ```
3. Reinicie o computador

---

## 📊 Verificar Instalação

Execute o teste de estrutura:

```bash
# Windows
python scripts\teste_estrutura.py

# Linux/macOS
python3 scripts/teste_estrutura.py
```

**Saída esperada:**
```
🎉 TUDO OK! O aplicativo está pronto para uso.
```

---

## 🎯 Execução Passo a Passo

### Primeira Execução

1. **Instale Python** (se ainda não tiver)
2. **Baixe/Clone o projeto**
3. **Abra terminal na pasta do projeto**
4. **Instale dependências:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Execute:**
   - Windows: Duplo clique em `App_Treinos_GUI.bat`
   - Linux/macOS: `python3 App_Treinos_GUI.py`

### Execuções Seguintes

- Basta executar o launcher (.bat no Windows, .sh no Linux/macOS)
- Ou dar duplo clique no arquivo apropriado

---

## 💡 Dicas

### Performance

- **Primeira execução:** Pode demorar 1-2 segundos (carregando bibliotecas)
- **Execuções seguintes:** < 0.5 segundos

### Atalhos

**Windows - Criar atalho na Área de Trabalho:**
1. Clique direito em `App_Treinos_GUI.bat`
2. Enviar para > Área de trabalho (criar atalho)
3. Renomeie para "App Treinos"

**Linux - Criar launcher de aplicativo:**
```bash
cp linux/App_Treinos_GUI.desktop ~/.local/share/applications/
```

**macOS - Adicionar ao Dock:**
1. Arraste `App_Treinos.command` para o Dock
2. Ou crie um Automator App Wrapper

---

## 📱 Ambientes Testados

✅ Windows 10/11  
✅ Ubuntu 20.04+  
✅ macOS Big Sur+  
✅ Python 3.8 - 3.14  

---

## 🆘 Suporte

### Logs de Erro

Se a GUI não abrir, execute via terminal e copie a saída:

```bash
python App_Treinos_GUI.py 2>&1 | tee erro.log
```

O arquivo `erro.log` terá todas as mensagens de erro.

### Informações do Sistema

Para reportar problemas, inclua:

```bash
# Versão Python
python --version

# Versão das bibliotecas
pip list | grep -E "pandas|openpyxl"

# Sistema operacional
# Windows:
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"

# Linux:
lsb_release -a

# macOS:
sw_vers
```

---

## ✅ Checklist de Execução

Antes de reportar problemas, verifique:

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Tkinter disponível (`python -c "import tkinter"`)
- [ ] Estrutura de pastas correta (`python scripts/teste_estrutura.py`)
- [ ] Executando da pasta raiz do projeto
- [ ] Terminal mostra erros ao executar

---

**Pronto para começar! 🎉**

Execute `App_Treinos_GUI.bat` (Windows) ou `python3 App_Treinos_GUI.py` (Linux/macOS) e comece a criar planos de treino personalizados!
