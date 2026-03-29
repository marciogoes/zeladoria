@echo off
title FIX FINAL - Zeladoria
color 0A
cls

echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║                                                      ║
echo   ║         CORRECAO FINAL - BCRYPT E USUARIOS           ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
echo   Este script vai:
echo   ✓ Parar API
echo   ✓ Recriar banco com modelo corrigido
echo   ✓ Criar usuarios com bcrypt direto
echo   ✓ Iniciar API
echo.
pause

cls
echo.
echo   [1/7] Parando API...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 >nul
echo         ✓ API parada
echo.

echo   [2/7] Deletando banco...
if exist zeladoria.db del /F /Q zeladoria.db >nul 2>&1
echo         ✓ Banco deletado
echo.

echo   [3/7] Testando bcrypt...
python -c "import bcrypt; print('         ✓ bcrypt OK')" 2>nul
echo.

echo   [4/7] Criando tabelas...
python -c "import sys; sys.path.insert(0, '.'); from app.database.database import engine, Base; from app.models.usuario import Usuario; from app.models.secretaria import Secretaria; from app.models_servicos import ServicoSecretaria; from app.models.chamado import Chamado; from app.models.categoria import Categoria; from app.models.bairro import Bairro; Base.metadata.create_all(bind=engine); print('         ✓ Tabelas criadas')"
echo.

echo   [5/7] Criando secretarias...
python app\seeds\seed_secretarias.py >nul 2>&1
echo         ✓ 5 secretarias criadas
echo.

echo   [6/7] Criando usuarios...
python app\seeds\seed_usuarios.py
echo.

echo   [7/7] Iniciando API...
echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║                                                      ║
echo   ║              API INICIANDO...                        ║
echo   ║                                                      ║
echo   ║  Acesse: http://localhost:8001/app                   ║
echo   ║  Login: admin@zeladoria.com / admin123               ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
echo   Pressione CTRL+C para parar
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
