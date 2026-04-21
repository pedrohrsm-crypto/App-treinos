"""
CLI Manager — Gerencia todos os comandos e modos de execução.

Sistema centralizado para:
- Iniciar a aplicação (dev, prod)
- Rodar testes
- Gerar builds
- Comando auxiliares
"""

import sys
import subprocess
from pathlib import Path
from typing import Optional

from app_treinos.config import AppConfig
from app_treinos.version import __version__


class CLIManager:
    """Gerenciador de interface de linha de comando."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.project_root = Path(__file__).parent.parent

    def run_app(self) -> int:
        """
        Inicia a aplicação em modo normal (Flet UI).

        Returns:
            Exit code (0 = sucesso, 1 = erro)
        """
        try:
            print(f"[INIT] Iniciando App Treinos v{self.config.version}")
            print(f"       Modo: {self.config.environment}")
            print(f"       Debug: {self.config.debug}")
            print()

            # Import aqui para evitar erros de import se Flet não estiver instalado
            from flet_app.main import main as flet_main
            import flet as ft

            # Rodar aplicação Flet
            ft.app(target=flet_main)
            return 0

        except ImportError as e:
            print(f"[ERROR] Erro de dependência: {e}", file=sys.stderr)
            print("   Execute: pip install -e .", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"[ERROR] Erro ao iniciar: {e}", file=sys.stderr)
            if self.config.debug:
                import traceback
                traceback.print_exc()
            return 1

    def run_tests(self, verbose: bool = True, failfast: bool = False) -> int:
        """
        Roda suite de testes com pytest.

        Args:
            verbose: Output verboso
            failfast: Para no primeiro teste que falha

        Returns:
            Exit code do pytest
        """
        try:
            print("[TEST] Rodando testes automatizados...")
            print()

            cmd = ["pytest", "tests/", "-v" if verbose else ""]
            if failfast:
                cmd.append("-x")

            result = subprocess.run(cmd, cwd=self.project_root)
            print()
            if result.returncode == 0:
                print("[OK] Todos os testes passaram!")
            else:
                print("[ERROR] Alguns testes falharam")
            return result.returncode

        except FileNotFoundError:
            print("[ERROR] pytest não encontrado. Execute: pip install pytest", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"[ERROR] Erro ao rodar testes: {e}", file=sys.stderr)
            return 1

    def build_exe(self) -> int:
        """
        Gera executável Windows com PyInstaller.

        Returns:
            Exit code (0 = sucesso)
        """
        try:
            print("🔨 Compilando executável Windows...")
            print()

            # Carregar e executar script de build
            build_script = self.project_root / "scripts" / "build.py"
            if not build_script.exists():
                print(f"[ERROR] Script não encontrado: {build_script}", file=sys.stderr)
                return 1

            result = subprocess.run(
                [sys.executable, str(build_script)],
                cwd=self.project_root
            )

            if result.returncode == 0:
                exe_path = self.project_root / "dist" / "App_Treinos.exe"
                print()
                print(f"[OK] Executável gerado: {exe_path}")
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    print(f"   Tamanho: {size_mb:.1f} MB")
            else:
                print("[ERROR] Erro ao compilar", file=sys.stderr)

            return result.returncode

        except Exception as e:
            print(f"[ERROR] Erro ao gerar build: {e}", file=sys.stderr)
            return 1

    def build_installer(self) -> int:
        """
        Gera instalador Inno Setup.

        Returns:
            Exit code (0 = sucesso)
        """
        try:
            print("📦 Gerando instalador Windows...")
            print()

            installer_script = self.project_root / "scripts" / "installer.iss"
            if not installer_script.exists():
                print(f"[ERROR] Script não encontrado: {installer_script}", file=sys.stderr)
                return 1

            # Tentar executar iscc (Inno Setup compiler)
            result = subprocess.run(
                ["iscc", str(installer_script)],
                cwd=self.project_root
            )

            if result.returncode == 0:
                setup_exe = self.project_root / "Output" / "App_Treinos_Setup.exe"
                print()
                print(f"[OK] Instalador gerado: {setup_exe}")
            else:
                print("[ERROR] Erro ao gerar instalador", file=sys.stderr)
                print("   Certifique-se de ter Inno Setup 6 instalado", file=sys.stderr)

            return result.returncode

        except FileNotFoundError:
            print("[ERROR] iscc não encontrado. Instale Inno Setup 6", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"[ERROR] Erro ao gerar instalador: {e}", file=sys.stderr)
            return 1

    def show_version(self) -> int:
        """Mostra versão da aplicação."""
        print(f"App Treinos v{self.config.version}")
        return 0

    def show_info(self) -> int:
        """Mostra informações da configuração."""
        print(f"App Treinos v{self.config.version}")
        print(f"  Ambiente: {self.config.environment}")
        print(f"  Debug: {self.config.debug}")
        print(f"  Raiz do projeto: {self.config.project_root}")
        print(f"  Banco de dados: {self.config.db_path}")
        print(f"  Banco existe: {self.config.db_exists}")
        print()
        return 0

    def ci_build(self) -> int:
        """Build para CI/CD (validação sem UI)."""
        print("🔍 CI Build: Validando código...")

        # Rodar testes primeiro
        if self.run_tests(verbose=False) != 0:
            return 1

        print("[OK] Validação OK")
        return 0

    def ci_test(self) -> int:
        """Testes para CI/CD."""
        return self.run_tests(verbose=True, failfast=True)
