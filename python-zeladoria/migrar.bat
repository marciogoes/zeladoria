@echo off
echo Migrando para Sistema de Secretarias...
echo.
call venv\Scripts\activate.bat
python migrar_secretarias.py
echo.
echo Migracao concluida!
pause
