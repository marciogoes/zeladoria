@echo off
echo ========================================
echo   POPULAR CATALOGO COMPLETO DE SERVICOS
echo ========================================
echo.
echo Populando banco de dados com 68 servicos...
echo.

psql -U postgres -d zeladoria -f POPULAR_CATALOGO_COMPLETO.sql

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo   SUCESSO! 68 SERVICOS CADASTRADOS!
    echo ========================================
    echo.
    echo Proximos passos:
    echo 1. Verificar no banco: SELECT COUNT(*^) FROM catalogo_servicos;
    echo 2. Iniciar o backend
    echo 3. Testar o endpoint: http://localhost:8001/api/servicos
    echo.
) else (
    echo ========================================
    echo   ERRO AO POPULAR BANCO!
    echo ========================================
    echo.
    echo Verifique:
    echo 1. PostgreSQL esta rodando?
    echo 2. Banco 'zeladoria' existe?
    echo 3. Usuario 'postgres' tem permissao?
    echo.
)

pause
