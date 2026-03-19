@echo off
REM ===============================================
REM App Treinos GUI - Launcher para Windows
REM ===============================================

chcp 65001 > nul
title App Treinos - Interface Gráfica

REM Verificar Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não encontrado!
    echo.
    echo Instale Python 3.8+ de: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verificar dependências
python -c "import pandas, openpyxl" > nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependências...
    python -m pip install --user pandas openpyxl
)

REM Executar GUI
python App_Treinos_GUI.py

if %errorlevel% neq 0 (
    echo.
    echo Houve um erro na execução.
    pause
)
