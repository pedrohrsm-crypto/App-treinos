"""
Estado Global da Aplicação
===========================

Armazena sessão do utilizador logado, atleta selecionado,
e outras preferências partilhadas entre telas.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass
class AppState:
    """Singleton que mantém o estado global entre telas."""

    # ── Sessão ───────────────────────────────────────────────────
    user: Optional[Dict] = None       # Dados do utilizador autenticado
    trainer_cref: Optional[str] = None
    trainer_name: Optional[str] = None
    is_admin: bool = False

    # ── Navegação ────────────────────────────────────────────────
    selected_athlete: Optional[str] = None  # athlete_name do card clicado
    selected_plan_id: Optional[str] = None  # plan_id para calendário

    # ── Preferências ─────────────────────────────────────────────
    dark_mode: bool = False
    language: str = "pt"

    # ── Helpers ──────────────────────────────────────────────────

    def login(self, user_data: Dict):
        """Preenche estado após autenticação bem-sucedida."""
        self.user = user_data
        self.trainer_cref = user_data.get("cref", "")
        self.trainer_name = user_data.get("nome", "")
        self.is_admin = user_data.get("tipo") == "admin"

    def logout(self):
        """Limpa sessão."""
        self.user = None
        self.trainer_cref = None
        self.trainer_name = None
        self.is_admin = False
        self.selected_athlete = None
        self.selected_plan_id = None

    @property
    def is_logged_in(self) -> bool:
        return self.user is not None

    def trainer_info(self):
        """Retorna dict compatível com training_manager (precisa de 'cref')."""
        return {"cref": self.trainer_cref} if self.trainer_cref else None


# Instância global
app_state = AppState()
