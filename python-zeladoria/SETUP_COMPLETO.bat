@echo off
cls
echo ========================================
echo   SETUP COMPLETO DO SISTEMA
echo ========================================
echo.
echo Este script vai:
echo   1. RESETAR o banco de dados
echo   2. Criar todas as tabelas
echo   3. Popular secretarias
echo   4. Criar usuarios de teste
echo   5. Popular catalogo de servicos
echo.
echo ATENCAO: Isso vai DELETAR todos os dados existentes!
echo.
pause
echo.

echo [1/5] Resetando banco de dados...
if exist zeladoria.db (
    del zeladoria.db
    echo OK: Banco antigo deletado
)
echo.

echo [2/5] Criando tabelas...
python migrations\criar_todas_tabelas.py
echo.

echo [3/5] Criando secretarias...
python app\seeds\seed_secretarias.py
echo.

echo [4/5] Criando usuarios de teste...
python app\seeds\seed_usuarios.py
echo.

echo [5/5] Populando catalogo de servicos...
python -c "from app.seeds.seed_servicos import seed_servicos; seed_servicos()"

echo.
echo ========================================
echo   SETUP COMPLETO!
echo ========================================
echo.
echo Agora execute: INICIAR_API_8001.bat
echo E acesse: http://localhost:8001/app
echo.
echo ========================================
echo   CREDENCIAIS DE TESTE
echo ========================================
echo.
echo Admin:    admin@zeladoria.com    / admin123
echo SEURB:    seurb@zeladoria.com    / seurb123
echo SESAN:    sesan@zeladoria.com    / sesan123
echo SEMOB:    semob@zeladoria.com    / semob123
echo SEMMA:    semma@zeladoria.com    / semma123
echo SESMA:    sesma@zeladoria.com    / sesma123
echo Gestor:   gestor@zeladoria.com   / gestor123
echo Equipe:   equipe@zeladoria.com   / equipe123
echo Cidadao:  cidadao@zeladoria.com  / cidadao123
echo.
echo ========================================
echo.
pause
