@echo off
chcp 65001 >nul
echo ============================================================
echo   INSTALAÇÃO COMPLETA - CATÁLOGO DE SERVIÇOS
echo   Sistema de Zeladoria Urbana - Belém/PA
echo ============================================================
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado!
    echo    Instale Python 3.8+ em https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version
echo.

:: Passo 1: Criar Tabela
echo ============================================================
echo   PASSO 1/3 - CRIAR TABELA NO BANCO DE DADOS
echo ============================================================
echo.
echo Criando tabela 'servicos_secretaria'...
python -c "from migrations.create_servicos_table import criar_tabela_servicos; criar_tabela_servicos()"

if errorlevel 1 (
    echo.
    echo ❌ Erro ao criar tabela!
    echo    Verifique a conexão com o banco de dados
    pause
    exit /b 1
)

echo.
echo ✅ Tabela criada com sucesso!
echo.

:: Passo 2: Ajustar IDs
echo ============================================================
echo   PASSO 2/3 - CONFIGURAR IDs DAS SECRETARIAS
echo ============================================================
echo.
echo ⚠️  IMPORTANTE: Você precisa ajustar os IDs das secretarias!
echo.
echo O arquivo que precisa ser editado é:
echo   app\seeds\seed_servicos.py
echo.
echo Procure por 'secretarias_map' e ajuste os IDs:
echo.
echo   secretarias_map = {
echo       "SEURB": 1,   # ^<-- Coloque o ID real da SEURB
echo       "SESAN": 2,   # ^<-- Coloque o ID real da SESAN
echo       "SEMOB": 3,   # ^<-- Coloque o ID real da SEMOB
echo       "SEMMA": 4,   # ^<-- Coloque o ID real da SEMMA
echo       "SESMA": 5,   # ^<-- Coloque o ID real da SESMA
echo   }
echo.
echo.

:: Perguntar se quer abrir o arquivo
set /p ABRIR="Deseja abrir o arquivo para editar agora? (S/N): "
if /i "%ABRIR%"=="S" (
    start notepad app\seeds\seed_servicos.py
    echo.
    echo 📝 Arquivo aberto no Notepad
    echo    Edite os IDs e salve o arquivo
    echo.
    pause
)

echo.
set /p CONTINUAR="IDs já estão corretos? Deseja popular o banco? (S/N): "
if /i not "%CONTINUAR%"=="S" (
    echo.
    echo ⏸️  Instalação pausada
    echo    Execute novamente quando os IDs estiverem corretos
    pause
    exit /b 0
)

:: Passo 3: Popular Banco
echo.
echo ============================================================
echo   PASSO 3/3 - POPULAR BANCO COM 100+ SERVIÇOS
echo ============================================================
echo.
echo Inserindo serviços no banco de dados...
echo Isso pode levar alguns segundos...
echo.

python manage_catalogo.py seed

if errorlevel 1 (
    echo.
    echo ❌ Erro ao popular banco!
    echo    Verifique os IDs das secretarias
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo ============================================================
echo.
echo ✅ Tabela criada
echo ✅ 100+ serviços cadastrados
echo ✅ Sistema pronto para uso
echo.
echo 📊 PRÓXIMOS PASSOS:
echo.
echo   1. Ver serviços cadastrados:
echo      execute_listar.bat
echo.
echo   2. Ver estatísticas:
echo      execute_stats.bat
echo.
echo   3. Iniciar API:
echo      iniciar_api.bat
echo.
echo   4. Abrir gerenciador interativo:
echo      gerenciador.bat
echo.
pause
