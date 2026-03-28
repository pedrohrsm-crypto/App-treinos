#!/usr/bin/env bash
# ===========================================================
# App Treinos v3.0 — Launcher Linux / macOS
# ===========================================================
# Duplo clique ou execute:  ./AppTreinos.sh
# ===========================================================

set -e
cd "$(dirname "$0")"

# ── Verificar Python ────────────────────────────────────────
PYTHON=""
for candidate in python3 python; do
    if command -v "$candidate" &>/dev/null; then
        PYTHON="$candidate"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo ""
    echo "  [ERRO] Python não encontrado!"
    echo ""
    echo "  Instale Python 3.10+:"
    echo "    • Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "    • macOS:         brew install python"
    echo ""
    exit 1
fi

echo "  Usando: $($PYTHON --version)"

# ── Verificar dependências ──────────────────────────────────
if ! $PYTHON -c "import flet, pandas, openpyxl, reportlab" 2>/dev/null; then
    echo ""
    echo "  Instalando dependências..."
    $PYTHON -m pip install --user -r requirements.txt
    echo ""
fi

# ── Executar App Treinos (Flet) ─────────────────────────────
echo ""
echo "  Iniciando App Treinos v3.0..."
echo ""
$PYTHON App_Treinos_Flet.py
