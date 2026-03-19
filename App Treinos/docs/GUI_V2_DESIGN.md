# 🎨 Nova Interface Gráfica - App Treinos v2.0

## Visão Geral

Interface moderna e acolhedora com foco em UX otimizada para profissionais de Educação Física.

---

## 🎯 Estrutura em 3 Etapas

### 1️⃣ Splash Screen (Tela Inicial)

**Elementos:**
- 🏃 Logo centralizada (placeholder de emoji, será substituído por imagem)
- **App Treinos** - Nome do aplicativo
- Subtítulo: "Sistema Profissional de Planejamento Esportivo"
- Fundo: `#68b2c2` (azul turquesa)

**Animação:**
- **Fade In**: Elementos aparecem suavemente (0 → 100% opacidade)
- **Permanência**: 2 segundos visível
- **Fade Out**: Elementos desaparecem suavemente (100% → 0% opacidade)
- **Duração total**: ~4 segundos

**Implementação:**
```python
class SplashScreen:
    - Interpolação de cores para simular fade
    - Alpha de 0.0 a 1.0
    - Callback on_complete ao finalizar
```

---

### 2️⃣ Login Screen (Tela de Login)

**Layout:**
```
┌─────────────────────────────────────────┐
│                                         │
│              🏃                         │
│                                         │
│         Bem-vindo!                      │
│    Faça login para continuar           │
│                                         │
│  CPF ou CREF (somente números):        │
│  ┌───────────────────────────┐         │
│  │                           │         │
│  └───────────────────────────┘         │
│                                         │
│  ┌───────────────────────────┐         │
│  │        Entrar             │         │
│  └───────────────────────────┘         │
│                                         │
│          ─── ou ───                    │
│                                         │
│  Não tem cadastro? Clique aqui         │
│      para se cadastrar                 │
│                                         │
└─────────────────────────────────────────┘
```

**Funcionalidades:**
- ✅ Campo de entrada para CPF ou CREF
- ✅ Validação básica (mínimo 4 dígitos)
- ✅ Enter key para fazer login
- ✅ Link para cadastro (placeholder)
- ✅ Card centralizado com sombra
- ✅ Fundo secundário (`#f0f8fa`)

**Cores:**
- Card: Branco (`#FFFFFF`)
- Texto: Primário (`#1a1a1a`)
- Botão: Turquesa (`#68b2c2`)
- Hover: Tom mais escuro (`#5a9eb0`)

---

### 3️⃣ Dashboard Screen (Painel Principal)

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ 🏃  App Treinos                        👤 Profissional │
│     Sistema Profissional...              ID: 123456...  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│         O que você deseja fazer?                        │
│                                                         │
│   ┌──────────────┐      ┌──────────────┐              │
│   │      ➕      │      │      ✏️      │              │
│   │              │      │              │              │
│   │ Criar Treino │      │ Editar Treino│              │
│   │              │      │              │              │
│   │ Crie um novo │      │ Edite ou     │              │
│   │ plano de     │      │ visualize    │              │
│   │ treinamento  │      │ planos       │              │
│   │              │      │              │              │
│   └──────────────┘      └──────────────┘              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Componentes:**

**Header:**
- Logo + Nome do aplicativo (esquerda)
- Info do profissional (direita)
- Fundo branco com separação visual

**Hero Cards:**
- **Card 1: Criar Treino**
  - Ícone: ➕ (verde)
  - Cor: `#68b2c2` (primária)
  - Dimensão: 350x250px
  
- **Card 2: Editar Treino**
  - Ícone: ✏️ (azul)
  - Cor: `#6885c2` (análoga)
  - Dimensão: 350x250px

**Efeitos:**
- ✅ Hover: Card muda fundo para `#e6f4f7`
- ✅ Cursor: Hand pointer
- ✅ Sombra suave nos cards
- ✅ Click: Transição para wizard

---

## 🎨 Paleta de Cores

### Cores Principais
| Nome | Hex | Uso |
|------|-----|-----|
| **Primária** | `#68b2c2` | Fundos, botões, destaques |
| **Complementar** | `#c27968` | Avisos, alertas |
| **Análoga 1** | `#68c2a6` | Sucesso, confirmações |
| **Análoga 2** | `#6885c2` | Info, cards secundários |
| **Triadic 1** | `#7968c2` | Destaque alternativo |
| **Triadic 2** | `#c268b2` | Destaque especial |

### Cores de Fundo
| Nome | Hex | Uso |
|------|-----|-----|
| **BG Primário** | `#68b2c2` | Splash screen |
| **BG Secundário** | `#f0f8fa` | Telas gerais |
| **BG Terciário** | `#e6f4f7` | Hover effects |
| **BG Branco** | `#FFFFFF` | Cards, modais |

