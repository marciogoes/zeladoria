@echo off
chcp 65001 >nul
echo ============================================================
echo   BUSCAR SERVIÇOS
echo ============================================================
echo.

set /p TERMO="Digite o termo de busca: "

if "%TERMO%"=="" (
    echo ❌ Termo de busca não pode ser vazio!
    pause
    exit /b 1
)

echo.
echo Buscando por: %TERMO%
echo.

python manage_catalogo.py buscar "%TERMO%"

echo.
pause
