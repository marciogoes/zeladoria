@echo off
cls
echo ========================================
echo   CRIAR USUARIOS DE TESTE
echo ========================================
echo.
echo Criando 9 usuarios de teste...
echo.

python app\seeds\seed_usuarios.py

echo.
echo ========================================
pause
