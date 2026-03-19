# 🔧 Correções Aplicadas na GUI - Identificação Profissional

## Data: 18/03/2026

---

## 🐛 Problemas Encontrados

### Erro 1: KeyError - 'normal'
**Linha:** 85 (gui/main_gui.py)  
**Erro:**
```python
KeyError: 'normal'
font=(theme.fonts['primary'], theme.font_sizes['normal'], 'bold')
```

**Causa:**  
O objeto `theme.font_sizes` não possui uma chave `'normal'`. As chaves disponíveis são:
- `'title'`: 24
- `'heading'`: 18
- `'subheading'`: 14
- `'body'`: 12
- `'small'`: 10
- `'button'`: 12

**Solução:**  
Substituído `theme.font_sizes['normal']` por `theme.font_sizes['body']`

```python
# ANTES (ERRO)
font=(theme.fonts['primary'], theme.font_sizes['normal'], 'bold')

# DEPOIS (CORRETO)
font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold')
```

---

### Erro 2: TclError - Mistura de Geometry Managers
**Erro:**
```python
_tkinter.TclError: cannot use geometry manager grid inside 
.!frame2.!dadosprofissionalstep.!frame2 which already has slaves 
managed by pack
```

**Causa:**  
No método `_create_body()` da classe `DadosProfissionalStep`, estava usando:
- `pack()` para `warning_frame` e `info_frame` dentro de `body`
- `grid()` para os campos do formulário também dentro de `body`

Tkinter não permite misturar `pack` e `grid` no mesmo container pai.

**Solução:**  
Criado um frame separado (`form_frame`) para os campos que usam `grid()`:

```python
# ANTES (ERRO)
def _create_body(self):
    body = ttk.Frame(self)
    body.pack(...)
    
    warning_frame = ttk.Frame(body, ...)
    warning_frame.pack(...)  # Pack no body
    
    # Campos usando grid no body (ERRO!)
    self._create_field(body, row, ...)  # Grid no body

# DEPOIS (CORRETO)
def _create_body(self):
    body = ttk.Frame(self)
    body.pack(...)
    
    warning_frame = ttk.Frame(body, ...)
    warning_frame.pack(...)  # Pack no body
    
    # Frame separado para grid
    form_frame = ttk.Frame(body)
    form_frame.pack(...)  # Pack no body
    
    # Campos usando grid no form_frame (CORRETO!)
    self._create_field(form_frame, row, ...)  # Grid no form_frame
```

**Estrutura Final:**
```
body (frame principal)
├── warning_frame (pack)
│   └── Labels (pack)
├── form_frame (pack no body)
│   └── Campos (grid no form_frame)
└── info_frame (pack)
    └── Labels (pack)
```

---

## ✅ Código Corrigido

### Método `_create_body()` Completo

