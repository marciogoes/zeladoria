@echo off
cls
echo ========================================
echo   POPULAR APENAS USUARIOS
echo ========================================
echo.

echo Criando usuarios de teste...
echo.

python app\seeds\seed_usuarios.py

echo.
echo ========================================
echo.

if %errorlevel%==0 (
    echo SUCESSO! Usuarios criados.
    echo.
    echo Agora tente fazer login novamente:
    echo   http://localhost:8001/app
    echo.
    echo Login: admin@zeladoria.com / admin123
) else (
    echo ERRO ao criar usuarios!
    echo.
    echo Tente: RECRIAR_BANCO.bat
)

echo.
pause
