@echo off
chcp 65001 >nul
:MENU
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🏛️  SISTEMA DE ZELADORIA URBANA - BELÉM/PA                ║
echo ║     📋  CATÁLOGO DE SERVIÇOS - MENU PRINCIPAL                  ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.
echo  ═══════════════════════════════════════════════════════════════
echo   🚀 INICIAR SISTEMA
echo  ═══════════════════════════════════════════════════════════════
echo.
echo   [1] 🔧 Iniciar Backend (FastAPI)
echo   [2] 🎨 Iniciar Frontend (React)
echo   [3] 🚀 Iniciar AMBOS (Backend + Frontend)
echo.
echo.
echo  ═══════════════════════════════════════════════════════════════
echo   📦 INSTALAÇÃO E CONFIGURAÇÃO
echo  ═══════════════════════════════════════════════════════════════
echo.
echo   [4] ⚙️  Setup Completo (Instalar tudo)
echo   [5] 📦 Instalar Frontend (npm)
echo   [6] ✅ Verificar Sistema
echo.
echo.
echo  ═══════════════════════════════════════════════════════════════
echo   📊 BANCO DE DADOS
echo  ═══════════════════════════════════════════════════════════════
echo.
echo   [7] 📋 Popular Catálogo de Serviços
echo   [8] 🔄 Recriar Banco de Dados
echo.
echo.
echo  ═══════════════════════════════════════════════════════════════
echo   🧪 TESTES E DIAGNÓSTICO
echo  ═══════════════════════════════════════════════════════════════
echo.
echo   [9]  🧪 Testar APIs do Catálogo
echo   [10] 🔍 Diagnóstico do Sistema
echo.
echo.
echo  ═══════════════════════════════════════════════════════════════
echo   📚 DOCUMENTAÇÃO E AJUDA
echo  ═══════════════════════════════════════════════════════════════
echo.
echo   [11] 📖 Ver Documentação
echo   [12] 🔧 Guia de Troubleshooting
echo   [13] 📋 Resumo da Implementação
echo.
echo.
echo  ═══════════════════════════════════════════════════════════════
echo   [0] ❌ SAIR
echo  ═══════════════════════════════════════════════════════════════
echo.
echo.

set /p opcao="  👉 Digite o número da opção desejada: "

if "%opcao%"=="0" goto FIM
if "%opcao%"=="1" goto BACKEND
if "%opcao%"=="2" goto FRONTEND
if "%opcao%"=="3" goto AMBOS
if "%opcao%"=="4" goto SETUP
if "%opcao%"=="5" goto INSTALAR_FRONT
if "%opcao%"=="6" goto VERIFICAR
if "%opcao%"=="7" goto POPULAR
if "%opcao%"=="8" goto RECRIAR
if "%opcao%"=="9" goto TESTAR
if "%opcao%"=="10" goto DIAGNOSTICO
if "%opcao%"=="11" goto DOCS
if "%opcao%"=="12" goto TROUBLE
if "%opcao%"=="13" goto RESUMO

echo.
echo ❌ Opção inválida! Tente novamente.
timeout /t 2 >nul
goto MENU

:BACKEND
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   🔧 INICIANDO BACKEND...                                      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
call INICIAR_BACKEND.bat
goto MENU

:FRONTEND
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   🎨 INICIANDO FRONTEND...                                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
call INICIAR_FRONTEND.bat
goto MENU

:AMBOS
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   🚀 INICIANDO BACKEND E FRONTEND...                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo ⚠️ ATENÇÃO: Será aberto em 2 janelas separadas
echo.
pause
start "" INICIAR_BACKEND.bat
timeout /t 3 >nul
start "" INICIAR_FRONTEND.bat
echo.
echo ✅ Backend e Frontend iniciados!
echo    • Backend: http://localhost:8000
echo    • Frontend: http://localhost:5173
echo.
pause
goto MENU

:SETUP
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   ⚙️  EXECUTANDO SETUP COMPLETO...                             ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
call SETUP_COMPLETO.bat
goto MENU

:INSTALAR_FRONT
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   📦 INSTALANDO FRONTEND...                                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
call INSTALAR_FRONTEND.bat
goto MENU

:VERIFICAR
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   ✅ VERIFICANDO SISTEMA...                                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
call VERIFICAR_SISTEMA.bat
goto MENU

:POPULAR
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   📋 POPULANDO CATÁLOGO...                                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
call POPULAR_CATALOGO.bat
goto MENU

:RECRIAR
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   🔄 RECRIANDO BANCO DE DADOS...                               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo ⚠️ ATENÇÃO: Isso vai apagar todos os dados!
echo.
set /p confirma="Tem certeza? (S/N): "
if /i "%confirma%"=="S" (
    cd python-zeladoria
    if exist zeladoria.db (
        echo Fazendo backup...
        copy zeladoria.db zeladoria_backup_%date:~-4%%date:~3,2%%date:~0,2%.db
        del zeladoria.db
    )
    echo Recriando banco...
    call venv\Scripts\activate
    python popular_catalogo_exemplo.py
    cd ..
    echo.
    echo ✅ Banco recriado com sucesso!
) else (
    echo Operação cancelada.
)
echo.
pause
goto MENU

:TESTAR
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   🧪 TESTANDO APIS...                                          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
call TESTAR_APIS.bat
goto MENU

:DIAGNOSTICO
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   🔍 DIAGNÓSTICO DO SISTEMA                                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
call VERIFICAR_SISTEMA.bat
goto MENU

:DOCS
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   📚 DOCUMENTAÇÃO DISPONÍVEL                                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Abrindo documentação...
echo.
echo Arquivos disponíveis:
echo   • README_CATALOGO.md (guia rápido)
echo   • GUIA_CATALOGO_SERVICOS.md (completo)
echo   • RESUMO_IMPLEMENTACAO.txt (overview)
echo   • TROUBLESHOOTING.txt (problemas comuns)
echo.

if exist README_CATALOGO.md (
    echo [1] README_CATALOGO.md
    echo [2] GUIA_CATALOGO_SERVICOS.md
    echo [3] RESUMO_IMPLEMENTACAO.txt
    echo [4] TROUBLESHOOTING.txt
    echo [5] Voltar ao menu
    echo.
    set /p doc="Escolha um documento: "
    
    if "!doc!"=="1" start notepad README_CATALOGO.md
    if "!doc!"=="2" start notepad GUIA_CATALOGO_SERVICOS.md
    if "!doc!"=="3" start notepad RESUMO_IMPLEMENTACAO.txt
    if "!doc!"=="4" start notepad TROUBLESHOOTING.txt
) else (
    echo ❌ Arquivos de documentação não encontrados!
)
echo.
pause
goto MENU

:TROUBLE
cls
type TROUBLESHOOTING.txt
echo.
pause
goto MENU

:RESUMO
cls
type RESUMO_IMPLEMENTACAO.txt
echo.
pause
goto MENU

:FIM
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     👋 Obrigado por usar o Sistema de Zeladoria!              ║
echo ║     🏛️  Prefeitura Municipal de Belém - PA                    ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
timeout /t 2 >nul
exit
