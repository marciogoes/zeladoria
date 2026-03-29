@echo off
chcp 65001 > nul
color 0D

echo.
echo ======================================================================
echo   TESTE DIRETO DA API - VERIFICAR DASHBOARD
echo ======================================================================
echo.
echo Este script vai:
echo   1. Fazer login com seurb@zeladoria.com
echo   2. Tentar acessar o dashboard
echo   3. Mostrar exatamente qual erro esta acontecendo
echo.
echo IMPORTANTE: A API deve estar rodando na porta 8001!
echo.
pause

cd /d "%~dp0"

if not exist "venv\" (
    echo ERRO: Ambiente virtual nao encontrado!
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python testar_api_dashboard.py
pause
