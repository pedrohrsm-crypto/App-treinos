"""
Testes do Módulo de Integração de IA
======================================

Testes unitários com mocks (sem chamadas reais a APIs).
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ajustar path para importações
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai.ai_config import (
    AIProviderConfig,
    SUPPORTED_PROVIDERS,
    _encrypt_key,
    _decrypt_key,
    load_ai_config,
    save_ai_config,
)
from ai.ai_provider import AIResponse, Message, create_provider
from ai.token_tracker import TokenTracker, TokenUsageEntry
from ai import prompt_templates


# ═══════════════════════════════════════════════════════════════════
# AIProviderConfig
# ═══════════════════════════════════════════════════════════════════


class TestAIProviderConfig(unittest.TestCase):
    """Testes para configuração e cifra de API keys."""

    def test_default_config_not_configured(self):
        cfg = AIProviderConfig()
        self.assertFalse(cfg.is_configured)
        self.assertFalse(cfg.enabled)

    def test_configured_when_provider_and_key_set(self):
        cfg = AIProviderConfig(provider="openai", api_key_encrypted="xxx")
        self.assertTrue(cfg.is_configured)

    def test_encrypt_decrypt_roundtrip_b64_fallback(self):
        """Quando cryptography não está disponível, usa b64."""
        key = "sk-test-12345"
        pw = "myhash"
        encrypted = _encrypt_key(key, pw)
        # Pode ser Fernet ou b64 dependendo da disponibilidade
        decrypted = _decrypt_key(encrypted, pw)
        self.assertEqual(decrypted, key)

    def test_set_get_api_key(self):
        cfg = AIProviderConfig(provider="openai")
        cfg.set_api_key("sk-abc123", "hash99")
        retrieved = cfg.get_api_key("hash99")
        self.assertEqual(retrieved, "sk-abc123")

    def test_to_dict_from_dict_roundtrip(self):
        cfg = AIProviderConfig(
            provider="anthropic",
            api_key_encrypted="enc123",
            model="claude-sonnet-4-20250514",
            base_url="",
            max_monthly_tokens=1_000_000,
            temperature=0.5,
            enabled=True,
        )
        d = cfg.to_dict()
        cfg2 = AIProviderConfig.from_dict(d)
        self.assertEqual(cfg.provider, cfg2.provider)
        self.assertEqual(cfg.model, cfg2.model)
        self.assertEqual(cfg.max_monthly_tokens, cfg2.max_monthly_tokens)
        self.assertEqual(cfg.temperature, cfg2.temperature)
        self.assertEqual(cfg.enabled, cfg2.enabled)

    def test_get_effective_base_url_default(self):
        cfg = AIProviderConfig(provider="openai")
        self.assertEqual(cfg.get_effective_base_url(), "https://api.openai.com/v1")

    def test_get_effective_base_url_custom(self):
        cfg = AIProviderConfig(provider="custom", base_url="http://localhost:11434/v1/")
        self.assertEqual(cfg.get_effective_base_url(), "http://localhost:11434/v1")

    def test_get_cost_per_million(self):
        cfg = AIProviderConfig(model="gpt-4o-mini")
        cost = cfg.get_cost_per_million()
        self.assertEqual(cost, (0.15, 0.60))

    def test_get_cost_unknown_model(self):
        cfg = AIProviderConfig(model="unknown-model-xyz")
        cost = cfg.get_cost_per_million()
        self.assertEqual(cost, (1.0, 3.0))  # fallback

    def test_supported_providers_have_required_fields(self):
        required = {"name", "base_url", "models", "default_model"}
        for key, info in SUPPORTED_PROVIDERS.items():
            for field in required:
                self.assertIn(field, info, f"{key} missing {field}")


class TestAIConfigPersistence(unittest.TestCase):
    """Testes de save/load da configuração."""

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        self._patch = patch(
            "ai.ai_config._config_path",
            return_value=Path(self._tmpdir) / "ai_config.json",
        )
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        import shutil
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def test_save_and_load(self):
        cfg = AIProviderConfig(
            provider="google",
            api_key_encrypted="enc",
            model="gemini-2.0-flash",
            enabled=True,
        )
        save_ai_config("TEST", cfg)
        loaded = load_ai_config("TEST")
        self.assertEqual(loaded.provider, "google")
        self.assertEqual(loaded.model, "gemini-2.0-flash")
        self.assertTrue(loaded.enabled)

    def test_load_missing_returns_default(self):
        loaded = load_ai_config("NONEXISTENT")
        self.assertFalse(loaded.is_configured)


# ═══════════════════════════════════════════════════════════════════
# AIResponse
# ═══════════════════════════════════════════════════════════════════


class TestAIResponse(unittest.TestCase):

    def test_total_tokens(self):
        r = AIResponse(input_tokens=100, output_tokens=50)
        self.assertEqual(r.total_tokens, 150)

    def test_is_error(self):
        r = AIResponse(error_message="boom")
        self.assertTrue(r.is_error)

    def test_not_error(self):
        r = AIResponse(content="ok")
        self.assertFalse(r.is_error)


# ═══════════════════════════════════════════════════════════════════
# TokenTracker
# ═══════════════════════════════════════════════════════════════════


class TestTokenTracker(unittest.TestCase):

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        self._patch = patch.object(
            TokenTracker,
            "_usage_path",
            return_value=Path(self._tmpdir) / "ai_usage.json",
        )
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        import shutil
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def test_empty_tracker(self):
        t = TokenTracker("TEST")
        self.assertEqual(t.total_tokens, 0)
        self.assertEqual(t.entry_count, 0)
        self.assertEqual(t.total_cost_usd, 0.0)

    def test_record_and_total(self):
        t = TokenTracker("TEST")
        t.record("gpt-4o-mini", input_tokens=100, output_tokens=50, action="test")
        self.assertEqual(t.total_tokens, 150)
        self.assertEqual(t.entry_count, 1)

    def test_near_limit(self):
        t = TokenTracker("TEST")
        t.record("gpt-4o-mini", input_tokens=8000, output_tokens=2000, action="test")
        self.assertTrue(t.is_near_limit(10000))  # 100% >= 80%
        self.assertFalse(t.is_near_limit(100000))  # 10% < 80%

    def test_over_limit(self):
        t = TokenTracker("TEST")
        t.record("gpt-4o-mini", input_tokens=6000, output_tokens=5000, action="test")
        self.assertTrue(t.is_over_limit(10000))  # 110% >= 100%
        self.assertFalse(t.is_over_limit(100000))

    def test_remaining_tokens(self):
        t = TokenTracker("TEST")
        t.record("gpt-4o-mini", input_tokens=200, output_tokens=100, action="x")
        self.assertEqual(t.remaining_tokens(1000), 700)

    def test_get_summary(self):
        t = TokenTracker("TEST")
        t.record("gpt-4o-mini", input_tokens=500, output_tokens=500, action="x")
        s = t.get_summary(10000)
        self.assertEqual(s["total_tokens"], 1000)
        self.assertEqual(s["max_monthly"], 10000)
        self.assertEqual(s["remaining"], 9000)
        self.assertAlmostEqual(s["usage_pct"], 10.0)
        self.assertFalse(s["near_limit"])
        self.assertFalse(s["over_limit"])

    def test_cost_estimation(self):
        cost = TokenTracker._estimate_cost("gpt-4o-mini", 1_000_000, 1_000_000)
        # input: 0.15 + output: 0.60 = 0.75
        self.assertAlmostEqual(cost, 0.75, places=2)

    def test_persistence(self):
        t1 = TokenTracker("TEST")
        t1.record("gpt-4o-mini", input_tokens=100, output_tokens=50)
        # Novo tracker carrega do ficheiro
        t2 = TokenTracker("TEST")
        self.assertEqual(t2.total_tokens, 150)


# ═══════════════════════════════════════════════════════════════════
# Prompt Templates
# ═══════════════════════════════════════════════════════════════════


class TestPromptTemplates(unittest.TestCase):

    def test_optimize_plan_returns_tuple(self):
        sys, usr = prompt_templates.optimize_plan(
            sessions=[{"dia": "seg", "modalidade": "corrida"}],
            athlete={"nome": "Test"},
        )
        self.assertIn("assistente", sys.lower())
        self.assertIn("corrida", usr)

    def test_suggest_workout_edit(self):
        sys, usr = prompt_templates.suggest_workout_edit(
            session={"dia": "ter", "tipo": "força"},
            context="Atleta com lombalgia",
        )
        self.assertIn("força", usr)
        self.assertIn("lombalgia", usr)

    def test_explain_periodization(self):
        sys, usr = prompt_templates.explain_periodization("Base", "natação", 4)
        self.assertIn("Base", usr)
        self.assertIn("natação", usr)

    def test_adjust_for_health(self):
        sys, usr = prompt_templates.adjust_for_health(
            sessions=[],
            condition="Hipertensão",
            athlete={"nome": "Test"},
        )
        self.assertIn("Hipertensão", usr)

    def test_weekly_analysis(self):
        sys, usr = prompt_templates.weekly_analysis(
            sessions=[{"dia": "seg"}],
            week_number=3,
            phase="Específica",
            week_type="carga",
        )
        self.assertIn("3", usr)
        self.assertIn("carga", usr)

    def test_race_strategy(self):
        sys, usr = prompt_templates.race_strategy(
            race_info={"nome": "Maratona SP", "distancia": "42km"},
            athlete={"nome": "Test"},
            recent_sessions=[],
        )
        self.assertIn("Maratona SP", usr)


# ═══════════════════════════════════════════════════════════════════
# Factory
# ═══════════════════════════════════════════════════════════════════


class TestCreateProvider(unittest.TestCase):

    def test_create_openai(self):
        cfg = AIProviderConfig(provider="openai", model="gpt-4o-mini")
        p = create_provider(cfg, "sk-test")
        self.assertEqual(p.__class__.__name__, "OpenAIProvider")

    def test_create_anthropic(self):
        cfg = AIProviderConfig(provider="anthropic", model="claude-sonnet-4-20250514")
        p = create_provider(cfg, "sk-ant-test")
        self.assertEqual(p.__class__.__name__, "AnthropicProvider")

    def test_create_google(self):
        cfg = AIProviderConfig(provider="google", model="gemini-2.0-flash")
        p = create_provider(cfg, "AIzaTest")
        self.assertEqual(p.__class__.__name__, "GoogleProvider")

    def test_create_deepseek(self):
        cfg = AIProviderConfig(provider="deepseek", model="deepseek-chat")
        p = create_provider(cfg, "sk-test")
        self.assertEqual(p.__class__.__name__, "DeepSeekProvider")

    def test_create_custom_uses_openai(self):
        cfg = AIProviderConfig(
            provider="custom",
            model="my-model",
            base_url="http://localhost:11434/v1",
        )
        p = create_provider(cfg, "key")
        self.assertEqual(p.__class__.__name__, "OpenAIProvider")

    def test_create_unknown_raises(self):
        cfg = AIProviderConfig(provider="xyz")
        with self.assertRaises(ValueError):
            create_provider(cfg, "key")


if __name__ == "__main__":
    unittest.main()
