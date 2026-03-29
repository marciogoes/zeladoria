@echo off
cls
echo ========================================
echo   RESET TOTAL - MATAR API E RESETAR
echo ========================================
echo.

echo [1/7] Matando processos do Python/Uvicorn...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM uvicorn.exe /T >nul 2>&1
timeout /t 2 >nul
echo OK: Processos finalizados

echo.
echo [2/7] Deletando banco...
if exist zeladoria.db (
    del /F /Q zeladoria.db
    if exist zeladoria.db (
        echo ERRO: Banco ainda travado. Reinicie o PC.
        pause
        exit
    )
)
echo OK: Banco deletado

echo.
echo [3/7] Criando tabelas...
python migrations\criar_todas_tabelas.py

echo.
echo [4/7] Populando secretarias...
python app\seeds\seed_secretarias.py

echo.
echo [5/7] Criando usuarios...
python app\seeds\seed_usuarios.py

echo.
echo [6/7] Testando banco...
python -c "from app.database.database import SessionLocal; from app.models.usuario import Usuario; from app.models.secretaria import Secretaria; db = SessionLocal(); u = db.query(Usuario).count(); s = db.query(Secretaria).count(); db.close(); print(f'OK: {u} usuarios, {s} secretarias')"

echo.
echo [7/7] Iniciando API...
echo.
echo ========================================
echo   SUCESSO! API INICIANDO...
echo ========================================
echo.
echo Acesse: http://localhost:8001/app
echo Login: admin@zeladoria.com / admin123
echo.
echo Pressione CTRL+C para parar a API
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
