"""
App Treinos — Suíte Unificada de Testes (pytest)
==================================================

Consolida os testes dispersos em scripts/ numa única suíte.
Executar: pytest tests/ -v
"""

import sys
import os
import math
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta

import pytest

# Garantir que o diretório do projeto está no path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from training_planner import (
    calcular_semanas_ate_prova,
    HealthIssue,
    TrainerInfo,
    Athlete,
    HealthAdvisor,
    PeriodizationPlanner,
    TrainingZones,
    TrainingPlanGenerator,
    ExcelExporter,
)
from core.database import DatabaseManager


# ═══════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════

@pytest.fixture
def trainer_valido():
    """Treinador com dados válidos."""
    return TrainerInfo(
        nome_completo="Dr. João Silva Santos",
        cpf="12345678909",
        cref="123456-G/SP",
    )


@pytest.fixture
def atleta_corrida(trainer_valido):
    """Atleta de corrida básico para testes."""
    return Athlete(
        nome="Maria Silva",
        idade=30,
        peso=65.0,
        altura=170,
        genero="Feminino",
        esporte="Corrida",
        distancia_prova="10K",
        limiar_lactato=165,
        vo2_max=48.0,
        dias_semana=4,
        semanas_ate_prova=12,
        trainer=trainer_valido,
    )


@pytest.fixture
def atleta_triathlon(trainer_valido):
    """Atleta de triathlon para testes."""
    return Athlete(
        nome="Carlos Mendes",
        idade=35,
        peso=75.0,
        altura=180,
        genero="Masculino",
        esporte="Triathlon",
        distancia_prova="Olímpico",
        limiar_lactato=170,
        vo2_max=55.0,
        dias_semana=5,
        semanas_ate_prova=16,
        trainer=trainer_valido,
    )


@pytest.fixture
def export_dir(tmp_path):
    """Diretório temporário para exportações."""
    d = tmp_path / "exports"
    d.mkdir()
    return d


@pytest.fixture
def db_temp(tmp_path):
    """Banco de dados temporário para testes de autenticação."""
    db_path = str(tmp_path / "test_app_treinos.db")
    return DatabaseManager(db_path=db_path)


# ═══════════════════════════════════════════════════════════════════
# 1. Validação de CPF
# ═══════════════════════════════════════════════════════════════════

class TestValidacaoCPF:
    """Testes de validação do CPF (algoritmo oficial)."""

    def test_cpf_valido(self):
        assert TrainerInfo._validar_cpf("12345678909") is True

    def test_cpf_invalido_digito_verificador(self):
        assert TrainerInfo._validar_cpf("12345678900") is False

    def test_cpf_digitos_iguais(self):
        for d in "0123456789":
            assert TrainerInfo._validar_cpf(d * 11) is False

    def test_cpf_curto(self):
        assert TrainerInfo._validar_cpf("123456") is False

    def test_cpf_com_formatacao(self):
        # A validação aceita apenas dígitos; o chamador normaliza
        assert TrainerInfo._validar_cpf("12345678909") is True


# ═══════════════════════════════════════════════════════════════════
# 2. Validação de CREF
# ═══════════════════════════════════════════════════════════════════

class TestValidacaoCREF:
    """Testes de validação do CREF."""

    @pytest.mark.parametrize("cref", [
        "123456-G/SP",
        "CREF1 123456-G/RJ",
        "098765-G/MG",
        "CREF 1234-G/BA",
    ])
    def test_cref_valido(self, cref):
        assert TrainerInfo._validar_cref(cref) is True

    @pytest.mark.parametrize("cref", [
        "ABC-123",
        "123",
        "",
        "CREF-INVALIDO",
    ])
    def test_cref_invalido(self, cref):
        assert TrainerInfo._validar_cref(cref) is False


# ═══════════════════════════════════════════════════════════════════
# 3. TrainerInfo (criação e formatação)
# ═══════════════════════════════════════════════════════════════════

