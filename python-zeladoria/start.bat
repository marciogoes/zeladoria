@echo off
title START - Zeladoria Belem
color 0B
cls

echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║                                                      ║
echo   ║    🏛️  SISTEMA DE ZELADORIA URBANA - BELEM/PA        ║
echo   ║                                                      ║
echo   ║              INICIALIZACAO COMPLETA                  ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
echo.
echo   Este script vai:
echo.
echo   ✓ Fechar API antiga
echo   ✓ Recriar banco de dados
echo   ✓ Popular com dados de teste
echo   ✓ Iniciar API
echo   ✓ Abrir navegador
echo.
echo.
echo   Pressione qualquer tecla para comecar...
pause >nul

:: Recriar e iniciar
call RECRIAR_E_INICIAR.bat
