"""
Hover Effects Utilities — Sistema consistente de efeitos visuais
==================================================================

Fornece funções helper para adicionar efeitos de hover a:
- Containers (cards)
- Botões
- IconButtons
- Menus

Padrão: Scale + Shadow + Color tint
"""

import flet as ft
from flet_app.theme import c, card_shadow
from typing import Callable, Optional


def apply_hover_effects_to_button(
    button: ft.Control,
    scale_ratio: float = 1.05,
    color_tint: Optional[str] = None,
    duration_ms: int = 150,
    dark: bool = False,
) -> ft.Control:
    """
    Adiciona efeitos de hover a um botão.

    Args:
        button: Botão (ElevatedButton, TextButton, etc.)
        scale_ratio: Escala ao hover (1.05 = 5% maior)
        color_tint: Cor de tint ao hover (opcional)
        duration_ms: Duração da animação
        dark: Modo escuro ativo

    Returns:
        Botão com hover effects aplicado
    """
    original_bgcolor = button.bgcolor
    original_color = button.color if hasattr(button, 'color') else None

    def _on_hover(e):
        if e.data == "true":
            button.scale = scale_ratio
            if hasattr(button, 'opacity'):
                button.opacity = 0.9
        else:
            button.scale = 1.0
            if hasattr(button, 'opacity'):
                button.opacity = 1.0
        button.update()

    button.on_hover = _on_hover
    button.animate = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)
    button.animate_scale = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)
    button.animate_opacity = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)

    return button


def apply_hover_effects_to_icon_button(
    icon_button: ft.IconButton,
    scale_ratio: float = 1.2,
    icon_size_increase: bool = False,
    duration_ms: int = 150,
    dark: bool = False,
) -> ft.IconButton:
    """
    Adiciona efeitos de hover a um IconButton.

    Args:
        icon_button: IconButton a afetar
        scale_ratio: Escala do container ao hover
        icon_size_increase: Aumentar tamanho do ícone também
        duration_ms: Duração da animação
        dark: Modo escuro ativo

    Returns:
        IconButton com hover effects
    """
    original_icon_size = icon_button.icon_size or 24

    def _on_hover(e):
        if e.data == "true":
            icon_button.scale = scale_ratio
            if icon_size_increase:
                icon_button.icon_size = max(original_icon_size * 1.1, original_icon_size + 2)
            icon_button.opacity = 0.85
        else:
            icon_button.scale = 1.0
            if icon_size_increase:
                icon_button.icon_size = original_icon_size
            icon_button.opacity = 1.0
        icon_button.update()

    icon_button.on_hover = _on_hover
    icon_button.animate = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)
    icon_button.animate_scale = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)
    icon_button.animate_icon_size = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)
    icon_button.animate_opacity = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)

    return icon_button


def apply_hover_effects_to_card(
    container: ft.Container,
    scale_ratio: float = 1.02,
    shadow_level: str = "lg",
    duration_ms: int = 200,
    dark: bool = False,
) -> ft.Container:
    """
    Adiciona efeitos de hover a um card/container.

    Args:
        container: Container/Card a afetar
        scale_ratio: Escala ao hover
        shadow_level: Nível de sombra ao hover ("sm", "md", "lg", "xl")
        duration_ms: Duração da animação
        dark: Modo escuro ativo

    Returns:
        Container com hover effects
    """
    original_shadow = container.shadow
    hover_shadow = card_shadow(dark, shadow_level)

    def _on_hover(e):
        if e.data == "true":
            container.scale = scale_ratio
            container.shadow = hover_shadow
        else:
            container.scale = 1.0
            container.shadow = original_shadow
        container.update()

    container.on_hover = _on_hover
    container.animate = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)
    container.animate_scale = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)

    # Adicionar ink effect se não existir
    if not hasattr(container, 'ink') or container.ink is None:
        container.ink = True

    return container


def apply_hover_effects_to_row(
    row: ft.Row,
    hover_color: Optional[str] = None,
    padding_increase: int = 4,
    duration_ms: int = 150,
    dark: bool = False,
) -> ft.Row:
    """
    Adiciona efeitos de hover a um Row (para menus/listas).

    Args:
        row: Row a afetar
        hover_color: Cor de fundo ao hover
        padding_increase: Aumento de padding ao hover
        duration_ms: Duração da animação
        dark: Modo escuro ativo

    Returns:
        Row com hover effects
    """
    original_bgcolor = row.bgcolor
    original_padding = row.padding or ft.padding.all(0)

    def _on_hover(e):
        if e.data == "true":
            if hover_color:
                row.bgcolor = hover_color
            row.scale = 1.01
        else:
            if hover_color:
                row.bgcolor = original_bgcolor
            row.scale = 1.0
        row.update()

    row.on_hover = _on_hover
    row.animate = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)
    row.animate_scale = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)
    row.animate_bgcolor = ft.Animation(duration_ms, ft.AnimationCurve.EASE_OUT)

    return row


def create_hoverable_menu_item(
    label: str,
    icon: Optional[str] = None,
    on_click: Optional[Callable] = None,
    dark: bool = False,
) -> ft.Container:
    """
    Cria um item de menu com hover effects integrados.

    Args:
        label: Texto do item
        icon: Ícone (opcional)
        on_click: Callback ao clicar
        dark: Modo escuro ativo

    Returns:
        Container do menu item com hover effects
    """
    content_controls = []

    if icon:
        content_controls.append(
            ft.Icon(icon, size=18, color=c("primary", dark))
        )

    content_controls.append(
        ft.Text(
            label,
            size=14,
            color=c("text_primary", dark),
            expand=True,
        )
    )

    row = ft.Row(
        content_controls,
        spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    container = ft.Container(
        content=row,
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        border_radius=8,
        bgcolor=c("bg_primary", dark),
        on_click=on_click,
    )

    # Aplicar hover effects
    apply_hover_effects_to_card(
        container,
        scale_ratio=1.02,
        shadow_level="md",
        dark=dark,
    )

    return container
