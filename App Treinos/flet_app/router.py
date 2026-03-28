"""
Router — Navegação por rotas nomeadas
======================================

Encapsula a troca de telas (Views) e o histórico de navegação.
Cada rota mapeia para uma função-fábrica que recebe (page, app_state)
e retorna um ft.View.
"""

import flet as ft
from typing import Callable, Dict


class Router:
    """Gerencia navegação entre telas da aplicação."""

    def __init__(self, page: ft.Page):
        self.page = page
        self._routes: Dict[str, Callable] = {}
        page.on_route_change = self._on_route_change
        page.on_view_pop = self._on_view_pop

    # ── Registo de rotas ─────────────────────────────────────────

    def add(self, pattern: str, builder: Callable):
        """Registra uma rota. *pattern* é ex. '/login' ou '/athlete'."""
        self._routes[pattern] = builder

    # ── Navegação ────────────────────────────────────────────────

    def go(self, route: str):
        """Navega para *route*."""
        self.page.go(route)

    def back(self):
        """Volta à rota anterior."""
        if len(self.page.views) > 1:
            self.page.views.pop()
            top = self.page.views[-1]
            self.page.go(top.route)

    # ── Callbacks internos ───────────────────────────────────────

    def _resolve(self, route: str) -> Callable | None:
        """Encontra builder para a rota, incluindo rotas dinâmicas."""
        if route in self._routes:
            return self._routes[route]
        # Rotas dinâmicas: /athlete/XXXX → /athlete
        parts = route.rstrip("/").rsplit("/", 1)
        if len(parts) == 2 and parts[0] in self._routes:
            return self._routes[parts[0]]
        return None

    def _on_route_change(self, e: ft.RouteChangeEvent):
        route = e.route
        builder = self._resolve(route)
        if builder is None:
            builder = self._routes.get("/login")
        if builder is None:
            return

        view = builder(self.page, route)
        self.page.views.clear()
        self.page.views.append(view)
        self.page.update()

    def _on_view_pop(self, e: ft.ViewPopEvent):
        if len(self.page.views) > 1:
            self.page.views.pop()
            top = self.page.views[-1]
            self.page.go(top.route)
