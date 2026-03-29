@echo off
cls
echo ========================================
echo   TESTE DE HASH DE SENHA
echo ========================================
echo.

echo Testando bcrypt direto...
python -c "import bcrypt; senha = b'admin123'; hashed = bcrypt.hashpw(senha, bcrypt.gensalt()); print('Hash criado:', hashed.decode('utf-8')); print('Verificacao:', bcrypt.checkpw(senha, hashed))"

echo.
echo ========================================
echo.

echo Se mostrou "True" acima, o bcrypt funciona!
echo.
pause
