@echo off
REM ===========================================================
REM App Treinos v3.0 — Launcher Windows
REM ===========================================================
REM Duplo clique neste arquivo para iniciar o App Treinos.
REM ===========================================================

chcp 65001 > nul
title App Treinos v3.0

cd /d "%~dp0"

REM ── Verificar Python ──────────────────────────────────────
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  [ERRO] Python nao encontrado!
    echo.
    echo  Instale Python 3.10+ de: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM ── Verificar dependências ────────────────────────────────
python -c "import flet, pandas, openpyxl, reportlab" > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  Instalando dependencias...
    python -m pip install --user -r requirements.txt
    echo.
)

REM ── Executar App Treinos (Flet) ───────────────────────────
echo.
echo  Iniciando App Treinos v3.0...
echo.
python App_Treinos_Flet.py

if %errorlevel% neq 0 (
    echo.
    echo  Ocorreu um erro na execucao.
    echo  Verifique se todas as dependencias estao instaladas:
    echo    pip install -r requirements.txt
    echo.
    pause
)
