@echo off
cls
echo Criando tabela servicos_secretaria...
echo.
python migrations\create_servicos_table.py
echo.
pause
