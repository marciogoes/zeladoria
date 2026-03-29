@echo off
chcp 65001 >nul
cls
echo ========================================
echo   INSTALAR DEPENDENCIAS
echo ========================================
echo.
echo Instalando pacotes necessarios...
echo.
echo [1/5] SQLAlchemy (banco de dados)
pip install sqlalchemy
echo.
echo [2/5] FastAPI (API)
pip install fastapi
echo.
echo [3/5] Uvicorn (servidor)
pip install uvicorn
echo.
echo [4/5] Pydantic (validacao)
pip install pydantic
echo.
echo [5/5] PyMySQL (MySQL/MariaDB)
pip install pymysql
echo.
echo ========================================
echo   INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Agora você pode:
echo   1. Executar MENU.bat novamente
echo   2. Escolher opcao [2] para criar a tabela
echo.
pause
