@echo off
cls
echo ========================================
echo   INSTALAR DEPENDENCIAS
echo ========================================
echo.
echo Instalando pacotes necessarios...
echo.
echo [1/5] SQLAlchemy
python -m pip install sqlalchemy
echo.
echo [2/5] FastAPI
python -m pip install fastapi
echo.
echo [3/5] Uvicorn
python -m pip install uvicorn
echo.
echo [4/5] Pydantic
python -m pip install pydantic
echo.
echo [5/5] PyMySQL
python -m pip install pymysql
echo.
echo ========================================
echo   INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Agora execute: criar_tabela_simples.bat
echo.
pause