class TestTrainerInfo:
    """Testes de criação e formatação do TrainerInfo."""

    def test_criar_com_dados_validos(self, trainer_valido):
        assert trainer_valido.nome_completo == "Dr. João Silva Santos"
        assert trainer_valido.cpf == "12345678909"

    def test_rejeitar_cpf_invalido(self):
        with pytest.raises(ValueError, match="CPF"):
            TrainerInfo("Dr. Maria Silva", cpf="12345678900", cref="123456-G/SP")

    def test_rejeitar_cref_invalido(self):
        with pytest.raises(ValueError, match="CREF"):
            TrainerInfo("Dr. Pedro Santos", cpf="12345678909", cref="ABC123")

    def test_rejeitar_nome_curto(self):
        with pytest.raises(ValueError, match="Nome"):
            TrainerInfo("João", cpf="12345678909", cref="123456-G/SP")

    def test_formatar_cpf(self, trainer_valido):
        assert trainer_valido.formatar_cpf() == "123.456.789-09"

    def test_formatar_cref(self, trainer_valido):
        assert trainer_valido.formatar_cref() == "123456-G/SP"


# ═══════════════════════════════════════════════════════════════════
# 4. Cálculo de semanas até a prova
# ═══════════════════════════════════════════════════════════════════

class TestCalculoSemanas:
    """Testes de calcular_semanas_ate_prova()."""

    def test_12_semanas(self):
        data = (datetime.now() + timedelta(days=84)).strftime("%d/%m/%Y")
        assert calcular_semanas_ate_prova(data) == 12

    def test_40_semanas(self):
        data = (datetime.now() + timedelta(days=280)).strftime("%d/%m/%Y")
        assert calcular_semanas_ate_prova(data) == 40

    def test_arredonda_para_cima(self):
        data = (datetime.now() + timedelta(days=5)).strftime("%d/%m/%Y")
        assert calcular_semanas_ate_prova(data) == 1

    def test_hoje_retorna_minimo_1(self):
        data = datetime.now().strftime("%d/%m/%Y")
        assert calcular_semanas_ate_prova(data) >= 1

    def test_data_passado_levanta_erro(self):
        with pytest.raises(ValueError):
            calcular_semanas_ate_prova("01/01/2020")

    def test_formato_invalido_levanta_erro(self):
        with pytest.raises(ValueError, match="Formato"):
            calcular_semanas_ate_prova("2026-03-20")


# ═══════════════════════════════════════════════════════════════════
# 5. Validação de senha
# ═══════════════════════════════════════════════════════════════════

class TestValidacaoSenha:
    """Testes de validação de senha (regras: 6-12 caracteres, sem espaços)."""

    @staticmethod
    def _senha_valida(senha: str) -> bool:
        return 6 <= len(senha) <= 12 and " " not in senha and len(senha) > 0

    @pytest.mark.parametrize("senha", [
        "abc123",        # 6 chars
        "Abc@123",       # 7 chars com especial
        "SenhaForte1!",  # 12 chars
        "SENHA123",      # maiúsculas
        "senha123",      # minúsculas
        "12345678",      # só números
        "!@#$%^&*",      # só especiais
    ])
    def test_senhas_validas(self, senha):
        assert self._senha_valida(senha) is True

    @pytest.mark.parametrize("senha,motivo", [
        ("abc12", "muito curta"),
        ("SenhaForte123", "muito longa"),
        ("senha com espaco", "espaços"),
        ("Sen ha1", "espaço no meio"),
        ("", "vazia"),
        ("     ", "só espaços"),
    ])
    def test_senhas_invalidas(self, senha, motivo):
        assert self._senha_valida(senha) is False, f"Deveria rejeitar: {motivo}"


# ═══════════════════════════════════════════════════════════════════
# 6. Athlete (criação e IMC)
# ═══════════════════════════════════════════════════════════════════

class TestAthlete:
    """Testes de criação do Athlete e cálculo de IMC."""

    def test_imc_calculado(self, atleta_corrida):
        # IMC = 65 / (1.70)^2 ≈ 22.5
        assert abs(atleta_corrida.imc - 22.5) < 0.1

    def test_dados_basicos(self, atleta_corrida):
        assert atleta_corrida.nome == "Maria Silva"
        assert atleta_corrida.esporte == "Corrida"
        assert atleta_corrida.semanas_ate_prova == 12


