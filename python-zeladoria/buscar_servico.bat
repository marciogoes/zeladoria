@echo off
chcp 65001 >nul
cls
echo ========================================
echo   BUSCAR SERVIÇOS
echo ========================================
echo.

set /p termo="Digite o termo de busca: "

echo.
echo Buscando por: %termo%
echo.

python manage_catalogo.py buscar "%termo%"

echo.
echo ========================================
echo.

pause
