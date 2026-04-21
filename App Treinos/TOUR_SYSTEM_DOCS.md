# Tour System Documentation

## Sistema de Tour Interativo First-Use

### Componente Principal: `tour_overlay.py`

**Classe TourStep:**
```python
TourStep(
    title="Título do passo",
    description="Descrição detalhada do que o usuário vê",
    target_control=None,           # Elemento a destacar (opcional)
    position="bottom",             # Posição do tooltip: top/bottom/left/right
    max_width=300                  # Largura máxima do tooltip
)
```

**Classe TourOverlay:**
```python
overlay = TourOverlay(
    page=page,                     # Página Flet
    tour_id="dashboard_tour",      # ID único para rastreamento
    steps=[list_of_steps],         # Lista de TourStep
    on_complete=callback,          # Chamado ao concluir
    dark=False                     # Modo escuro
)

overlay.start()          # Inicia tour (pula se já visto)
overlay.next_step()      # Vai para próximo passo
overlay.skip()           # Pula tour completamente
```

### Factory Functions

**create_dashboard_tour()** - Tour de 4 passos
- Bem-vindo ao Dashboard
- Pesquise Atletas
- Crie Novos Planos
- Menu de Ajuda

**create_athletes_tour()** - Tour de 4 passos
- Seus Atletas
- Adicione Atleta
- Menu de Ações
- Dados Rastreados

**create_help_tour()** - Tour de 4 passos
- Centro de Ajuda
- Como Usar
- Configurações
- Suporte

### Integração em Screens

**Dashboard (`dashboard.py`)**
```python
# Ao final de _load_data
tour = create_dashboard_tour(page)
tour.start()
```

**Athletes Management (`athletes_management.py`)**
```python
# Ao final de load_athletes()
tour = create_athletes_tour(page)
tour.start()
```

**Help (`help.py`)**
```python
# Antes do return statement
tour = create_help_tour(page)
tour.start()
```

### Persistência

**Armazenamento em `preferences.json`:**
```json
{
  "_seen_tours": {
    "dashboard_tour": true,
    "athletes_tour": true,
    "help_tour": true
  }
}
```

**Métodos na classe TourOverlay:**
- `_should_skip_tour()` - Verifica se já foi visto
- `_mark_tour_as_seen()` - Salva em preferences.json

### Features Implementadas

✅ **Overlay com Backdrop**
- Fundo escuro (rgba 70% opacidade)
- Clicável para pular para próximo passo

✅ **Highlight de Elementos**
- Border com cor de destaque
- Shadow com efeito brilho
- Scale animation (1.05x)

✅ **Tooltips Interativos**
- Título com tamanho maior
- Descrição com até 5 linhas
- Progress indicator (ex: "1/4")
- Botões: Pular, Próximo/Concluir

✅ **Controle de Fluxo**
- Botão "Pular" em qualquer passo
- Botão "Próximo" para avançar
- "Concluir" no último passo

✅ **Animações**
- Fade-in do tooltip (300ms)
- Scale do elemento destacado (300ms)
- Transições suaves entre passos

✅ **Persistência**
- Tours vistos salvos em preferences.json
- Função `restart_tour()` para re-exibir
- Sem tours duplicados

### UX Flow

1. **Primeira Visita**: Tour começa automaticamente
   - User vê passo 1 com backdrop e tooltip
   - Pode clicar "Próximo", "Pular" ou no backdrop para avançar

2. **Próximos Passos**: Tour guia progressivamente
   - Destaque dinâmico move para próximo elemento
   - Tooltip atualiza com novo conteúdo

3. **Conclusão**: Tour marca como visto
   - Callback `on_complete()` executado se fornecido
   - Prévia grava em preferences.json
   - Futuras visitas não mostram tour

4. **Re-iniciar**: Botão "Refazer Tour Interativo" em Help
   - Remove tour de `_seen_tours`
   - Próxima visita à tela mostra tour novamente

### Limitações Conhecidas (Flet)

- Highlight pode não ser pixel-perfect (sem APIs de coordenadas exatas em Flet)
- Tooltip posicionado dinamicamente em overlay, não próximo ao elemento
- Em telas menores, tooltip pode cobrir elementos
- Sem suporte a "spotlight" nativo do Flet

### Melhorias Futuras

1. Detectar tamanho/posição de elementos para tooltip mais preciso
2. Animar backdrop fade-in/fade-out
3. Adicionar GIF/screenshots em tooltips
4. Skip button com confirmação
5. Progress bar visual entre passos
6. Tours customizáveis por theme/idioma

---

**Status**: ✅ Implementado e Testado
**Testado em**: Screens Dashboard, Athletes Management, Help
**Persistence**: Verificado em preferences.json
