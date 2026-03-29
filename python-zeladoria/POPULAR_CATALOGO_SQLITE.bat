@echo off
echo ========================================
echo   POPULAR CATALOGO - SQLITE
echo ========================================
echo.
echo Populando banco SQLite com 68 servicos...
echo.

python popular_catalogo_sqlite.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCESSO!
    echo ========================================
    echo.
    echo Proximos passos:
    echo 1. Iniciar o backend: INICIAR_BACKEND.bat
    echo 2. Testar endpoint: http://localhost:8001/api/catalogo
    echo 3. Ver documentacao: http://localhost:8001/docs
    echo.
) else (
    echo.
    echo ========================================
    echo   ERRO!
    echo ========================================
    echo.
    echo Verifique se:
    echo 1. Python esta instalado
    echo 2. Arquivo zeladoria.db existe
    echo.
)

pause
