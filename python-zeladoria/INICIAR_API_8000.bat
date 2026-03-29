@echo off
cls
echo ========================================
echo   INICIAR API - Porta 8000
echo ========================================
echo.
echo Servidor sera iniciado em:
echo   http://localhost:8000
echo.
echo Documentacao em:
echo   http://localhost:8000/docs
echo.
echo Pressione CTRL+C para parar
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