# ═══════════════════════════════════════════════════════════════════
# 7. Geração de plano de treinamento
# ═══════════════════════════════════════════════════════════════════

class TestGeracaoPlano:
    """Testes de geração de planos de treinamento."""

    def test_gerar_plano_corrida(self, atleta_corrida):
        gen = TrainingPlanGenerator(atleta_corrida)
        plano = gen.get_weekly_training(1)
        assert len(plano) > 0
        assert all("dia" in t for t in plano)

    def test_gerar_plano_completo(self, atleta_corrida):
        gen = TrainingPlanGenerator(atleta_corrida)
        plano = gen.get_full_training_plan()
        assert len(plano) > 0

    def test_gerar_plano_triathlon(self, atleta_triathlon):
        gen = TrainingPlanGenerator(atleta_triathlon)
        plano = gen.get_weekly_training(1)
        assert len(plano) > 0

    def test_periodizacao_tem_fases(self, atleta_corrida):
        gen = TrainingPlanGenerator(atleta_corrida)
        dist = gen.periodization.calcular_distribuicao_fases()
        assert len(dist) > 0
        assert all("fase" in b for b in dist)


# ═══════════════════════════════════════════════════════════════════
# 8. HealthAdvisor
# ═══════════════════════════════════════════════════════════════════

class TestHealthAdvisor:
    """Testes do sistema de saúde com IA."""

    def test_analise_problema_ortopedico(self):
        advisor = HealthAdvisor()
        problema = HealthIssue(
            tipo="ortopédico",
            descricao="Tendinite patelar",
            membro_afetado="joelho_direito",
            gravidade="moderado",
        )
        analise = advisor.analyze_health_issues([problema], "Corrida")
        assert "recomendacoes" in analise
        assert len(analise["recomendacoes"]) > 0

    def test_analise_sem_problemas(self):
        advisor = HealthAdvisor()
        analise = advisor.analyze_health_issues([], "Corrida")
        assert "recomendacoes" in analise


# ═══════════════════════════════════════════════════════════════════
# 9. Exportação Excel
# ═══════════════════════════════════════════════════════════════════

class TestExportacaoExcel:
    """Testes de exportação para Excel."""

    def test_exportar_plano_semanal(self, atleta_corrida, export_dir):
        gen = TrainingPlanGenerator(atleta_corrida)
        plano = gen.get_weekly_training(1)
        exporter = ExcelExporter(atleta_corrida, plano, is_full_plan=False, output_dir=str(export_dir))
        filepath = exporter.export_to_excel("teste_semanal.xlsx")
        assert Path(filepath).exists()
        assert Path(filepath).stat().st_size > 0

    def test_exportar_plano_completo(self, atleta_corrida, export_dir):
        gen = TrainingPlanGenerator(atleta_corrida)
        plano = gen.get_full_training_plan()
        exporter = ExcelExporter(atleta_corrida, plano, is_full_plan=True, output_dir=str(export_dir))
        filepath = exporter.export_to_excel("teste_completo.xlsx")
        assert Path(filepath).exists()
        assert Path(filepath).stat().st_size > 0


# ═══════════════════════════════════════════════════════════════════
# 10. Exportação PDF
# ═══════════════════════════════════════════════════════════════════

class TestExportacaoPDF:
    """Testes de exportação para PDF."""

    def test_exportar_pdf(self, atleta_corrida, export_dir):
        gen = TrainingPlanGenerator(atleta_corrida)
        plano = gen.get_weekly_training(1)

        from pdf_exporter import PDFExporter

        pdf_exp = PDFExporter(atleta_corrida, plano, is_full_plan=False, output_dir=str(export_dir))
        filepath = pdf_exp.export_to_pdf("teste.pdf")
        assert Path(filepath).exists()
        assert Path(filepath).stat().st_size > 0


# ═══════════════════════════════════════════════════════════════════
# 11. Autenticação (banco temporário)
# ═══════════════════════════════════════════════════════════════════

