"""
Configuração Centralizada — App Treinos

Carrega todas as configurações de:
- Environment variables
- Ficheiros .env
- Valores padrão
"""

import os
from pathlib import Path
from typing import Optional

from app_treinos.version import __version__


class AppConfig:
    """Configuração centralizada da aplicação."""

    def __init__(self):
        # ── Versão ───────────────────────────────────────────────
        self.version = __version__

        # ── Environment ──────────────────────────────────────────
        self.environment = os.getenv("APP_ENV", "production").lower()
        self.debug = self.environment in ("development", "dev")
        self.is_ci = os.getenv("CI", "false").lower() == "true"

        # ── Paths ────────────────────────────────────────────────
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / "data"
        self.logs_dir = self.project_root / "logs"
        self.db_path = self.data_dir / "app_treinos.db"

        # ── Database ─────────────────────────────────────────────
        self.db_type = os.getenv("DB_TYPE", "sqlite")  # sqlite | mysql
        self.db_exists = self.db_path.exists()

        # MySQL (if needed)
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_user = os.getenv("DB_USER", "")
        self.db_pass = os.getenv("DB_PASS", "")
        self.db_name = os.getenv("DB_NAME", "app_treinos")

        # ── AI Configuration ─────────────────────────────────────
        self.ai_provider = os.getenv("AI_PROVIDER", "openai")
        self.ai_api_key = os.getenv("AI_API_KEY", "")
        self.ai_model = os.getenv("AI_MODEL", "gpt-4o-mini")
        self.ai_timeout = int(os.getenv("AI_TIMEOUT", "30"))

        # ── Logging ──────────────────────────────────────────────
        self.log_level = os.getenv("LOG_LEVEL", "INFO" if not self.debug else "DEBUG")
        self.log_file = self.logs_dir / "app.log"

        # ── UI ───────────────────────────────────────────────────
        self.window_width = int(os.getenv("WINDOW_WIDTH", "1024"))
        self.window_height = int(os.getenv("WINDOW_HEIGHT", "720"))
        self.theme_mode = os.getenv("THEME_MODE", "light")  # light | dark

        # ── Security ────────────────────────────────────────────
        self.pbkdf2_iterations = int(os.getenv("PBKDF2_ITER", "100000"))

        # Criar diretórios se não existirem
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def load(cls) -> "AppConfig":
        """Carrega configuração do ambiente."""
        # TODO: Carregar .env se existir
        return cls()

    @property
    def is_development(self) -> bool:
        """Está em modo desenvolvimento?"""
        return self.debug

    @property
    def is_production(self) -> bool:
        """Está em modo produção?"""
        return self.environment == "production"

    def __repr__(self) -> str:
        return (
            f"AppConfig(version={self.version}, "
            f"env={self.environment}, "
            f"db={self.db_type} @ {self.db_path})"
        )
