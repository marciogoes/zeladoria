@echo off
title Zelô — Zeladoria Urbana de Belém v4.0.0
chcp 65001 >nul

echo.
echo  ████████╗███████╗██╗      ██████╗
echo     ██╔══╝██╔════╝██║     ██╔═══██╗
echo     ██║   █████╗  ██║     ██║   ██║
echo     ██║   ██╔══╝  ██║     ██║   ██║
echo     ██║   ███████╗███████╗╚██████╔╝
echo     ╚═╝   ╚══════╝╚══════╝ ╚═════╝
echo.
echo  Zeladoria Urbana de Belém/PA — v4.0.0
echo  Preparado para a COP 30
echo ══════════════════════════════════════════

cd /d "%~dp0python-zeladoria"

:: Verifica venv
if not exist "venv\Scripts\activate.bat" (
    echo [1/3] Criando ambiente virtual...
    python -m venv venv
    echo [2/3] Instalando dependencias...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt --quiet
) else (
    echo [1/3] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

:: Seed se banco não existir
if not exist "zeladoria.db" (
    echo [2/3] Populando banco de dados inicial...
    set POPULATE_DATA=true
    python seed.py
)

echo [3/3] Iniciando servidor Zelô...
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║  Sistema:  http://localhost:8001/app     ║
echo  ║  Landing:  http://localhost:8001/landing ║
echo  ║  Painel TV: http://localhost:8001/tv     ║
echo  ║  API Docs: http://localhost:8001/docs    ║
echo  ╠══════════════════════════════════════════╣
echo  ║  Logins (senha: senha123)                ║
echo  ║  Admin:    admin@belem.pa.gov.br         ║
echo  ║  Gestor:   maria.santos@belem.pa.gov.br  ║
echo  ║  Cidadão:  pedro.almeida@email.com       ║
echo  ╚══════════════════════════════════════════╝
echo.

uvicorn main:app --host 0.0.0.0 --port 8001 --reload

pause
