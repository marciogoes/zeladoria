@echo off
cls
echo ========================================
echo   INSTALAR DEPENDENCIAS
echo   Via requirements.txt
echo ========================================
echo.
echo Instalando todas as dependencias do projeto...
echo Isso pode levar alguns minutos...
echo.

python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   ERRO NA INSTALACAO!
    echo ========================================
    echo.
    echo Tentando instalacao basica...
    echo.
    python -m pip install fastapi uvicorn sqlalchemy passlib python-jose python-multipart pydantic pymysql
)

echo.
echo ========================================
echo   INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Agora execute: INICIAR_API_8001.bat
echo.
pause
