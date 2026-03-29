@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🔍 DIAGNÓSTICO DE ROTAS                              ║
echo ║   Sistema de Zeladoria Urbana                          ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo [INFO] Testando se o backend está acessível...
echo.

call venv\Scripts\activate
python testar_rotas.py

pause
