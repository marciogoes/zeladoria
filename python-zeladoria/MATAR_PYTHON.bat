@echo off
chcp 65001 > nul
color 0C

echo.
echo ======================================================================
echo   MATAR TODAS AS INSTANCIAS DO PYTHON/UVICORN
echo ======================================================================
echo.
echo Este script vai parar TODAS as instancias do Python rodando
echo Isso garante que a API antiga seja completamente fechada
echo.
pause

echo.
echo Procurando processos Python rodando...
echo.

tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I "python.exe" >NUL

if %ERRORLEVEL% EQU 0 (
    echo Encontrados processos Python. Matando...
    taskkill /F /IM python.exe /T 2>NUL
    echo.
    echo Processos Python finalizados!
) else (
    echo Nenhum processo Python encontrado.
)

echo.
echo ======================================================================
echo   AGORA EXECUTE: INICIAR_API_8001.bat
echo ======================================================================
echo.
pause
