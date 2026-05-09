"""
Integração com APIs de Saúde e Fitness
=======================================

Camada de abstração para importar dados de dispositivos e plataformas.
Suporta: Strava, Garmin Connect (extensível).

Configuração:
  Crie um arquivo .env ou passe credenciais ao instanciar o connector.
  Strava: client_id, client_secret, redirect_uri
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# ── Modelos de dados ─────────────────────────────────────────────

@dataclass
class ActivitySummary:
    """Resumo de uma atividade importada."""
    source: str                     # 'strava', 'garmin', 'manual'
    external_id: str                # ID na plataforma de origem
    name: str
    sport: str                      # Normalizado: Corrida, Ciclismo, Natação
    date: str                       # ISO 8601
    distance_km: float
    duration_minutes: float
    avg_heart_rate: Optional[float] = None
    max_heart_rate: Optional[float] = None
    elevation_gain_m: Optional[float] = None
    avg_pace_min_km: Optional[float] = None
    calories: Optional[float] = None
    raw_data: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)


# ── Mapas de normalização ────────────────────────────────────────

_STRAVA_SPORT_MAP = {
    'Run': 'Corrida',
    'TrailRun': 'Corrida',
    'VirtualRun': 'Corrida',
    'Ride': 'Ciclismo',
    'VirtualRide': 'Ciclismo',
    'Swim': 'Natação',
    'Walk': 'Caminhada',
}


# ── Classe base ──────────────────────────────────────────────────

class FitnessConnector:
    """Interface base para conectores de fitness."""

    name: str = "base"

    def authorize_url(self) -> str:
        """Retorna URL para o utilizador autorizar acesso."""
        raise NotImplementedError

    def exchange_token(self, code: str) -> Dict:
        """Troca código de autorização por access_token."""
        raise NotImplementedError

    def get_activities(self, limit: int = 30) -> List[ActivitySummary]:
        """Retorna últimas atividades."""
        raise NotImplementedError

    def is_connected(self) -> bool:
        """Verifica se há token válido."""
        raise NotImplementedError


# ── Strava ───────────────────────────────────────────────────────

class StravaConnector(FitnessConnector):
    """Conector para a API do Strava (v3)."""

    name = "strava"
    AUTH_URL = "https://www.strava.com/oauth/authorize"
    TOKEN_URL = "https://www.strava.com/oauth/token"
    API_BASE = "https://www.strava.com/api/v3"

    def __init__(self, client_id: str, client_secret: str,
                 redirect_uri: str = "http://localhost:5000/callback",
                 token_path: Optional[str] = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._token_path = Path(token_path) if token_path else (
            Path(__file__).parent / "data" / ".strava_token.json"
        )
        self._token: Optional[Dict] = None
        self._load_token()

    # ── Autenticação ─────────────────────────────────────────

    def authorize_url(self) -> str:
        params = urllib.parse.urlencode({
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "activity:read_all",
        })
        return f"{self.AUTH_URL}?{params}"

    def exchange_token(self, code: str) -> Dict:
        data = urllib.parse.urlencode({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
        }).encode()
        req = urllib.request.Request(self.TOKEN_URL, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            self._token = json.loads(resp.read())
        self._save_token()
        return self._token

    def _refresh_token(self):
        if not self._token or "refresh_token" not in self._token:
            return
        data = urllib.parse.urlencode({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self._token["refresh_token"],
            "grant_type": "refresh_token",
        }).encode()
        req = urllib.request.Request(self.TOKEN_URL, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            self._token = json.loads(resp.read())
        self._save_token()

    def is_connected(self) -> bool:
        return self._token is not None and "access_token" in self._token

    # ── Atividades ───────────────────────────────────────────

    def get_activities(self, limit: int = 30) -> List[ActivitySummary]:
        if not self.is_connected():
            return []
        # Tentar refresh se token expirou
        if self._token.get("expires_at", 0) < datetime.now().timestamp():
            try:
                self._refresh_token()
            except Exception:
                return []

        url = f"{self.API_BASE}/athlete/activities?per_page={limit}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {self._token['access_token']}")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw_list = json.loads(resp.read())
        except urllib.error.HTTPError:
            return []

        return [self._parse_activity(a) for a in raw_list]

    def _parse_activity(self, raw: Dict) -> ActivitySummary:
        sport_type = raw.get("type", raw.get("sport_type", ""))
        sport = _STRAVA_SPORT_MAP.get(sport_type, sport_type)
        distance_km = raw.get("distance", 0) / 1000
        duration_min = raw.get("moving_time", 0) / 60
        avg_pace = (duration_min / distance_km) if distance_km > 0 else None

        return ActivitySummary(
            source="strava",
            external_id=str(raw.get("id", "")),
            name=raw.get("name", ""),
            sport=sport,
            date=raw.get("start_date_local", raw.get("start_date", "")),
            distance_km=round(distance_km, 2),
            duration_minutes=round(duration_min, 1),
            avg_heart_rate=raw.get("average_heartrate"),
            max_heart_rate=raw.get("max_heartrate"),
            elevation_gain_m=raw.get("total_elevation_gain"),
            avg_pace_min_km=round(avg_pace, 2) if avg_pace else None,
            calories=raw.get("calories"),
            raw_data=raw,
        )

    # ── Persistência do token ────────────────────────────────

    def _load_token(self):
        if self._token_path.exists():
            try:
                with open(self._token_path, "r", encoding="utf-8") as f:
                    self._token = json.load(f)
            except Exception:
                self._token = None

    def _save_token(self):
        self._token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._token_path, "w", encoding="utf-8") as f:
            json.dump(self._token, f, indent=2)


# ── Garmin (stub) ────────────────────────────────────────────────

class GarminConnector(FitnessConnector):
    """
    Stub para integração com Garmin Connect.

    A API oficial do Garmin requer parceria comercial.
    Este stub permite extensão futura quando disponível.
    """

    name = "garmin"

    def authorize_url(self) -> str:
        raise NotImplementedError("Garmin Connect requer parceria comercial para API.")

    def exchange_token(self, code: str) -> Dict:
        raise NotImplementedError

    def get_activities(self, limit: int = 30) -> List[ActivitySummary]:
        return []

    def is_connected(self) -> bool:
        return False


# ── SmartWatch / Wearables ───────────────────────────────────────

class SmartWatchConnector(FitnessConnector):
    """Interface base para conectores de smartwatch/wearables."""

    name: str = "smartwatch"
    device_type: str = "generic"  # garmin, apple, fitbit, samsung

    def authorize_url(self) -> str:
        """Retorna URL para o utilizador autorizar acesso ao dispositivo."""
        raise NotImplementedError

    def exchange_token(self, code: str) -> Dict:
        """Troca código de autorização por access_token."""
        raise NotImplementedError

    def get_activities(self, limit: int = 30) -> List[ActivitySummary]:
        """Retorna últimas atividades sincronizadas do relógio."""
        raise NotImplementedError

    def is_connected(self) -> bool:
        """Verifica se há conexão ativa com o dispositivo."""
        raise NotImplementedError

    def pair_device(self, device_id: str) -> bool:
        """Emparelha um novo dispositivo."""
        raise NotImplementedError

    def sync_now(self) -> bool:
        """Força sincronização imediata com dispositivo."""
        raise NotImplementedError


class GarminWatchConnector(SmartWatchConnector):
    """
    Stub para integração com Garmin Devices (Edge, Watch, etc).

    Suporta sincronização de atividades de dispositivos Garmin.
    Configuração necessária:
      - Garmin Connect credentials ou personal token
    """

    name = "garmin_watch"
    device_type = "garmin"

    def __init__(self, email: str = "", password: str = ""):
        self.email = email
        self.password = password
        self.connected = False

    def authorize_url(self) -> str:
        # Garmin Connect OAuth would go here
        return ""

    def exchange_token(self, code: str) -> Dict:
        return {}

    def get_activities(self, limit: int = 30) -> List[ActivitySummary]:
        return []

    def is_connected(self) -> bool:
        return self.connected

    def pair_device(self, device_id: str) -> bool:
        self.connected = True
        return True

    def sync_now(self) -> bool:
        return True


class AppleWatchConnector(SmartWatchConnector):
    """
    Stub para integração com Apple Watch / HealthKit.

    Macros está disponível apenas no ecossistema Apple.
    """

    name = "apple_watch"
    device_type = "apple"

    def authorize_url(self) -> str:
        return ""

    def exchange_token(self, code: str) -> Dict:
        return {}

    def get_activities(self, limit: int = 30) -> List[ActivitySummary]:
        return []

    def is_connected(self) -> bool:
        return False

    def pair_device(self, device_id: str) -> bool:
        return False

    def sync_now(self) -> bool:
        return False


class FitbitConnector(SmartWatchConnector):
    """
    Stub para integração com Fitbit.

    Requer autenticação OAuth2 com Fitbit API.
    """

    name = "fitbit"
    device_type = "fitbit"

    def __init__(self, client_id: str = "", client_secret: str = ""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.connected = False

    def authorize_url(self) -> str:
        return ""

    def exchange_token(self, code: str) -> Dict:
        return {}

    def get_activities(self, limit: int = 30) -> List[ActivitySummary]:
        return []

    def is_connected(self) -> bool:
        return self.connected

    def pair_device(self, device_id: str) -> bool:
        self.connected = True
        return True

    def sync_now(self) -> bool:
        return True


class SamsungConnector(SmartWatchConnector):
    """
    Stub para integração com Samsung Galaxy Watch.

    Requer Samsung Health API e credenciais apropriadas.
    """

    name = "samsung"
    device_type = "samsung"

    def authorize_url(self) -> str:
        return ""

    def exchange_token(self, code: str) -> Dict:
        return {}

    def get_activities(self, limit: int = 30) -> List[ActivitySummary]:
        return []

    def is_connected(self) -> bool:
        return False

    def pair_device(self, device_id: str) -> bool:
        return False

    def sync_now(self) -> bool:
        return False


# ── Registo de conectores ────────────────────────────────────────

CONNECTORS = {
    "strava": StravaConnector,
    "garmin": GarminConnector,
    "garmin_watch": GarminWatchConnector,
    "apple_watch": AppleWatchConnector,
    "fitbit": FitbitConnector,
    "samsung": SamsungConnector,
}
