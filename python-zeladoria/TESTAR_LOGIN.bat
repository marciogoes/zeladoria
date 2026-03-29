@echo off
cls
echo ========================================
echo   TESTE DE LOGIN - API
echo ========================================
echo.

echo Testando login com admin@zeladoria.com...
echo.

curl -X POST http://localhost:8001/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@zeladoria.com\",\"senha\":\"admin123\"}"

echo.
echo.
echo ========================================
echo.

if %errorlevel%==0 (
    echo Se aparecer um token acima, o login funciona!
    echo O problema pode estar no frontend.
) else (
    echo API nao esta respondendo.
    echo Execute: INICIAR_API_8001.bat
)

echo.
pause
