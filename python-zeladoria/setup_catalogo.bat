@echo off
chcp 65001 >nul
echo ========================================
echo   SETUP COMPLETO - CATÁLOGO DE SERVIÇOS
echo   Sistema de Zeladoria Urbana - Belém/PA
echo ========================================
echo.

echo 📋 Este script vai:
echo   1. Criar a tabela no banco de dados
echo   2. Popular com 100+ serviços
echo   3. Verificar a instalação
echo   4. Mostrar estatísticas
echo.

pause

echo.
echo ========================================
echo   PASSO 1/4 - Criando Tabela no Banco
echo ========================================
echo.

python -c "from migrations.create_servicos_table import criar_tabela_servicos; criar_tabela_servicos()"

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERRO ao criar tabela!
    echo Verifique se o banco de dados está configurado corretamente.
    pause
    exit /b 1
)

echo.
echo ✅ Tabela criada com sucesso!
echo.
pause

echo.
echo ========================================
echo   PASSO 2/4 - Verificando Tabela
echo ========================================
echo.

python -c "from migrations.create_servicos_table import verificar_tabela; verificar_tabela()"

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERRO ao verificar tabela!
    pause
    exit /b 1
)

echo.
pause

echo.
echo ========================================
echo   PASSO 3/4 - Populando com Serviços
echo ========================================
echo.
echo ⚠️  IMPORTANTE: 
echo Antes de continuar, verifique se você ajustou os IDs
echo das secretarias em: app\seeds\seed_servicos.py
echo.
echo Deseja continuar?
pause

python -c "from app.seeds import seed_servicos; seed_servicos()"

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERRO ao popular banco!
    echo.
    echo Possíveis causas:
    echo - IDs de secretarias não existem no banco
    echo - Códigos duplicados
    echo - Problema de conexão com o banco
    pause
    exit /b 1
)

echo.
echo ✅ Banco populado com sucesso!
echo.
pause

echo.
echo ========================================
echo   PASSO 4/4 - Estatísticas
echo ========================================
echo.

python manage_catalogo.py stats

echo.
echo ========================================
echo   ✅ SETUP COMPLETO!
echo ========================================
echo.
echo O catálogo de serviços está pronto para uso!
echo.
echo Próximos passos:
echo   • Execute: iniciar_api.bat para iniciar o servidor
echo   • Acesse: http://localhost:8000/docs
echo   • Execute: listar_servicos.bat para ver os serviços
echo.

pause
