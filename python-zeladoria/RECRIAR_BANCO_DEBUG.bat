@echo off
title Recriar Banco - DEBUG
color 0E
cls

echo ========================================
echo   RECRIAR BANCO - MODO DEBUG
echo ========================================
echo.

echo [1/6] Fechando API...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM uvicorn.exe /T >nul 2>&1
timeout /t 2 >nul
echo OK - Processos finalizados
echo.

echo [2/6] Deletando banco antigo...
if exist zeladoria.db (
    del /F /Q zeladoria.db
    if exist zeladoria.db (
        echo ERRO - Nao conseguiu deletar!
        pause
        exit
    )
    echo OK - Banco deletado
) else (
    echo OK - Banco nao existia
)
echo.

echo [3/6] Criando tabelas (COM DETALHES)...
echo.
python migrations\criar_todas_tabelas.py
echo.
if %errorlevel% neq 0 (
    echo.
    echo ERRO AO CRIAR TABELAS!
    echo Veja o erro acima ^^^
    echo.
    pause
    exit
)
echo.

echo [4/6] Criando secretarias...
echo.
python app\seeds\seed_secretarias.py
echo.
if %errorlevel% neq 0 (
    echo ERRO AO CRIAR SECRETARIAS!
    pause
    exit
)
echo.

echo [5/6] Criando usuarios...
echo.
python app\seeds\seed_usuarios.py
echo.
if %errorlevel% neq 0 (
    echo ERRO AO CRIAR USUARIOS!
    pause
    exit
)
echo.

echo [6/6] Verificando banco...
python -c "from app.database.database import SessionLocal; from app.models.usuario import Usuario; from app.models.secretaria import Secretaria; db = SessionLocal(); u = db.query(Usuario).count(); s = db.query(Secretaria).count(); db.close(); print(f'OK: {u} usuarios e {s} secretarias')"
echo.

echo ========================================
echo   SUCESSO!
echo ========================================
echo.
echo Execute: INICIAR_API_8001.bat
echo Acesse: http://localhost:8001/app
echo Login: admin@zeladoria.com / admin123
echo.
pause
