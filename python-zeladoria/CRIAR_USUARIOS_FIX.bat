@echo off
cls
echo ========================================
echo   CRIAR USUARIOS - VERSAO CORRIGIDA
echo ========================================
echo.

echo [1] Parando API...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 >nul
echo OK
echo.

echo [2] Testando bcrypt...
python -c "import bcrypt; senha = b'teste'; hash = bcrypt.hashpw(senha, bcrypt.gensalt()); print('OK: bcrypt funciona')" 2>nul
if %errorlevel% neq 0 (
    echo ERRO: bcrypt nao funciona!
    pause
    exit
)
echo.

echo [3] Criando usuarios...
python app\seeds\seed_usuarios.py
echo.

if %errorlevel%==0 (
    echo ========================================
    echo   USUARIOS CRIADOS COM SUCESSO!
    echo ========================================
    echo.
    echo Execute: INICIAR_API_8001.bat
    echo Acesse: http://localhost:8001/app
    echo Login: admin@zeladoria.com / admin123
) else (
    echo ERRO ao criar usuarios!
)

echo.
pause
