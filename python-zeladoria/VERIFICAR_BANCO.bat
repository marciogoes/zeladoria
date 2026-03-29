@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🔍 VERIFICANDO BANCO DE DADOS                        ║
echo ║   Sistema de Zeladoria Urbana                          ║
echo ╚════════════════════════════════════════════════════════╝
echo.

call venv\Scripts\activate
python verificar_banco.py

pause