class TestAutenticacao:
    """Testes do sistema de autenticação."""

    def test_cadastrar_usuario(self, db_temp):
        sucesso, msg = db_temp.cadastrar_usuario(
            cpf="12345678901",
            cref="123456-G/SP",
            nome="João Silva",
            senha="senha123",
            email="joao@teste.com",
        )
        assert sucesso, msg

    def test_login_correto(self, db_temp):
        db_temp.cadastrar_usuario("12345678901", "123456-G/SP", "João Silva", "senha123", "")
        sucesso, usuario = db_temp.autenticar_usuario("12345678901", "senha123")
        assert sucesso
        assert usuario["nome"] == "João Silva"

    def test_login_senha_errada(self, db_temp):
        db_temp.cadastrar_usuario("12345678901", "123456-G/SP", "João Silva", "senha123", "")
        sucesso, _ = db_temp.autenticar_usuario("12345678901", "senhaerrada")
        assert not sucesso

    def test_login_por_cref(self, db_temp):
        db_temp.cadastrar_usuario("12345678901", "123456-G/SP", "João Silva", "senha123", "")
        sucesso, usuario = db_temp.autenticar_usuario("123456-G/SP", "senha123")
        assert sucesso

    def test_cpf_duplicado(self, db_temp):
        db_temp.cadastrar_usuario("12345678901", "123456-G/SP", "João Silva", "senha123", "")
        sucesso, msg = db_temp.cadastrar_usuario("12345678901", "654321-G/RJ", "Maria", "abc123", "")
        assert not sucesso


# ═══════════════════════════════════════════════════════════════════
# 12. TrainingManager (isolamento por profissional)
# ═══════════════════════════════════════════════════════════════════

class TestTrainingManager:
    """Testes de isolamento de dados por profissional."""

    def test_criar_diretorio_por_cref(self, tmp_path, trainer_valido, atleta_corrida):
        from training_manager import TrainingManager

        manager = TrainingManager(base_dir=str(tmp_path / "trainers"))

        record = manager.register_training(
            trainer_info=trainer_valido,
            athlete=atleta_corrida,
        )

        # Verificar que o diretório do treinador foi criado
        trainer_id = "".join(filter(str.isalnum, trainer_valido.cref))
        trainer_dir = tmp_path / "trainers" / trainer_id
        assert trainer_dir.exists()

    def test_rejeitar_trainer_none(self, tmp_path):
        from training_manager import TrainingManager

        manager = TrainingManager(base_dir=str(tmp_path / "trainers"))
        with pytest.raises(ValueError, match="trainer_info não pode ser None"):
            manager._get_trainer_id(None)

    def test_rejeitar_cref_vazio(self, tmp_path):
        from training_manager import TrainingManager

        manager = TrainingManager(base_dir=str(tmp_path / "trainers"))
        with pytest.raises(ValueError, match="CREF do treinador não pode ser vazio"):
            manager._get_trainer_id({"cref": ""})


# ═══════════════════════════════════════════════════════════════════
# 13. Estrutura do projeto
# ═══════════════════════════════════════════════════════════════════

class TestEstruturaProjeto:
    """Testes de integridade da estrutura de diretórios."""

    @pytest.mark.parametrize("subdir", [
        "gui", "core", "data", "docs", "scripts", "linux", "macos",
    ])
    def test_diretorio_existe(self, subdir):
        assert (PROJECT_ROOT / subdir).is_dir()

    @pytest.mark.parametrize("arquivo", [
        "App_Treinos_GUI.py",
        "training_planner.py",
        "training_manager.py",
        "pdf_exporter.py",
        "requirements.txt",
    ])
    def test_arquivo_raiz_existe(self, arquivo):
        assert (PROJECT_ROOT / arquivo).is_file()

    def test_gui_init_exporta_classes(self):
        from gui import AppTreinosGUI, AccessibleTheme
        assert AppTreinosGUI is not None
        assert AccessibleTheme is not None

    def test_core_init_exporta_classes(self):
        from core import Athlete, TrainerInfo, TrainingPlanGenerator
        assert Athlete is not None


# ═══════════════════════════════════════════════════════════════════
# 14. Dependências
# ═══════════════════════════════════════════════════════════════════

class TestDependencias:
    """Testes de dependências instaladas."""

    @pytest.mark.parametrize("modulo", ["pandas", "openpyxl", "reportlab"])
    def test_dependencia_instalada(self, modulo):
        __import__(modulo)
