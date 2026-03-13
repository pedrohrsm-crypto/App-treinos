# 🐧 App Treinos - Versão para Linux

## 📋 Instalação Rápida

### 1. Tornar os scripts executáveis
```bash
cd "App Treinos"
chmod +x linux/*.sh
```

### 2. Executar instalação
```bash
./linux/instalar.sh
```

### 3. Executar o sistema
```bash
./linux/executar.sh
```

---

## 🚀 Comandos Disponíveis

### Executar o Sistema Principal
```bash
./linux/executar.sh
```

### Menu de Exemplos
```bash
./linux/exemplos.sh
```

### Instalação Manual
```bash
pip3 install --user pandas openpyxl
python3 training_planner.py
```

---

## 🔧 Distribuições Testadas

✅ **Ubuntu / Debian**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

✅ **Fedora / RedHat / CentOS**
```bash
sudo yum install python3 python3-pip
```

✅ **Arch Linux / Manjaro**
```bash
sudo pacman -S python python-pip
```

---

## 📦 Dependências

- **Python 3.8+**
- **pandas >= 2.0.0**
- **openpyxl >= 3.1.0**

---

## 🐛 Solução de Problemas

### Problema: "permission denied"
```bash
chmod +x linux/*.sh
```

### Problema: "python3 não encontrado"
```bash
# Ubuntu/Debian
sudo apt-get install python3

# Fedora/RedHat
sudo yum install python3

# Arch Linux
sudo pacman -S python
```

### Problema: Erro de encoding UTF-8
O sistema já está configurado para UTF-8. Se encontrar problemas, defina:
```bash
export LC_ALL=pt_BR.UTF-8
export LANG=pt_BR.UTF-8
```

---

## 📁 Estrutura de Arquivos

```
linux/
├── instalar.sh      # Script de instalação
├── executar.sh      # Executa o sistema principal
├── exemplos.sh      # Menu de exemplos
└── README.md        # Este arquivo
```

---

## 💡 Dicas de Uso

### Criar Alias (Opcional)
Adicione ao seu `~/.bashrc` ou `~/.zshrc`:
```bash
alias treinos='cd /caminho/para/App\ Treinos && ./linux/executar.sh'
alias treinos-exemplos='cd /caminho/para/App\ Treinos && ./linux/exemplos.sh'
```

Depois execute:
```bash
source ~/.bashrc  # ou ~/.zshrc
```

Agora você pode executar de qualquer lugar:
```bash
treinos
treinos-exemplos
```

---

## 🎯 Recursos do Sistema

- ✅ Cálculo automático de semanas por data
- ✅ Periodização profissional (1-52 semanas)
- ✅ Adaptação para ciclo menstrual
- ✅ IA de saúde para lesões
- ✅ Exportação Excel completa
- ✅ Mensagens educativas de limite

---

## 📞 Suporte

Para problemas específicos do Linux, verifique:
1. Versão do Python: `python3 --version`
2. Versão do pip: `pip3 --version`
3. Locale: `locale`

---

**Versão:** 2.3 Linux  
**Última atualização:** 13/03/2026
