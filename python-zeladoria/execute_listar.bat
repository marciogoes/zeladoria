@echo off
chcp 65001 >nul
echo ============================================================
echo   LISTAR SERVIÇOS DO CATÁLOGO
echo ============================================================
echo.

python manage_catalogo.py listar

echo.
pause
