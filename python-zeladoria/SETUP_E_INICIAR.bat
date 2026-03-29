@echo off
title SETUP RAPIDO - Zeladoria Belem
color 0A
cls

echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║                                                      ║
echo   ║    🏛️  SISTEMA DE ZELADORIA URBANA - BELÉM/PA       ║
echo   ║                                                      ║
echo   ║               SETUP RÁPIDO - 60 SEGUNDOS            ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
echo   Isso vai:
echo   ✓ Resetar banco
echo   ✓ Criar tabelas
echo   ✓ Popular dados
echo   ✓ Iniciar API
echo.
echo   Pressione qualquer tecla para começar...
pause >nul

cls
echo.
echo   [1/6] Resetando banco...
if exist zeladoria.db del zeladoria.db >nul 2>&1

echo   [2/6] Criando tabelas...
python migrations\criar_todas_tabelas.py >nul 2>&1

echo   [3/6] Criando secretarias...
python app\seeds\seed_secretarias.py >nul 2>&1

echo   [4/6] Criando usuarios...
python app\seeds\seed_usuarios.py >nul 2>&1

echo   [5/6] Populando servicos...
python -c "from app.seeds.seed_servicos import seed_servicos; seed_servicos()" >nul 2>&1

echo   [6/6] Iniciando API...
echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║                                                      ║
echo   ║    ✅ SETUP CONCLUÍDO!                               ║
echo   ║                                                      ║
echo   ║    🌐 Acesse: http://localhost:8001/app              ║
echo   ║                                                      ║
echo   ║    👤 Login: admin@zeladoria.com / admin123          ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
echo   Iniciando servidor...
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