```python
def _create_body(self):
    """Cria campos de identificação profissional."""
    body = ttk.Frame(self)
    body.pack(fill='both', expand=True, padx=theme.spacing['xl'], pady=theme.spacing['md'])
    
    # Aviso importante
    warning_frame = ttk.Frame(body, style='Card.TFrame')
    warning_frame.pack(fill='x', pady=(0, theme.spacing['lg']))
    
    ttk.Label(
        warning_frame,
        text="⚠️ ATENÇÃO",
        foreground=theme.colors['accent_primary'],
        font=(theme.fonts['primary'], theme.font_sizes['body'], 'bold')  # ✅ CORRIGIDO
    ).pack(anchor='w', padx=theme.spacing['md'], pady=(theme.spacing['md'], theme.spacing['xs']))
    
    ttk.Label(
        warning_frame,
        text="Todo plano de treinamento deve ser elaborado por um profissional\n"
             "de Educação Física credenciado (CREF). Preencha os dados abaixo:",
        foreground=theme.colors['text_secondary']
    ).pack(anchor='w', padx=theme.spacing['md'], pady=(0, theme.spacing['md']))
    
    # Frame para formulário grid (separado para não misturar com pack) ✅ CORRIGIDO
    form_frame = ttk.Frame(body)
    form_frame.pack(fill='x', pady=theme.spacing['md'])
    
    row = 0
    
    # Nome Completo
    self._create_field(form_frame, row, "Nome Completo do Profissional:", "nome_completo", "text",
                      "Ex: Dr. João Silva Santos")
    row += 1
    
    # CPF
    self._create_field(form_frame, row, "CPF (somente números):", "cpf", "text",
                      "Ex: 12345678909 (11 dígitos)")
    row += 1
    
    # CREF
    self._create_field(form_frame, row, "CREF:", "cref", "text",
                      "Ex: 123456-G/SP ou CREF1 123456-G/RJ")
    row += 1
    
    # Informação adicional
    info_frame = ttk.Frame(body, style='Card.TFrame')
    info_frame.pack(fill='x', pady=(theme.spacing['lg'], 0))
    
    ttk.Label(
        info_frame,
        text="ℹ️ Informações sobre os campos:",
        font=(theme.fonts['primary'], theme.font_sizes['small'], 'bold')
    ).pack(anchor='w', padx=theme.spacing['md'], pady=(theme.spacing['sm'], theme.spacing['xs']))
    
    ttk.Label(
        info_frame,
        text="• CPF: Cadastro de Pessoa Física (validado automaticamente)\n"
             "• CREF: Conselho Regional de Educação Física\n"
             "  Formato: NNNNNN-G/UF (ex: 123456-G/SP)",
        foreground=theme.colors['text_secondary'],
        font=(theme.fonts['primary'], theme.font_sizes['small'])
    ).pack(anchor='w', padx=theme.spacing['md'], pady=(0, theme.spacing['sm']))
```

---

## 🧪 Testes Realizados

### ✅ Teste 1: Execução da GUI
**Comando:** `python gui/main_gui.py`  
**Resultado:** GUI abre sem erros ✅

### ✅ Teste 2: Navegação entre Etapas
**Resultado:** Wizard funciona corretamente ✅

### ✅ Teste 3: Validação de Dados
**Dados Válidos:**
- Nome: Dr. João Silva Santos
- CPF: 12345678909
- CREF: 123456-G/SP

**Resultado:** Validação bem-sucedida, mensagem exibida ✅

**Dados Inválidos:**
- CPF: 12345678900 → Erro exibido corretamente ✅
- CREF: ABC-123 → Erro exibido corretamente ✅
- Nome: João → Erro exibido corretamente ✅

---

## 📋 Lições Aprendidas

### 1. Sempre verificar documentação do tema
Antes de usar propriedades de objetos como `theme.font_sizes`, verificar quais chaves estão disponíveis.

### 2. Não misturar geometry managers
No Tkinter, **NUNCA** misturar `pack()` e `grid()` no mesmo container pai. Use frames separados se necessário.

### 3. Estrutura hierárquica clara
Manter uma estrutura clara de frames ajuda a evitar conflitos:
```
Container Principal (pack)
├── Sub-container 1 (pack no principal)
│   └── Widgets (pack no sub-container 1)
├── Sub-container 2 (pack no principal)
│   └── Widgets (grid no sub-container 2)
└── Sub-container 3 (pack no principal)
    └── Widgets (pack no sub-container 3)
```

---

## ✅ Status Final

**Data:** 18/03/2026  
**Status:** ✅ **CORRIGIDO E FUNCIONANDO**

- ✅ Erro de KeyError resolvido
- ✅ Erro de TclError (geometry manager) resolvido
- ✅ GUI executando sem erros
- ✅ Validação funcionando corretamente
- ✅ Testes manuais passando

---

**Arquivos Modificados:**
- `gui/main_gui.py` - Classe `DadosProfissionalStep`
  - Linha 85: Corrigido font_sizes
  - Linhas 96-100: Adicionado form_frame separado

**Scripts de Teste:**
- `scripts/teste_gui_final.py` - Validação final
- `scripts/teste_gui_profissional.py` - Testes de validação
- `scripts/teste_validacao_profissional.py` - Testes unitários (9/9 passando)
