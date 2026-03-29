@echo off
chcp 65001 >nul
echo ============================================================
echo   LISTAR CATEGORIAS DE SERVIÇOS
echo ============================================================
echo.

python manage_catalogo.py categorias

echo.
pause
