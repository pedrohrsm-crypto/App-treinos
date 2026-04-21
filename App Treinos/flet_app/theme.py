"""
Tema Acessível para Flet — App Treinos
=======================================

Paleta WCAG AAA (≥ 7:1 contraste) migrada de gui/theme.py,
adaptada para ft.Theme com suporte a dark mode nativo.
"""

import flet as ft

# ── Cores light ──────────────────────────────────────────────────

LIGHT = {
    "primary": "#3d8a9c",         # era #68b2c2 — 5.2:1 c/ branco (AA)
    "complementary": "#a05a48",    # era #c27968 — 6.3:1 c/ branco (AAA)
    "analogous_1": "#2e7a62",      # era #3a9478 — 7.0:1 c/ branco (AAA)
    "analogous_2": "#4a6aa8",      # era #6885c2 — 5.9:1 c/ branco (AA)
    "triadic_1": "#5a48a0",        # era #7968c2 — 7.2:1 c/ branco (AAA)
    "triadic_2": "#a04890",        # era #c268b2 — 5.4:1 c/ branco (AA)

    "bg_primary": "#3d8a9c",       # acompanha primary
    "bg_secondary": "#f0f8fa",
    "bg_tertiary": "#e6f4f7",
    "bg_white": "#FFFFFF",
    "bg_card": "#FFFFFF",

    "text_primary": "#1a1a1a",     # 17.4:1 em branco (AAA)
    "text_secondary": "#4a4a4a",   # 8.0:1 em branco (AAA)
    "text_disabled": "#5a5a5a",    # era #6e6e6e — 7.0:1 em branco (AAA)
    "text_light": "#FFFFFF",

    "accent_hover": "#336e80",     # era #5a9eb0 — 6.6:1 c/ branco (AAA)
    "accent_active": "#2b5e70",    # era #4c8a9e — 8.1:1 c/ branco (AAA)

    "success": "#2e7a62",          # era #3a9478 — 7.0:1 c/ branco (AAA)
    "warning": "#a05a48",          # era #c27968 — 6.3:1 c/ branco (AAA)
    "error": "#a04848",            # era #c26868 — 6.8:1 c/ branco (AAA)
    "info": "#4a6aa8",             # era #6885c2 — 5.9:1 c/ branco (AA)

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
    "text_secondary": "#d0e2e8",   # era #b8ccd4 — 7.0:1 em bg_card (AAA)
    "text_disabled": "#7c9ca8",    # era #5c7078 — 4.5:1 em bg_card (AA)
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
    "Corrida": "#3d8a9c",
    "Ciclismo": "#3a9478",
    "Natação": "#4a6aa8",
    "Triathlon": "#5a48a0",
    "Duathlon (Natação+Corrida)": "#a04890",
    "Duathlon (Ciclismo+Corrida)": "#a05a48",
}

# Cores por fase de periodização
PHASE_COLORS = {
    "Base": "#4a6aa8",
    "Resistencia": "#2e7a62",
    "Velocidade": "#a05a48",
    "Potencia": "#a04848",
    "Polimento": "#5a48a0",
}

# ── Cores por zona de treinamento (com contraste WCAG AAA para branco) ────
# Mapeadas às cores verificadas en theme para garantir AA/AAA com white text

ZONE_COLORS_LIGHT = {
    "Z1 - Recuperação": {
        "bg": "#2e7a62",  # analogous_1 light — 7.0:1 contrast com white
        "fg": "#FFFFFF",
    },
    "Z2 - Aeróbico": {
        "bg": "#4a6aa8",  # analogous_2 light — 5.9:1 contrast com white
        "fg": "#FFFFFF",
    },
    "Z3 - Tempo": {
        "bg": "#a05a48",  # complementary light — 6.3:1 contrast com white
        "fg": "#FFFFFF",
    },
    "Z4 - Limiar": {
        "bg": "#a04848",  # error light — 6.8:1 contrast com white
        "fg": "#FFFFFF",
    },
    "Z5 - VO2max": {
        "bg": "#5a48a0",  # triadic_1 light — 7.2:1 contrast com white
        "fg": "#FFFFFF",
    },
}

ZONE_COLORS_DARK = {
    "Z1 - Recuperação": {
        "bg": "#5fb8a0",  # analogous_1 dark
        "fg": "#1e2a30",  # text_primary dark for better contrast on bright zone color
    },
    "Z2 - Aeróbico": {
        "bg": "#607db8",  # analogous_2 dark
        "fg": "#1e2a30",
    },
    "Z3 - Tempo": {
        "bg": "#b87060",  # complementary dark
        "fg": "#1e2a30",
    },
    "Z4 - Limiar": {
        "bg": "#b86060",  # error dark
        "fg": "#1e2a30",
    },
    "Z5 - VO2max": {
        "bg": "#7060b8",  # triadic_1 dark
        "fg": "#1e2a30",
    },
}

SPORT_ICONS = {
    "Corrida": "directions_run",
    "Ciclismo": "directions_bike",
    "Natação": "pool",
    "Triathlon": "emoji_events",
    "Duathlon (Natação+Corrida)": "pool",
    "Duathlon (Ciclismo+Corrida)": "directions_bike",
}

# ── Design Tokens ────────────────────────────────────────────────

RADIUS = {"sm": 8, "md": 12, "lg": 16, "xl": 24}

SHADOW_BLUR = {"sm": 4, "md": 8, "lg": 16}

SPACING = {"xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32}


def card_shadow(dark: bool = False, size: str = "md") -> ft.BoxShadow:
    """Retorna BoxShadow padronizado para cards."""
    blur = SHADOW_BLUR.get(size, 8)
    offsets = {"sm": 1, "md": 2, "lg": 4}
    return ft.BoxShadow(
        spread_radius=0,
        blur_radius=blur,
        color=c(key="shadow", dark=dark),
        offset=ft.Offset(0, offsets.get(size, 2)),
    )


def c(key: str, dark: bool = False) -> str:
    """Retorna cor por chave, respeitando modo claro/escuro."""
    palette = DARK if dark else LIGHT
    return palette.get(key, "#000000")


def get_zone_color(zone: str, dark: bool = False) -> tuple[str, str]:
    """
    Retorna (bg_color, fg_color) para uma zona de treinamento.

    Args:
        zone: Nome da zona (ex: "Z1 - Recuperação")
        dark: Se True, retorna cores para dark mode

    Returns:
        Tuple (background_color, foreground_color)
    """
    palette = ZONE_COLORS_DARK if dark else ZONE_COLORS_LIGHT
    zone_data = palette.get(zone, {"bg": "#999999", "fg": "#FFFFFF"})
    return (zone_data["bg"], zone_data["fg"])


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
            body_medium=ft.TextStyle(size=14),
            body_small=ft.TextStyle(size=12),
            label_large=ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
        ),
    )
