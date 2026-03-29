@echo off
chcp 65001 > nul
color 0A

echo.
echo ================================================
echo   POPULAR CATEGORIAS E BAIRROS
echo ================================================
echo.

cd /d "%~dp0"

if not exist "venv\" (
    echo ERRO: Ambiente virtual nao encontrado!
    echo.
    echo Execute primeiro: INSTALAR.bat
    pause
    exit /b 1
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Populando categorias e bairros...
python popular_categorias_bairros.py

if errorlevel 1 (
    echo.
    echo ERRO ao popular dados
    pause
    exit /b 1
)

echo.
echo ================================================
echo   DADOS POPULADOS COM SUCESSO!
echo ================================================
echo.
echo Agora voce pode:
echo   1. Iniciar a API: INICIAR_API_8000.bat
echo   2. Acessar o sistema: http://localhost:8000/app
echo.
pause
