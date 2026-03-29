@echo off
title Recriar e Iniciar - Zeladoria Belem
color 0A
cls

echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║                                                      ║
echo   ║      RECRIAR BANCO E INICIAR API AUTOMATICAMENTE     ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
echo   Pressione qualquer tecla para comecar...
pause >nul

:: Executar recriacao do banco
call RECRIAR_BANCO.bat

if %errorlevel% neq 0 (
    echo.
    echo   ERRO ao recriar banco!
    pause
    exit
)

cls
echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║                                                      ║
echo   ║           INICIANDO API EM 3 SEGUNDOS...             ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
timeout /t 3 >nul

cls
echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║                  API RODANDO                         ║
echo   ╠══════════════════════════════════════════════════════╣
echo   ║                                                      ║
echo   ║  Frontend:  http://localhost:8001/app                ║
echo   ║  API Docs:  http://localhost:8001/docs               ║
echo   ║  Health:    http://localhost:8001/health             ║
echo   ║                                                      ║
echo   ║  Login: admin@zeladoria.com / admin123               ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
echo   Pressione CTRL+C para parar a API
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
