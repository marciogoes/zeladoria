@echo off
chcp 65001 >nul
cls
echo ========================================
echo   POPULAR BANCO - 100+ Serviços
echo ========================================
echo.

echo ⚠️  ANTES DE CONTINUAR:
echo.
echo Você ajustou os IDs das secretarias em:
echo   app\seeds\seed_servicos.py ?
echo.
echo Pressione qualquer tecla para continuar...
pause >nul

echo.
echo Populando banco de dados...
echo.

python -c "from app.seeds.seed_servicos import seed_servicos; seed_servicos()"

echo.
echo Concluído!
echo.
pause
