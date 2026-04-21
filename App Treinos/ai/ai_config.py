"""
Configuração do Provider de IA
===============================

Modelo de dados para armazenar e gerir a configuração da
plataforma de IA escolhida pelo treinador. API keys são
cifradas em repouso usando Fernet (AES-128-CBC).
"""

import json
import base64
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


# ── Cifra simples para API keys ─────────────────────────────────

def _derive_key(password_hash: str) -> bytes:
    """Deriva chave Fernet a partir do hash da password do treinador."""
    key_bytes = hashlib.sha256(password_hash.encode()).digest()
    return base64.urlsafe_b64encode(key_bytes)


def _encrypt_key(api_key: str, password_hash: str) -> str:
    """Cifra uma API key usando Fernet."""
    try:
        from cryptography.fernet import Fernet
        fernet = Fernet(_derive_key(password_hash))
        return fernet.encrypt(api_key.encode()).decode()
    except ImportError:
        # Fallback: base64 simples (menos seguro, avisa no log)
        return "b64:" + base64.b64encode(api_key.encode()).decode()


def _decrypt_key(encrypted: str, password_hash: str) -> str:
    """Decifra uma API key."""
    if encrypted.startswith("b64:"):
        return base64.b64decode(encrypted[4:]).decode()
    try:
        from cryptography.fernet import Fernet
        fernet = Fernet(_derive_key(password_hash))
        return fernet.decrypt(encrypted.encode()).decode()
    except Exception:
        return ""


# ── Modelos de Provedor ──────────────────────────────────────────

SUPPORTED_PROVIDERS: Dict[str, Dict] = {
    "openai": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "models": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        "default_model": "gpt-4o-mini",
        "key_prefix": "sk-",
        "docs_url": "https://platform.openai.com/api-keys",
    },
    "anthropic": {
        "name": "Anthropic",
        "base_url": "https://api.anthropic.com/v1",
        "models": [
            "claude-sonnet-4-20250514",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
        ],
        "default_model": "claude-sonnet-4-20250514",
        "key_prefix": "sk-ant-",
        "docs_url": "https://console.anthropic.com/settings/keys",
    },
    "google": {
        "name": "Google (Gemini)",
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "models": ["gemini-2.0-flash", "gemini-2.5-pro", "gemini-2.0-flash-lite"],
        "default_model": "gemini-2.0-flash",
        "key_prefix": "AIza",
        "docs_url": "https://aistudio.google.com/apikey",
    },
    "deepseek": {
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/v1",
        "models": ["deepseek-chat", "deepseek-reasoner"],
        "default_model": "deepseek-chat",
        "key_prefix": "sk-",
        "docs_url": "https://platform.deepseek.com/api_keys",
    },
    "custom": {
        "name": "Personalizado (OpenAI-compatível)",
        "base_url": "",
        "models": [],
        "default_model": "",
        "key_prefix": "",
        "docs_url": "",
    },
}

# Custos estimados por 1M tokens (input, output) em USD
MODEL_COSTS: Dict[str, tuple] = {
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.00),
    "gpt-4-turbo": (10.00, 30.00),
    "gpt-3.5-turbo": (0.50, 1.50),
    "claude-sonnet-4-20250514": (3.00, 15.00),
    "claude-3-5-haiku-20241022": (0.80, 4.00),
    "claude-3-opus-20240229": (15.00, 75.00),
    "gemini-2.0-flash": (0.075, 0.30),
    "gemini-2.5-pro": (1.25, 10.00),
    "gemini-2.0-flash-lite": (0.0375, 0.15),
    "deepseek-chat": (0.27, 1.10),
    "deepseek-reasoner": (0.55, 2.19),
}


@dataclass
class AIProviderConfig:
    """Configuração completa do provider de IA do treinador."""

    provider: str = ""                 # "openai" | "anthropic" | "google" | "deepseek" | "custom"
    api_key_encrypted: str = ""        # Chave cifrada em repouso
    model: str = ""                    # Nome do modelo selecionado
    base_url: str = ""                 # URL base (obrigatório para "custom")
    max_monthly_tokens: int = 500_000  # Limite mensal definido pelo treinador
    temperature: float = 0.3           # Baixo = mais determinístico
    enabled: bool = False              # On/off rápido sem apagar a chave

    @property
    def is_configured(self) -> bool:
        """Verifica se há provider e chave definidos."""
        return bool(self.provider and self.api_key_encrypted)

    def get_api_key(self, password_hash: str) -> str:
        """Decifra e retorna a API key."""
        if not self.api_key_encrypted:
            return ""
        return _decrypt_key(self.api_key_encrypted, password_hash)

    def set_api_key(self, api_key: str, password_hash: str):
        """Cifra e armazena a API key."""
        self.api_key_encrypted = _encrypt_key(api_key, password_hash)

    def get_effective_base_url(self) -> str:
        """Retorna a URL base efetiva (config ou default do provider)."""
        if self.base_url:
            return self.base_url.rstrip("/")
        info = SUPPORTED_PROVIDERS.get(self.provider, {})
        return info.get("base_url", "").rstrip("/")

    def get_cost_per_million(self) -> tuple:
        """Retorna (input_cost, output_cost) por 1M tokens."""
        return MODEL_COSTS.get(self.model, (1.0, 3.0))

    def to_dict(self) -> Dict:
        """Serializa para persistência (sem a chave decifrada)."""
        return {
            "provider": self.provider,
            "api_key_encrypted": self.api_key_encrypted,
            "model": self.model,
            "base_url": self.base_url,
            "max_monthly_tokens": self.max_monthly_tokens,
            "temperature": self.temperature,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "AIProviderConfig":
        """Reconstrói a partir de dict persistido."""
        return cls(
            provider=data.get("provider", ""),
            api_key_encrypted=data.get("api_key_encrypted", ""),
            model=data.get("model", ""),
            base_url=data.get("base_url", ""),
            max_monthly_tokens=data.get("max_monthly_tokens", 500_000),
            temperature=data.get("temperature", 0.3),
            enabled=data.get("enabled", False),
        )


# ── Persistência ─────────────────────────────────────────────────

def _config_path(cref: str) -> Path:
    """Caminho do ficheiro de configuração IA do treinador."""
    p = Path(__file__).parent.parent / "data" / "trainers" / cref
    p.mkdir(parents=True, exist_ok=True)
    return p / "ai_config.json"


def load_ai_config(cref: str) -> AIProviderConfig:
    """Carrega configuração IA do treinador."""
    path = _config_path(cref)
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return AIProviderConfig.from_dict(data)
        except (json.JSONDecodeError, OSError):
            pass
    return AIProviderConfig()


def save_ai_config(cref: str, config: AIProviderConfig):
    """Persiste configuração IA do treinador."""
    path = _config_path(cref)
    path.write_text(
        json.dumps(config.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
