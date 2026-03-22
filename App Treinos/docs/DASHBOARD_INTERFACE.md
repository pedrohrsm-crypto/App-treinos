# Interface de Dashboard - App Treinos

## 📋 Visão Geral

Interface de dashboard criada para ser exibida após o login do usuário no sistema. Esta interface serve como hub central de navegação, oferecendo acesso rápido às principais funcionalidades do aplicativo.

## ✨ Recursos Implementados

### 1. **Header Profissional**
- **Logo e Branding**: Ícone do app + título "App Treinos" com subtítulo
- **Informações do Usuário**: 
  - Ícone de perfil
  - Nome completo do profissional
  - Número CREF
- **Botão de Logout**: 
  - Design em vermelho com ícone de porta
  - Efeito hover interativo
  - Confirmação antes de sair

### 2. **Hero Cards Interativos**

#### Card 1: "Novo Plano" 📋
- **Função**: Criar um novo plano de treinamento personalizado
- **Ícone**: 📋 (prancheta)
- **Cor**: Azul turquesa (cor primária do sistema)
- **Descrição**: "Crie um novo plano de treinamento personalizado para seu atleta"

#### Card 2: "Editar Plano" 📝
- **Função**: Visualizar, editar ou exportar planos existentes
- **Ícone**: 📝 (documento com caneta)
- **Cor**: Verde-azulado (cor análoga)
- **Descrição**: "Visualize, edite ou exporte planos de treinamento já criados"

### 3. **Design Visual Aprimorado**

#### Características dos Hero Cards:
- ✅ **Barra colorida no topo**: Identifica visualmente cada card
- ✅ **Ícone em círculo**: Fundo colorido que destaca o ícone
- ✅ **Bordas arredondadas**: Visual moderno e profissional
- ✅ **Sombras sutis**: Profundidade e hierarquia visual
- ✅ **Efeitos hover animados**:
  - Mudança de cor de fundo
  - Sublinhado no título
  - Mudança de cor do círculo do ícone
  - Borda colorida destacada
  - Indicador "Clique para começar →"

### 4. **Saudação Personalizada**
- Mensagem personalizada com o primeiro nome do usuário
- Exemplo: "Olá, Pedro! O que você deseja fazer hoje?"
- Subtítulo orientativo: "Escolha uma opção abaixo para começar"

## 🎨 Paleta de Cores Utilizada

| Elemento | Cor | Código |
|----------|-----|--------|
| Cor Primária (Card "Novo Plano") | Azul Turquesa | `#68b2c2` |
| Cor Análoga (Card "Editar Plano") | Verde-azulado | `#68c2a6` |
| Fundo Principal | Cinza Claro | `#f0f8fa` |
| Cards | Branco | `#FFFFFF` |
| Texto Principal | Quase Preto | `#1a1a1a` |
| Texto Secundário | Cinza | `#4a4a4a` |
| Botão Logout | Vermelho Suave | `#c26868` |

## 🔄 Fluxo de Navegação

```
Login Screen
     ↓
Dashboard (Hero Cards)
     ↓
┌────┴────┐
│         │
Novo      Editar
Plano     Plano
│         │
↓         ↓
Wizard    Lista de
Criação   Planos
```

## 🚀 Como Testar

### Opção 1: Executar o aplicativo completo
```bash
cd "d:\GitHub\App Treinos\Python\App Treinos"
python App_Treinos_GUI.py
```

### Opção 2: Executar via arquivo BAT
```bash
cd "d:\GitHub\App Treinos\Python\App Treinos"
App_Treinos_GUI.bat
```

### Credenciais de Teste
- **CPF/CREF**: Use um cadastro existente no banco de dados
- **Senha**: Senha cadastrada anteriormente

## 📱 Responsividade

A interface é totalmente responsiva e se adapta a diferentes tamanhos de tela:
- **Tamanho mínimo**: 400x500 pixels
- **Tamanho inicial**: 1000x700 pixels
- **Redimensionável**: Sim, todos os elementos se adaptam

## 🎯 Funcionalidades Futuras

As ações dos cards atualmente mostram mensagens informativas. As próximas implementações incluirão:

1. **Novo Plano**: Wizard completo com etapas:
   - Dados do atleta
   - Modalidade esportiva (incluindo duathlons)
   - Disponibilidade e objetivos
   - Geração e exportação do plano

2. **Editar Plano**: Interface de gestão com:
   - Lista de todos os planos criados
   - Filtros e busca
   - Edição de planos existentes
   - Visualização de histórico
   - Exportação para Excel

## 🔧 Arquivos Modificados

1. **gui/main_gui.py**
   - Classe `DashboardScreen` aprimorada
   - Método `_create_content()` atualizado
   - Método `_create_hero_card()` redesenhado
   - Método `_logout()` adicionado
   - Melhorias no header com botão de logout

## 📝 Notas Técnicas

### Tecnologias Utilizadas
- **Framework**: Tkinter (Python GUI)
- **Estilo**: Theme personalizado com cores acessíveis
- **Padrões**: WCAG 2.1 para acessibilidade

### Estrutura do Código
```python
class DashboardScreen:
    def __init__(parent, credential, on_create_training, on_edit_training)
    def _create_header()      # Header com logo e logout
    def _create_content()     # Hero cards e saudação
    def _create_hero_card()   # Criação individual de cards
    def _on_card_click()      # Navegação para ações
    def _logout()             # Logout com confirmação
```

## ✅ Checklist de Qualidade

- [x] Interface visualmente atraente
- [x] Navegação intuitiva
- [x] Efeitos hover responsivos
- [x] Saudação personalizada
- [x] Botão de logout funcional
- [x] Cores acessíveis (contraste adequado)
- [x] Responsividade implementada
- [x] Código sem erros
- [x] Documentação completa

---

**Atualizado em**: 21/03/2026  
**Última modificação**: Implementação completa do Dashboard com Hero Cards
