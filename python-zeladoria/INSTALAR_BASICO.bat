@echo off
cls
echo ========================================
echo   INSTALAR DEPENDENCIAS ESSENCIAIS
echo ========================================
echo.
echo Instalando pacotes basicos...
echo.

python -m pip install fastapi uvicorn sqlalchemy passlib python-jose python-multipart pydantic pymysql email-validator python-dotenv pillow

echo.
echo ========================================
echo   INSTALACAO CONCLUIDA!
echo ========================================
echo.
pause
