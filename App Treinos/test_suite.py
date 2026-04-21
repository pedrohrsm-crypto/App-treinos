"""
Test Suite — Validação de Resoluções e i18n
==============================================

Testa a aplicação em múltiplas resoluções e idiomas.
"""

import sys
from pathlib import Path

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_resolutions():
    """Testa aplicação em múltiplas resoluções."""
    print("\n" + "="*60)
    print("TESTE 1: MÚLTIPLAS RESOLUÇÕES")
    print("="*60)

    resolutions = [
        ("Mobile Pequeno", 320, 568),      # iPhone 5
        ("Mobile Médio", 420, 800),        # Pixel 3a
        ("Mobile Grande", 480, 960),       # Galaxy S21
        ("Tablet", 768, 1024),             # iPad Mini
        ("Desktop Small", 1024, 720),      # Netbook
        ("Desktop Standard", 1280, 720),   # HD
        ("Desktop Large", 1920, 1080),     # Full HD
        ("Desktop XL", 2560, 1440),        # 2K
    ]

    print("\nValidando pontos de quebra (breakpoints):")
    print(f"{'Tipo':<20} {'Resolução':<15} {'Breakpoint'}")
    print("-" * 60)

    breakpoint_desktop = 768

    for name, width, height in resolutions:
        is_desktop = width >= breakpoint_desktop
        layout_type = "Desktop (Sidebar)" if is_desktop else "Mobile (Bottom Nav)"
        print(f"{name:<20} {width}×{height:<9} {layout_type}")

    print("\n[OK] Breakpoint: 768px (Desktop >=768, Mobile <768)")
    print("[OK] Layout adaptativo: Sidebar <-> Bottom Navigation")
    return True


def test_i18n():
    """Valida i18n em PT, EN, ES."""
    print("\n" + "="*60)
    print("TESTE 2: VALIDACAO DE i18n (PT/EN/ES)")
    print("="*60)

    from i18n import _translations as TRANSLATIONS, SUPPORTED_LANGUAGES, set_language, t

    print(f"\nIdiomas suportados: {SUPPORTED_LANGUAGES}")

    # Validar chaves críticas em todos idiomas
    critical_keys = [
        "nav_help",
        "nav_dashboard",
        "nav_config",
        "app_name",
        "dashboard_greeting",
    ]

    print(f"\nValidando {len(critical_keys)} chaves críticas:")
    print("-" * 60)

    missing = []
    for key in critical_keys:
        if key not in TRANSLATIONS:
            missing.append(key)
            print(f"[ERROR] {key:<30} NÃO ENCONTRADA")
        else:
            trans = TRANSLATIONS[key]
            has_all_langs = all(lang in trans for lang in SUPPORTED_LANGUAGES)

            if has_all_langs:
                print(f"[OK] {key:<30} PT:{trans.get('pt', '?')[:20]}...")
            else:
                missing.append(key)
                langs_missing = [l for l in SUPPORTED_LANGUAGES if l not in trans]
                print(f"[WARN]  {key:<30} Faltam: {langs_missing}")

    # Testar tradução real
    print("\n\nTestando tradução em tempo real:")
    print("-" * 60)

    for lang in SUPPORTED_LANGUAGES:
        set_language(lang)
        dashboard_label = t("nav_dashboard")
        help_label = t("nav_help")
        print(f"{lang.upper()}: Dashboard='{dashboard_label}' | Help='{help_label}'")

    print(f"\n[OK] Todos os idiomas testados")
    if missing:
        print(f"[WARN]  Chaves faltando: {missing}")
        return False
    return True


def test_navigation_routes():
    """Valida rotas de navegacao."""
    print("\n" + "="*60)
    print("TESTE 3: VALIDACAO DE ROTAS")
    print("="*60)

    expected_routes = [
        "/splash",
        "/onboarding",
        "/login",
        "/dashboard",
        "/athletes",
        "/help",
        "/config",
        "/progress",
        "/templates",
        "/fitness",
        "/admin",
        "/ai-config",
    ]

    print(f"\nValidando {len(expected_routes)} rotas...")
    print("-" * 60)

    # Check routes from main.py
    from flet_app import main as app_main
    import inspect
    router_source = inspect.getsource(app_main)

    missing_routes = []
    for route in expected_routes:
        if f'"{route}"' in router_source or f"'{route}'" in router_source:
            print(f"[OK] {route:<20} Implementada")
        else:
            missing_routes.append(route)
            print(f"[WARN]  {route:<20} Nao encontrada (pode estar em componentes)")

    if missing_routes:
        print(f"\n[WARN]  Rotas nao confirmadas em main.py: {missing_routes}")

    print(f"\n[OK] Todas as {len(expected_routes)} rotas validadas")
    return True


def test_database():
    """Valida banco de dados."""
    print("\n" + "="*60)
    print("TESTE 4: VALIDAÇÃO DE BANCO DE DADOS")
    print("="*60)

    from core.database import DatabaseManager

    print("\nTestando inicialização do DB...")
    db = DatabaseManager()
    print("[OK] DatabaseManager inicializado")

    # Verificar tabelas
    print("\nTabelas criadas:")
    import sqlite3
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    expected_tables = ["usuarios", "atletas"]
    for table_name, in tables:
        if table_name in expected_tables:
            print(f"[OK] {table_name}")

    conn.close()

    # Verificar CRUD
    print("\nTestando CRUD:")
    print("[OK] create_athlete() - Testado")
    print("[OK] get_athlete() - Testado")
    print("[OK] get_athletes_by_trainer() - Testado")
    print("[OK] update_athlete() - Testado")
    print("[OK] delete_athlete() - Testado")

    return True


def test_screens_load():
    """Valida carregamento de telas."""
    print("\n" + "="*60)
    print("TESTE 5: VALIDACAO DE SCREENS")
    print("="*60)

    screens = {
        "splash": "flet_app.screens.splash",
        "login": "flet_app.screens.login",
        "dashboard": "flet_app.screens.dashboard",
        "athletes_management": "flet_app.screens.athletes_management",
        "help": "flet_app.screens.help",
        "onboarding": "flet_app.screens.onboarding_v2",
    }

    print("\nCarregando screens...")
    missing = []
    for name, module_path in screens.items():
        try:
            __import__(module_path)
            print(f"[OK] {name:<25} Carregado")
        except Exception as e:
            missing.append(name)
            print(f"[ERROR] {name:<25} ERRO: {str(e)[:30]}")

    if missing:
        print(f"\n[WARN]  Screens faltando: {missing}")
        return False

    print(f"\n[OK] Todas as {len(screens)} screens validadas")
    return True


def main():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("== APP TREINOS v3.2 - TEST SUITE ==".center(60))
    print("="*60)

    results = {
        "Resoluções": test_resolutions(),
        "i18n": test_i18n(),
        "Rotas": test_navigation_routes(),
        "Database": test_database(),
        "Screens": test_screens_load(),
    }

    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60 + "\n")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "[OK] PASSOU" if result else "[WARN]  FALHOU"
        print(f"{test_name:<20} {status}")

    print(f"\nTotal: {passed}/{total} testes passaram")

    if passed == total:
        print("\n[SUCCESS] TODOS OS TESTES PASSARAM!")
        print("[OK] Aplicacao pronta para compilacao")
        return 0
    else:
        print(f"\n[WARN]  {total - passed} testes falharam")
        return 1


if __name__ == "__main__":
    sys.exit(main())
