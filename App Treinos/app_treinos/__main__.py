"""
App Treinos — Ponto de Entrada Centralizado

Uso:
    python -m app_treinos              # Modo produção (normal)
    python -m app_treinos --dev        # Modo desenvolvimento
    python -m app_treinos --test       # Rodar testes
    python -m app_treinos --build      # Gerar executável .exe
    python -m app_treinos --installer  # Gerar instalador
    python -m app_treinos --help       # Ver todas as opções
"""

import sys
import argparse
from app_treinos.config import AppConfig
from app_treinos.cli import CLIManager
from app_treinos.version import __version__


def create_parser() -> argparse.ArgumentParser:
    """Cria parser de argumentos da CLI."""
    parser = argparse.ArgumentParser(
        description="App Treinos — Software para Personal Trainers Profissionais",
        prog="python -m app_treinos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python -m app_treinos              # Rodar aplicação (modo produção)
  python -m app_treinos --dev        # Rodar em desenvolvimento
  python -m app_treinos --test       # Rodar testes
  python -m app_treinos --build      # Gerar executável
  python -m app_treinos --version    # Mostrar versão

Variáveis de ambiente:
  APP_ENV=development                # Modo desenvolvimento
  DB_TYPE=sqlite                     # Tipo banco (sqlite|mysql)
  AI_PROVIDER=openai                 # Provider IA
  AI_API_KEY=sk-...                  # Chave API
        """
    )

    # Modo de execução
    mode_group = parser.add_argument_group("Modo de Execução")
    mode_group.add_argument(
        "--dev",
        action="store_true",
        help="Modo desenvolvimento (hot reload, verbose logs)"
    )
    mode_group.add_argument(
        "--prod",
        action="store_true",
        help="Modo produção (default, otimizado)"
    )

    # Build e testes
    build_group = parser.add_argument_group("Build e Testes")
    build_group.add_argument(
        "--test",
        action="store_true",
        help="Rodar suite de testes (pytest)"
    )
    build_group.add_argument(
        "--build",
        action="store_true",
        help="Gerar executável Windows (.exe)"
    )
    build_group.add_argument(
        "--installer",
        action="store_true",
        help="Gerar instalador Inno Setup"
    )

    # CI/CD
    ci_group = parser.add_argument_group("CI/CD")
    ci_group.add_argument(
        "--ci-build",
        action="store_true",
        help="Build para CI/CD (validação)"
    )
    ci_group.add_argument(
        "--ci-test",
        action="store_true",
        help="Testes para CI/CD"
    )

    # Info
    info_group = parser.add_argument_group("Informação")
    info_group.add_argument(
        "--version",
        action="store_true",
        help="Mostrar versão"
    )
    info_group.add_argument(
        "--info",
        action="store_true",
        help="Mostrar informações de configuração"
    )

    return parser


def main():
    """Função principal — dispatcher de comandos."""
    parser = create_parser()
    args = parser.parse_args()

    # Carregar configuração
    config = AppConfig.load()

    # Definir environment baseado em argumentos
    if args.dev:
        config.environment = "development"
        config.debug = True
    elif args.prod:
        config.environment = "production"
        config.debug = False

    # Criar CLI manager
    cli = CLIManager(config)

    # Dispatch dos comandos
    if args.version:
        return cli.show_version()
    elif args.info:
        return cli.show_info()
    elif args.test:
        return cli.run_tests()
    elif args.build:
        return cli.build_exe()
    elif args.installer:
        return cli.build_installer()
    elif args.ci_build:
        return cli.ci_build()
    elif args.ci_test:
        return cli.ci_test()
    else:
        # Default: rodar aplicação
        return cli.run_app()


if __name__ == "__main__":
    sys.exit(main())
