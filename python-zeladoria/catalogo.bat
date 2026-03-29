@echo off
chcp 65001 >nul

:menu
cls
echo ========================================
echo   CATÁLOGO DE SERVIÇOS - MENU PRINCIPAL
echo   Sistema de Zeladoria Urbana - Belém/PA
echo ========================================
echo.
echo   1. 🔧 Setup Completo (Primeira vez)
echo   2. 📋 Criar Tabela no Banco
echo   3. 🌱 Popular com Serviços
echo   4. 📊 Ver Estatísticas
echo   5. 📋 Listar Todos os Serviços
echo   6. 🔍 Buscar Serviço
echo   7. 🗂️  Ver Categorias
echo   8. 🚀 Iniciar API
echo   9. 🔄 Gerenciador Interativo
echo   0. ❌ Sair
echo.
echo ========================================
echo.

set /p opcao="Escolha uma opção: "

if "%opcao%"=="1" (
    call setup_catalogo.bat
    goto menu
)

if "%opcao%"=="2" (
    call criar_tabela.bat
    goto menu
)

if "%opcao%"=="3" (
    call popular_catalogo.bat
    goto menu
)

if "%opcao%"=="4" (
    call ver_estatisticas.bat
    goto menu
)

if "%opcao%"=="5" (
    call listar_servicos.bat
    goto menu
)

if "%opcao%"=="6" (
    call buscar_servico.bat
    goto menu
)

if "%opcao%"=="7" (
    cls
    echo ========================================
    echo   CATEGORIAS DE SERVIÇOS
    echo ========================================
    echo.
    python manage_catalogo.py categorias
    echo.
    pause
    goto menu
)

if "%opcao%"=="8" (
    call iniciar_api.bat
    goto menu
)

if "%opcao%"=="9" (
    python manage_catalogo.py
    goto menu
)

if "%opcao%"=="0" (
    echo.
    echo 👋 Até logo!
    exit /b 0
)

echo.
echo ❌ Opção inválida!
timeout /t 2 >nul
goto menu
