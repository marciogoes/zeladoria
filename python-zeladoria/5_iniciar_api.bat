@echo off
chcp 65001 >nul
cls
echo ========================================
echo   INICIAR API
echo ========================================
echo.
echo Servidor será iniciado em:
echo   http://localhost:8000
echo.
echo Documentação em:
echo   http://localhost:8000/docs
echo.
echo Pressione CTRL+C para parar
echo.

uvicorn main:app --reload

pause
