@echo off
chcp 65001 > nul
color 0A

echo.
echo ========================================================================
echo   POPULAR CATALOGO DE SERVICOS
echo ========================================================================
echo.
echo Este script vai criar 100+ servicos organizados por secretaria
echo com SLA (prazo de atendimento) definido para cada um!
echo.
echo Servicos incluem:
echo   - SEURB: Iluminacao, Pavimentacao, Sinalizacao, Pracas
echo   - SESAN: Limpeza, Coleta, Drenagem
echo   - SEMOB: Transporte, Semaforos, Ciclovias
echo   - SEMMA: Arborizacao, Animais, Licenciamento
echo   - SESMA: Vigilancia Sanitaria, Vetores, Zoonoses
echo.
pause

cd /d "%~dp0"

if not exist "venv\" (
    echo ERRO: Ambiente virtual nao encontrado!
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo.
echo Populando catalogo de servicos...
python -m app.seeds.seed_servicos

if errorlevel 1 (
    echo.
    echo ERRO ao popular servicos
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo   CATALOGO DE SERVICOS CRIADO COM SUCESSO!
echo ========================================================================
echo.
echo Agora voce pode:
echo   1. Acessar: http://localhost:8001/api/servicos/dashboard
echo   2. Ver servicos: http://localhost:8001/api/servicos/
echo   3. Buscar: http://localhost:8001/api/servicos/buscar/avancada?q=iluminacao
echo.
pause
