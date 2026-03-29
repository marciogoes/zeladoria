@echo off
chcp 65001 > nul
color 0B

cd /d "%~dp0"

if not exist "venv\" (
    echo ERRO: Ambiente virtual nao encontrado!
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python verificar_dados.py
pause
