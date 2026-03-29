@echo off
chcp 65001 >nul
cls
echo ========================================
echo   CRIAR TABELA - Simples
echo ========================================
echo.

echo Criando tabela servicos_secretaria...
echo.

python migrations\create_servicos_table.py

echo.
pause
