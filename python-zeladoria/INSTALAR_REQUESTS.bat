@echo off
chcp 65001 >nul
echo.
echo ========================================================
echo    INSTALANDO BIBLIOTECA REQUESTS
echo ========================================================
echo.

call venv\Scripts\activate
pip install requests

echo.
echo ========================================================
echo    INSTALACAO CONCLUIDA!
echo ========================================================
echo.
pause
