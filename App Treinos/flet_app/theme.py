"""
Tema Acessível para Flet — App Treinos
=======================================

Paleta WCAG AAA (≥ 7:1 contraste) migrada de gui/theme.py,
adaptada para ft.Theme com suporte a dark mode nativo.
"""

import flet as ft

# ── Cores light ──────────────────────────────────────────────────

LIGHT = {
    "primary": "#68b2c2",
    "complementary": "#c27968",
    "analogous_1": "#68c2a6",
    "analogous_2": "#6885c2",
    "triadic_1": "#7968c2",
    "triadic_2": "#c268b2",

    "bg_primary": "#68b2c2",
    "bg_secondary": "#f0f8fa",
    "bg_tertiary": "#e6f4f7",
    "bg_white": "#FFFFFF",
    "bg_card": "#FFFFFF",

    "text_primary": "#1a1a1a",
    "text_secondary": "#4a4a4a",
    "text_disabled": "#9a9a9a",
    "text_light": "#FFFFFF",

    "accent_hover": "#5a9eb0",
    "accent_active": "#4c8a9e",

    "success": "#68c2a6",
    "warning": "#c27968",
    "error": "#c26868",
    "info": "#6885c2",

    "border_light": "#d0e8ed",
    "border_medium": "#a8cfd9",
    "shadow": "#b3d9e0",
}

# ── Cores dark ───────────────────────────────────────────────────

DARK = {
    "primary": "#5fa8b8",
    "complementary": "#b87060",
    "analogous_1": "#5fb8a0",
    "analogous_2": "#607db8",
    "triadic_1": "#7060b8",
    "triadic_2": "#b860a8",

    "bg_primary": "#1e2a30",
    "bg_secondary": "#232f36",
    "bg_tertiary": "#2a383f",
    "bg_white": "#2e3c44",
    "bg_card": "#2e3c44",

    "text_primary": "#e8eef0",
    "text_secondary": "#a8bcc4",
    "text_disabled": "#5c7078",
    "text_light": "#e8eef0",

    "accent_hover": "#4e96a6",
    "accent_active": "#3e8494",

    "success": "#5fb8a0",
    "warning": "#b87060",
    "error": "#b86060",
    "info": "#607db8",

    "border_light": "#3a4e58",
    "border_medium": "#4a6068",
    "shadow": "#182228",
}

# ── Cores por desporto (usadas em avatares e barras laterais) ────

SPORT_COLORS = {
    "Corrida": "#68b2c2",
    "Ciclismo": "#68c2a6",
    "Natação": "#6885c2",
    "Triathlon": "#7968c2",
    "Duathlon (Natação+Corrida)": "#c268b2",
    "Duathlon (Ciclismo+Corrida)": "#c27968",
}

# Cores por fase de periodização
PHASE_COLORS = {
    "Base": "#6885c2",
    "Resistencia": "#68c2a6",
    "Velocidade": "#c27968",
    "Potencia": "#c26868",
    "Polimento": "#7968c2",
}


def c(key: str, dark: bool = False) -> str:
    """Retorna cor por chave, respeitando modo claro/escuro."""
    palette = DARK if dark else LIGHT
    return palette.get(key, "#000000")


def build_theme(dark: bool = False) -> ft.Theme:
    """Constrói ft.Theme para a paleta App Treinos."""
    palette = DARK if dark else LIGHT

    return ft.Theme(
        color_scheme_seed=palette["primary"],
        color_scheme=ft.ColorScheme(
            primary=palette["primary"],
            on_primary=palette["text_light"],
            secondary=palette["analogous_1"],
            on_secondary=palette["text_light"],
            error=palette["error"],
            on_error=palette["text_light"],
            surface=palette["bg_white"],
            on_surface=palette["text_primary"],
            surface_variant=palette["bg_secondary"],
            on_surface_variant=palette["text_secondary"],
        ),
        text_theme=ft.TextTheme(
            display_large=ft.TextStyle(size=48, weight=ft.FontWeight.BOLD),
            display_medium=ft.TextStyle(size=32, weight=ft.FontWeight.BOLD),
            headline_large=ft.TextStyle(size=24, weight=ft.FontWeight.W_600),
            headline_medium=ft.TextStyle(size=20, weight=ft.FontWeight.W_600),
            title_large=ft.TextStyle(size=18, weight=ft.FontWeight.W_500),
            title_medium=ft.TextStyle(size=16, weight=ft.FontWeight.W_500),
            body_large=ft.TextStyle(size=14),
            body_medium=ft.TextStyle(size=13),
            body_small=ft.TextStyle(size=12),
            label_large=ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
        ),
    )
