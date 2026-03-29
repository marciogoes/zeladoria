@echo off
chcp 65001 >nul
cls
echo ========================================
echo   LISTAR SERVIÇOS DO CATÁLOGO
echo ========================================
echo.

python manage_catalogo.py listar

echo.
echo ========================================
echo.

pause
