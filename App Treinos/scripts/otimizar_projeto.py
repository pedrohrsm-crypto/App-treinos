"""
Script de Otimização e Limpeza - App Treinos
============================================

Remove duplicatas, consolida documentação e otimiza código.
"""

import os
import shutil
from pathlib import Path

# Diretório raiz
ROOT_DIR = Path(__file__).parent.parent

def remover_duplicatas_gui():
    """Remove arquivos duplicados da GUI."""
    gui_dir = ROOT_DIR / 'gui'
    arquivos_remover = [
        'main_gui_v2.py',
        'main_gui_old_backup.py'
    ]
    
    removidos = []
    for arquivo in arquivos_remover:
        caminho = gui_dir / arquivo
        if caminho.exists():
            caminho.unlink()
            removidos.append(str(caminho))
    
    return removidos

def limpar_pycache():
    """Remove todos os diretórios __pycache__."""
    removidos = []
    for pycache in ROOT_DIR.rglob('__pycache__'):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            removidos.append(str(pycache))
    return removidos

def consolidar_readme():
    """Consolida arquivos README duplicados."""
    # Manter apenas README.md principal
    readmes_duplicados = [
        'LEIA-ME.md',
        'CAMINHOS_OK.md',
        'INDICE.md'
    ]
    
    removidos = []
    for readme in readmes_duplicados:
        caminho = ROOT_DIR / readme
        if caminho.exists():
            # Fazer backup antes de remover
            backup = ROOT_DIR / 'docs' / 'archived' / readme
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(caminho), str(backup))
            removidos.append(f"{readme} → docs/archived/{readme}")
    
    return removidos

def consolidar_scripts_teste():
    """Move scripts de teste antigos para pasta archived."""
    scripts_dir = ROOT_DIR / 'scripts'
    archived_dir = scripts_dir / 'archived'
    archived_dir.mkdir(exist_ok=True)
    
    # Scripts antigos/redundantes
    scripts_antigos = [
        'exemplos.py',
        'teste_ia_saude.py',
        'resumo_implementacao.py',
        'comparacao_modos_configuracao.py'
    ]
    
    movidos = []
    for script in scripts_antigos:
        origem = scripts_dir / script
        if origem.exists():
            destino = archived_dir / script
            shutil.move(str(origem), str(destino))
            movidos.append(f"{script} → scripts/archived/")
    
    return movidos

def otimizar_documentacao():
    """Consolida documentação redundante."""
    docs_dir = ROOT_DIR / 'docs'
    archived_dir = docs_dir / 'archived'
    archived_dir.mkdir(exist_ok=True)
    
    # Documentos a arquivar (informações já consolidadas em outros)
    docs_arquivar = [
        'CORRECOES_GUI.md',  # Info já em GUI_V2_DESIGN.md
        'GUI_MANUAL.md',  # Substituído por GUI_V2_DESIGN.md
        'ATUALIZACAO_CAMINHOS.md',  # Implementado
        'EXECUCAO_DUPLO_CLIQUE.md',  # Info em COMO_EXECUTAR.md
    ]
    
    arquivados = []
    for doc in docs_arquivar:
        origem = docs_dir / doc
        if origem.exists():
            destino = archived_dir / doc
            shutil.move(str(origem), str(destino))
            arquivados.append(f"{doc} → docs/archived/")
    
    return arquivados

def criar_indice_unificado():
    """Cria índice único e consolidado."""
    indice_content = """# 📚 Índice do Projeto - App Treinos

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
"""
    
    # Salvar índice unificado
    indice_path = ROOT_DIR / 'INDICE_PROJETO.md'
    indice_path.write_text(indice_content, encoding='utf-8')
    
    return str(indice_path)

def main():
    """Executa otimização completa."""
    print("="*70)
    print("🔧 OTIMIZAÇÃO E LIMPEZA DO PROJETO")
    print("="*70)
    
    # 1. Remover duplicatas GUI
    print("\n1️⃣ Removendo arquivos GUI duplicados...")
    removidos_gui = remover_duplicatas_gui()
    for arquivo in removidos_gui:
        print(f"   ✅ Removido: {arquivo}")
    if not removidos_gui:
        print("   ℹ️  Nenhum arquivo duplicado encontrado")
    
    # 2. Limpar __pycache__
    print("\n2️⃣ Limpando cache Python (__pycache__)...")
    removidos_cache = limpar_pycache()
    print(f"   ✅ Removidos {len(removidos_cache)} diretórios __pycache__")
    
    # 3. Consolidar README
    print("\n3️⃣ Consolidando arquivos README duplicados...")
    removidos_readme = consolidar_readme()
    for item in removidos_readme:
        print(f"   ✅ Arquivado: {item}")
    if not removidos_readme:
        print("   ℹ️  Nenhum README duplicado encontrado")
    
    # 4. Consolidar scripts de teste
    print("\n4️⃣ Arquivando scripts de teste antigos...")
    movidos_scripts = consolidar_scripts_teste()
    for item in movidos_scripts:
        print(f"   ✅ Movido: {item}")
    if not movidos_scripts:
        print("   ℹ️  Nenhum script antigo encontrado")
    
    # 5. Otimizar documentação
    print("\n5️⃣ Consolidando documentação redundante...")
    arquivados_docs = otimizar_documentacao()
    for item in arquivados_docs:
        print(f"   ✅ Arquivado: {item}")
    if not arquivados_docs:
        print("   ℹ️  Nenhuma documentação redundante encontrada")
    
    # 6. Criar índice unificado
    print("\n6️⃣ Criando índice unificado...")
    indice = criar_indice_unificado()
    print(f"   ✅ Criado: {indice}")
    
    # Resumo final
    print("\n" + "="*70)
    print("✅ OTIMIZAÇÃO CONCLUÍDA!")
    print("="*70)
    print(f"\n📊 Resumo:")
    print(f"   • Arquivos GUI removidos: {len(removidos_gui)}")
    print(f"   • Diretórios cache limpos: {len(removidos_cache)}")
    print(f"   • READMEs arquivados: {len(removidos_readme)}")
    print(f"   • Scripts arquivados: {len(movidos_scripts)}")
    print(f"   • Docs arquivados: {len(arquivados_docs)}")
    print(f"\n📁 Estrutura otimizada e consolidada!")
    print(f"📖 Consulte: INDICE_PROJETO.md\n")

if __name__ == "__main__":
    main()
