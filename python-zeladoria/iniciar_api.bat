@echo off
cls
echo ========================================
echo   INICIAR API - Escolher Porta
echo ========================================
echo.
echo Qual porta deseja usar?
echo.
echo [1] Porta 8000 (padrao)
echo [2] Porta 8001
echo [3] Porta 8080
echo [4] Outra porta
echo [0] Cancelar
echo.

set /p opcao="Opcao: "

if "%opcao%"=="1" set PORTA=8000
if "%opcao%"=="2" set PORTA=8001
if "%opcao%"=="3" set PORTA=8080
if "%opcao%"=="4" (
    set /p PORTA="Digite a porta: "
)
if "%opcao%"=="0" exit

cls
echo ========================================
echo   INICIANDO API NA PORTA %PORTA%
echo ========================================
echo.
echo Servidor em: http://localhost:%PORTA%
echo Documentacao: http://localhost:%PORTA%/docs
echo.
echo Pressione CTRL+C para parar
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port %PORTA%

pause
