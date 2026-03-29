@echo off
chcp 65001 >nul
echo ============================================================
echo   ESTATÍSTICAS DO CATÁLOGO
echo ============================================================
echo.

python manage_catalogo.py stats

echo.
pause