### Cores de Texto
| Nome | Hex | Contraste |
|------|-----|-----------|
| **Texto Primário** | `#1a1a1a` | Alto contraste |
| **Texto Secundário** | `#4a4a4a` | Médio contraste |
| **Texto Desabilitado** | `#9a9a9a` | Baixo contraste |
| **Texto Claro** | `#FFFFFF` | Sobre fundos escuros |

---

## 📝 Tipografia

### Fontes
- **Windows**: Segoe UI
- **macOS**: SF Pro Text
- **Linux**: Ubuntu
- **Fallback**: Arial / Helvetica Neue

### Tamanhos
| Contexto | Tamanho | Peso |
|----------|---------|------|
| Splash Logo | 48px | Bold |
| Título Principal | 32px | Bold |
| Cabeçalho | 24px | Bold |
| Título Card | 20px | Bold |
| Subcabeçalho | 18px | Normal |
| Corpo | 14px | Normal |
| Pequeno | 12px | Normal |
| Botão | 14px | Bold |

**Características:**
- ✅ Sans-serif (sem serifas)
- ✅ Acolhedora e legível
- ✅ Profissional
- ✅ Alta legibilidade em todos os tamanhos

---

## 🎭 Animações e Transições

### Splash Screen
```python
# Fade In: 50ms x 20 frames = 1 segundo
# Hold: 2 segundos
# Fade Out: 50ms x 20 frames = 1 segundo
# Total: 4 segundos
```

### Hover Effects
- **Cards**: Mudança de fundo instantânea
- **Botões**: Mudança de cor ao clicar

### Screen Transitions
- Destroy anterior + create novo
- Smooth visual flow

---

## 🔧 Componentes Reutilizáveis

### Hero Card
```python
_create_hero_card(
    parent,
    title="Título",
    icon="🎯",
    description="Descrição\nMultilinha",
    color="#68b2c2",
    command=callback_function
)
```

**Features:**
- Ícone grande centralizado
- Título em negrito
- Descrição multilinha
- Hover effect
- Click callback
- Sombra customizada

---

## 📊 Dimensões e Espaçamento

### Tamanhos de Componentes
| Componente | Largura | Altura |
|------------|---------|--------|
| Janela Mínima | 1000px | 700px |
| Hero Card | 350px | 250px |
| Botão | auto | 50px |
| Input | auto | 45px |
| Card Login | 450px | 550px |

### Espaçamento
| Tipo | Valor |
|------|-------|
| XS | 4px |
| SM | 8px |
| MD | 16px |
| LG | 24px |
| XL | 32px |

---

## 🚀 Próximos Passos

### Implementações Futuras

1. **Substituir Placeholders**
   - Logo do emoji 🏃 → Imagem PNG/SVG
   - Nome "App Treinos" → Logo com tipografia customizada

2. **Banco de Dados Local**
   - SQLite para armazenar cadastros
   - Autenticação real
   - Histórico de treinos

3. **Wizard Completo**
   - Integrar DadosProfissionalStep (já criado)
   - DadosBasicosStep
   - ModalidadeStep
   - ObjetivosStep
   - ReviewStep

4. **Funcionalidade de Edição**
   - Lista de treinos criados
   - Filtros e busca
   - Exportação em lote

5. **Melhorias Visuais**
   - Animações mais suaves
   - Ícones SVG customizados
   - Temas (claro/escuro)

---

## 📝 Notas Técnicas

### Arquivos Modificados
- ✅ `gui/theme.py` - Paleta de cores atualizada
- ✅ `gui/main_gui_v2.py` - Nova estrutura completa

### Arquivos Criados
- ✅ `docs/GUI_V2_DESIGN.md` - Esta documentação

### Compatibilidade
- ✅ Windows ✓
- ✅ macOS ✓
- ✅ Linux ✓

### Dependências
- Python 3.x
- tkinter (nativo)
- Nenhuma dependência externa adicional

---

## 🧪 Como Testar

```bash
# Executar nova interface
python gui/main_gui_v2.py
```

**Fluxo de Teste:**
1. Observe o splash screen (fade in/out)
2. Digite qualquer CPF ou CREF com 4+ dígitos
3. Clique em "Entrar" ou pressione Enter
4. Explore o dashboard
5. Clique nos hero cards (placeholder messages)

---

**Criado em:** 18/03/2026  
**Versão:** 2.0  
**Status:** ✅ Implementado e Funcional
