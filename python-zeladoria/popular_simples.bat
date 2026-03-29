@echo off
cls
echo IMPORTANTE: Antes de popular, ajuste os IDs das secretarias!
echo Arquivo: app\seeds\seed_servicos.py
echo Linha ~682
echo.
pause
echo.
echo Populando banco de dados...
echo.
python -c "from app.seeds.seed_servicos import seed_servicos; seed_servicos()"
echo.
pause
