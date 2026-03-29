@echo off
title Recriar Banco - Zeladoria Belem
color 0A
cls

echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║                                                      ║
echo   ║         RECRIAR BANCO DE DADOS COMPLETO              ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
echo   Pressione qualquer tecla para comecar...
pause >nul

cls
echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║              RECRIANDO BANCO...                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.

echo   [1/5] Fechando API...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM uvicorn.exe /T >nul 2>&1
timeout /t 2 >nul
echo         ✓ Processos finalizados
echo.

echo   [2/5] Deletando banco antigo...
if exist zeladoria.db (
    del /F /Q zeladoria.db
    if exist zeladoria.db (
        echo         ✗ ERRO - Nao conseguiu deletar!
        pause
        exit
    )
    echo         ✓ Banco deletado
) else (
    echo         ✓ Banco nao existia
)
echo.

echo   [3/5] Criando tabelas...
python -c "import sys; import os; sys.path.insert(0, '.'); from app.database.database import engine, Base; from app.models.usuario import Usuario; from app.models.secretaria import Secretaria; from app.models_servicos import ServicoSecretaria; from app.models.chamado import Chamado; from app.models.categoria import Categoria; from app.models.bairro import Bairro; Base.metadata.create_all(bind=engine); print('         ✓ Tabelas criadas')"
echo.

echo   [4/5] Criando secretarias e usuarios...
python -c "from app.seeds.seed_secretarias import seed_secretarias; from app.seeds.seed_usuarios import seed_usuarios; seed_secretarias(); seed_usuarios()" 2>nul
if %errorlevel%==0 (
    echo         ✓ Dados populados
) else (
    echo         ✗ Erro ao popular dados
    echo.
    echo Tentando individualmente...
    echo.
    python app\seeds\seed_secretarias.py
    echo.
    python app\seeds\seed_usuarios.py
)
echo.

echo   [5/5] Verificando banco...
python -c "from app.database.database import SessionLocal; from app.models.usuario import Usuario; from app.models.secretaria import Secretaria; db = SessionLocal(); u = db.query(Usuario).count(); s = db.query(Secretaria).count(); db.close(); print(f'         ✓ {u} usuarios e {s} secretarias criados')"
echo.

echo   ╔══════════════════════════════════════════════════════╗
echo   ║                                                      ║
echo   ║              BANCO RECRIADO COM SUCESSO!             ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║         CREDENCIAIS DE TESTE                         ║
echo   ╠══════════════════════════════════════════════════════╣
echo   ║                                                      ║
echo   ║  Admin:    admin@zeladoria.com    / admin123         ║
echo   ║  SEURB:    seurb@zeladoria.com    / seurb123         ║
echo   ║  SESAN:    sesan@zeladoria.com    / sesan123         ║
echo   ║  SEMOB:    semob@zeladoria.com    / semob123         ║
echo   ║  SEMMA:    semma@zeladoria.com    / semma123         ║
echo   ║  SESMA:    sesma@zeladoria.com    / sesma123         ║
echo   ║  Gestor:   gestor@zeladoria.com   / gestor123        ║
echo   ║  Equipe:   equipe@zeladoria.com   / equipe123        ║
echo   ║  Cidadao:  cidadao@zeladoria.com  / cidadao123       ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
echo   ╔══════════════════════════════════════════════════════╗
echo   ║         PROXIMOS PASSOS                              ║
echo   ╠══════════════════════════════════════════════════════╣
echo   ║                                                      ║
echo   ║  1. Execute: INICIAR_API_8001.bat                    ║
echo   ║                                                      ║
echo   ║  2. Acesse: http://localhost:8001/app                ║
echo   ║                                                      ║
echo   ║  3. Login: admin@zeladoria.com / admin123            ║
echo   ║                                                      ║
echo   ╚══════════════════════════════════════════════════════╝
echo.
pause
