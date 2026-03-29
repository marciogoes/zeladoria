@echo off
echo Parando Sistema de Zeladoria Urbana...

taskkill /F /IM python.exe >nul 2>&1

echo [OK] Backend parado
pause
