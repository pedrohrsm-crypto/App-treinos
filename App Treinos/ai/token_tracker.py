"""
Rastreador de Consumo de Tokens
================================

Regista cada chamada à IA, calcula custos, detecta
proximidade e esgotamento do limite mensal.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from ai.ai_config import MODEL_COSTS


@dataclass
class TokenUsageEntry:
    """Uma utilização individual de tokens."""

    timestamp: str = ""
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    action: str = ""           # ex.: "optimize_plan", "suggest_edit"
    cost_usd: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "model": self.model,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "action": self.action,
            "cost_usd": self.cost_usd,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "TokenUsageEntry":
        return cls(
            timestamp=d.get("timestamp", ""),
            model=d.get("model", ""),
            input_tokens=d.get("input_tokens", 0),
            output_tokens=d.get("output_tokens", 0),
            action=d.get("action", ""),
            cost_usd=d.get("cost_usd", 0.0),
        )


class TokenTracker:
    """Gere o histórico de consumo de tokens por treinador."""

    WARNING_THRESHOLD = 0.80   # 80% = aviso
    BLOCK_THRESHOLD = 1.00     # 100% = bloqueio

    def __init__(self, cref: str):
        self.cref = cref
        self._entries: List[TokenUsageEntry] = []
        self._month_key: str = ""
        self._load()

    # ── Caminho ──────────────────────────────────────────────────

    def _usage_path(self) -> Path:
        p = Path(__file__).parent.parent / "data" / "trainers" / self.cref
        p.mkdir(parents=True, exist_ok=True)
        return p / "ai_usage.json"

    # ── Persistência ─────────────────────────────────────────────

    def _load(self):
        path = self._usage_path()
        current_month = datetime.now().strftime("%Y-%m")
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                self._month_key = data.get("month", "")
                self._entries = [
                    TokenUsageEntry.from_dict(e)
                    for e in data.get("entries", [])
                ]
            except (json.JSONDecodeError, OSError):
                self._month_key = current_month
                self._entries = []
        else:
            self._month_key = current_month
            self._entries = []

        # Auto-reset mensal
        if self._month_key != current_month:
            self._month_key = current_month
            self._entries = []
            self._save()

    def _save(self):
        path = self._usage_path()
        data = {
            "month": self._month_key,
            "entries": [e.to_dict() for e in self._entries],
        }
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ── Registo ──────────────────────────────────────────────────

    def record(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        action: str = "",
    ):
        """Regista uma utilização de tokens."""
        cost = self._estimate_cost(model, input_tokens, output_tokens)
        entry = TokenUsageEntry(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            action=action,
            cost_usd=round(cost, 6),
        )
        self._entries.append(entry)
        self._save()

    # ── Consultas ────────────────────────────────────────────────

    @property
    def total_tokens(self) -> int:
        return sum(e.input_tokens + e.output_tokens for e in self._entries)

    @property
    def total_cost_usd(self) -> float:
        return round(sum(e.cost_usd for e in self._entries), 4)

    @property
    def entry_count(self) -> int:
        return len(self._entries)

    def usage_ratio(self, max_monthly: int) -> float:
        """Retorna 0.0 – 1.0+ consoante a utilização vs limite."""
        if max_monthly <= 0:
            return 0.0
        return self.total_tokens / max_monthly

    def is_near_limit(self, max_monthly: int) -> bool:
        """True se >= 80% do limite mensal."""
        return self.usage_ratio(max_monthly) >= self.WARNING_THRESHOLD

    def is_over_limit(self, max_monthly: int) -> bool:
        """True se >= 100% do limite mensal."""
        return self.usage_ratio(max_monthly) >= self.BLOCK_THRESHOLD

    def remaining_tokens(self, max_monthly: int) -> int:
        """Tokens restantes no mês."""
        return max(0, max_monthly - self.total_tokens)

    def get_summary(self, max_monthly: int) -> Dict:
        """Resumo para exibição na UI."""
        return {
            "month": self._month_key,
            "total_tokens": self.total_tokens,
            "max_monthly": max_monthly,
            "remaining": self.remaining_tokens(max_monthly),
            "usage_pct": round(self.usage_ratio(max_monthly) * 100, 1),
            "total_cost_usd": self.total_cost_usd,
            "requests": self.entry_count,
            "near_limit": self.is_near_limit(max_monthly),
            "over_limit": self.is_over_limit(max_monthly),
        }

    # ── Custo ────────────────────────────────────────────────────

    @staticmethod
    def _estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
        """Calcula custo estimado em USD."""
        input_per_m, output_per_m = MODEL_COSTS.get(model, (1.0, 3.0))
        return (input_tokens * input_per_m + output_tokens * output_per_m) / 1_000_000
