@echo off
chcp 65001 >nul
cls
echo ========================================
echo   ESTATÍSTICAS DO CATÁLOGO
echo ========================================
echo.

python manage_catalogo.py stats

echo.
echo ========================================
echo.

pause
