@echo off
cls
echo ========================================
echo   INSTALAR TODAS AS DEPENDENCIAS
echo   Sistema de Zeladoria Completo
echo ========================================
echo.
echo Instalando pacotes necessarios...
echo.

echo [1/15] SQLAlchemy
python -m pip install sqlalchemy

echo [2/15] FastAPI
python -m pip install fastapi

echo [3/15] Uvicorn
python -m pip install uvicorn[standard]

echo [4/15] Pydantic
python -m pip install pydantic

echo [5/15] PyMySQL
python -m pip install pymysql

echo [6/15] Passlib
python -m pip install passlib[bcrypt]

echo [7/15] Python-Jose (JWT)
python -m pip install python-jose[cryptography]

echo [8/15] Python-Multipart
python -m pip install python-multipart

echo [9/15] Pillow (Imagens)
python -m pip install pillow

echo [10/15] Pandas (CSV/Excel)
python -m pip install pandas

echo [11/15] Openpyxl (Excel)
python -m pip install openpyxl

echo [12/15] Python-Dotenv
python -m pip install python-dotenv

echo [13/15] Httpx (Cliente HTTP)
python -m pip install httpx

echo [14/15] Email-Validator
python -m pip install email-validator

echo [15/15] Atualizando pip
python -m pip install --upgrade pip

echo.
echo ========================================
echo   INSTALACAO CONCLUIDA!
echo ========================================
echo.
echo Agora execute: INICIAR_API_8001.bat
echo.
pause
