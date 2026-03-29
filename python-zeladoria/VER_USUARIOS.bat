@echo off
cls
echo ========================================
echo   VERIFICAR USUARIOS NO BANCO
echo ========================================
echo.

python -c "from app.database.database import SessionLocal; from app.models.usuario import Usuario; db = SessionLocal(); usuarios = db.query(Usuario).all(); print(f'\nTotal: {len(usuarios)} usuario(s) no banco\n'); print('Email                      | Tipo'); print('-' * 50); [print(f'{u.email:30} | {u.tipo}') for u in usuarios]; db.close()" 2>nul

if %errorlevel% neq 0 (
    echo.
    echo ERRO: Nao conseguiu acessar o banco!
    echo Execute: RECRIAR_BANCO.bat
)

echo.
echo ========================================
pause
