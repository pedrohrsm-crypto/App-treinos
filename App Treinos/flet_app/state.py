"""
Estado Global da Aplicação
===========================

Armazena sessão do utilizador logado, atleta selecionado,
e preferências partilhadas entre telas.
Inclui persistência de preferências e sessão via JSON local.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict


def _prefs_path() -> Path:
    """Retorna caminho do ficheiro de preferências."""
    p = Path(__file__).parent.parent / "data"
    p.mkdir(exist_ok=True)
    return p / "preferences.json"


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

    # ── DB singleton (inicializado no splash) ────────────────────
    db: object = None  # DatabaseManager instance

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
        self.clear_session()

    @property
    def is_logged_in(self) -> bool:
        return self.user is not None

    def trainer_info(self):
        """Retorna dict compatível com training_manager (precisa de 'cref')."""
        return {"cref": self.trainer_cref} if self.trainer_cref else None

    # ── Persistência de preferências ─────────────────────────────

    def save_preferences(self):
        """Persiste dark_mode e language em JSON."""
        data = self._read_prefs_file()
        key = self.trainer_cref or "_global"
        data[key] = {"dark_mode": self.dark_mode, "language": self.language}
        self._write_prefs_file(data)

    # ── Onboarding ───────────────────────────────────────────────

    def is_onboarding_completed(self) -> bool:
        """Verifica se o onboarding já foi concluído."""
        data = self._read_prefs_file()
        return data.get("_onboarding_completed", False)

    def set_onboarding_completed(self):
        """Marca o onboarding como concluído."""
        data = self._read_prefs_file()
        data["_onboarding_completed"] = True
        self._write_prefs_file(data)

    def load_preferences(self) -> Optional[Dict]:
        """Carrega preferências do treinador logado (ou _global)."""
        data = self._read_prefs_file()
        key = self.trainer_cref or "_global"
        return data.get(key)

    # ── Persistência de sessão (auto-login) ──────────────────────

    def save_session(self, credential: str, password_raw: str):
        """Guarda credenciais para auto-login (ficheiro local).

        Armazena o hash da DB (PBKDF2) após autenticação bem-sucedida,
        nunca a senha em texto claro.
        """
        # Obter o hash armazenado na DB para este utilizador
        import sqlite3
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'SELECT senha_hash FROM usuarios WHERE (cpf = ? OR cref = ?) AND ativo = 1',
                (credential, credential)
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                db_hash = row[0]
            else:
                return  # Utilizador não encontrado, não guardar sessão
        except Exception:
            return

        data = self._read_prefs_file()
        data["_session"] = {"credential": credential, "password_hash": db_hash}
        self._write_prefs_file(data)

    def load_session(self) -> Optional[Dict]:
        """Carrega sessão guardada."""
        data = self._read_prefs_file()
        return data.get("_session")

    def clear_session(self):
        """Remove sessão guardada."""
        data = self._read_prefs_file()
        data.pop("_session", None)
        self._write_prefs_file(data)

    # ── I/O helpers ──────────────────────────────────────────────

    def _read_prefs_file(self) -> dict:
        path = _prefs_path()
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _write_prefs_file(self, data: dict):
        path = _prefs_path()
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )


# Instância global
app_state = AppState()
