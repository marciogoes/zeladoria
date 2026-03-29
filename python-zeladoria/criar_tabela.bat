@echo off
cls
echo ========================================
echo   CRIAR TABELA - Teste
echo ========================================
echo.
echo Executando script de migracao...
echo.

python migrations\create_servicos_table.py

echo.
echo ========================================
echo.
pause
