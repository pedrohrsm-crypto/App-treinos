@echo off
REM ===============================================
REM App Treinos - Sistema de Planejamento de Treino
REM Execução Rápida para Windows
REM ===============================================

REM Configurar encoding UTF-8
chcp 65001 > nul

REM Definir título da janela
title App Treinos - Sistema de Planejamento Esportivo

REM Limpar tela
cls

REM Banner de inicialização
echo.
echo ===============================================
echo    APP TREINOS - SISTEMA PROFISSIONAL
echo ===============================================
echo.
echo Iniciando sistema...
echo.

REM Verificar se Python está instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.8+ de:
    echo https://www.python.org/downloads/
    echo.
    echo Certifique-se de marcar "Add Python to PATH"
    echo durante a instalacao.
    echo.
    pause
    exit /b 1
)

REM Verificar se o arquivo principal existe
if not exist "training_planner.py" (
    echo [ERRO] Arquivo training_planner.py nao encontrado!
    echo.
    echo Certifique-se de executar este script no diretorio
    echo correto do App Treinos.
    echo.
    pause
    exit /b 1
)

REM Verificar dependências
echo Verificando dependencias...
python -c "import pandas, openpyxl" > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [AVISO] Dependencias nao encontradas.
    echo Instalando pandas e openpyxl...
    echo.
    python -m pip install --user pandas openpyxl
    if %errorlevel% neq 0 (
        echo.
        echo [ERRO] Falha ao instalar dependencias.
        echo Tente executar manualmente:
        echo   pip install pandas openpyxl
        echo.
        pause
        exit /b 1
    )
)

REM Executar o sistema
echo.
echo ===============================================
echo.
python training_planner.py

REM Verificar se houve erro na execução
if %errorlevel% neq 0 (
    echo.
    echo ===============================================
    echo [ERRO] O sistema encontrou um problema.
    echo ===============================================
    echo.
)

REM Manter janela aberta
echo.
echo ===============================================
echo Execucao concluida.
echo ===============================================
echo.
pause
