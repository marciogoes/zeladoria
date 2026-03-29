@echo off
chcp 65001 >nul
cls
color 0A
mode con: cols=80 lines=30

echo.
echo    ╔════════════════════════════════════════════════════════════════╗
echo    ║                                                                ║
echo    ║         🏛️  SISTEMA DE ZELADORIA - BELÉM/PA                    ║
echo    ║         📋  CATÁLOGO DE SERVIÇOS                               ║
echo    ║                                                                ║
echo    ║         ✅ VERSÃO 1.0.0 - COMPLETO E FUNCIONAL                 ║
echo    ║                                                                ║
echo    ╔════════════════════════════════════════════════════════════════╗
echo.
echo.
echo         🚀 BEM-VINDO! ESCOLHA UMA OPÇÃO:
echo.
echo.
echo         [1] ⚡ INICIAR SISTEMA (recomendado)
echo             Inicia backend e frontend automaticamente
echo.
echo         [2] 📖 VER DOCUMENTAÇÃO
echo             Guias, manuais e ajuda
echo.
echo         [3] 🔧 CONFIGURAR/INSTALAR
echo             Setup e instalação
echo.
echo         [0] ❌ SAIR
echo.
echo    ════════════════════════════════════════════════════════════════
echo.

set /p opt="         Digite sua escolha: "

if "%opt%"=="1" goto INICIAR
if "%opt%"=="2" goto DOCS
if "%opt%"=="3" goto CONFIG
if "%opt%"=="0" exit
goto START

:INICIAR
cls
echo.
echo    ════════════════════════════════════════════════════════════════
echo     🚀 INICIANDO SISTEMA...
echo    ════════════════════════════════════════════════════════════════
echo.
echo     Backend será aberto em uma janela...
echo     Frontend será aberto em outra janela...
echo.
echo     Aguarde alguns segundos e acesse:
echo     👉 http://localhost:5173
echo.
echo    ════════════════════════════════════════════════════════════════
echo.
start "" INICIAR_BACKEND.bat
timeout /t 3 >nul
start "" INICIAR_FRONTEND.bat
echo.
echo     ✅ Sistema iniciado!
echo.
pause
exit

:DOCS
cls
start notepad README.md
exit

:CONFIG
cls
call MENU_CATALOGO.bat
exit

:START
cls
color 0A
mode con: cols=80 lines=30
echo.
echo    ╔════════════════════════════════════════════════════════════════╗
echo    ║                                                                ║
echo    ║         🏛️  SISTEMA DE ZELADORIA - BELÉM/PA                    ║
echo    ║         📋  CATÁLOGO DE SERVIÇOS                               ║
echo    ║                                                                ║
echo    ║         ✅ VERSÃO 1.0.0 - COMPLETO E FUNCIONAL                 ║
echo    ║                                                                ║
echo    ╔════════════════════════════════════════════════════════════════╗
echo.
echo.
echo         🚀 BEM-VINDO! ESCOLHA UMA OPÇÃO:
echo.
echo.
echo         [1] ⚡ INICIAR SISTEMA (recomendado)
echo             Inicia backend e frontend automaticamente
echo.
echo         [2] 📖 VER DOCUMENTAÇÃO
echo             Guias, manuais e ajuda
echo.
echo         [3] 🔧 CONFIGURAR/INSTALAR
echo             Setup e instalação
echo.
echo         [0] ❌ SAIR
echo.
echo    ════════════════════════════════════════════════════════════════
echo.

set /p opt="         Digite sua escolha: "

if "%opt%"=="1" goto INICIAR
if "%opt%"=="2" goto DOCS
if "%opt%"=="3" goto CONFIG
if "%opt%"=="0" exit
goto START
