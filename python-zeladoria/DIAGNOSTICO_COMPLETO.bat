@echo off
chcp 65001 > nul
color 0E

cd /d "%~dp0"

if not exist "venv\" (
    echo ERRO: Ambiente virtual nao encontrado!
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python diagnostico_completo.py
pause
