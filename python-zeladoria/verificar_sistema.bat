@echo off
cls
echo ========================================
echo   VERIFICACAO DO SISTEMA
echo ========================================
echo.

echo [1/5] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado
    pause
    exit
)
echo OK: Python instalado
echo.

echo [2/5] Verificando dependencias...
python -c "import fastapi, uvicorn, sqlalchemy, passlib, pydantic; print('OK: Dependencias principais instaladas')"
if %errorlevel% neq 0 (
    echo ERRO: Faltam dependencias
    echo Execute: INSTALAR_TUDO_FALTANDO.bat
    pause
    exit
)
echo.

echo [3/5] Verificando banco de dados...
if exist zeladoria.db (
    echo OK: Banco de dados existe
) else (
    echo AVISO: Banco de dados nao encontrado
    echo Execute: SETUP_COMPLETO.bat
)
echo.

echo [4/5] Verificando secretarias...
python -c "from app.database.database import SessionLocal; from app.models.secretaria import Secretaria; db = SessionLocal(); count = db.query(Secretaria).count(); db.close(); print(f'OK: {count} secretaria(s) cadastrada(s)' if count > 0 else 'AVISO: Nenhuma secretaria. Execute CRIAR_SECRETARIAS.bat')"
echo.

echo [5/5] Verificando usuarios...
python -c "from app.database.database import SessionLocal; from app.models.usuario import Usuario; db = SessionLocal(); count = db.query(Usuario).count(); db.close(); print(f'OK: {count} usuario(s) cadastrado(s)' if count > 0 else 'AVISO: Nenhum usuario. Execute CRIAR_USUARIOS.bat')"
echo.

echo ========================================
echo   VERIFICACAO CONCLUIDA
echo ========================================
echo.
echo Se tudo estiver OK, execute:
echo   INICIAR_API_8001.bat
echo.
echo E acesse:
echo   http://localhost:8001/app
echo.
pause
