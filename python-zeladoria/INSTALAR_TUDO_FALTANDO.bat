@echo off
cls
echo ========================================
echo   INSTALAR TODAS DEPENDENCIAS FALTANTES
echo ========================================
echo.
echo Instalando TUDO que esta faltando...
echo.

python -m pip install fastapi uvicorn sqlalchemy passlib python-jose python-multipart pydantic pymysql email-validator python-dotenv Pillow openpyxl pandas python-dateutil geopy requests bcrypt

echo.
echo ========================================
echo   INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Agora execute: INICIAR_API_8001.bat
echo.
pause
