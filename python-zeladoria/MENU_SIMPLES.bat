@echo off
cls

:menu
cls
echo ========================================
echo   CATALOGO DE SERVICOS - MENU
echo ========================================
echo.
echo  PRIMEIRA VEZ?
echo  [I] Instalar Dependencias
echo.
echo  SETUP:
echo  [1] Diagnostico
echo  [2] Criar Tabela
echo  [3] Popular Banco
echo.
echo  USO:
echo  [4] Listar Servicos
echo  [5] Estatisticas
echo  [7] Iniciar API
echo.
echo  [0] Sair
echo.
echo ========================================
echo.

set /p opcao="Opcao: "

if /i "%opcao%"=="I" goto instalar
if "%opcao%"=="1" goto diag
if "%opcao%"=="2" goto criar
if "%opcao%"=="3" goto popular
if "%opcao%"=="4" goto listar
if "%opcao%"=="5" goto stats
if "%opcao%"=="7" goto api
if "%opcao%"=="0" exit

echo Opcao invalida!
timeout /t 2 >nul
goto menu

:instalar
cls
echo Instalando dependencias...
echo.
python -m pip install sqlalchemy fastapi uvicorn pydantic pymysql
echo.
echo Concluido!
pause
goto menu

:diag
cls
python --version
echo.
cd
echo.
dir /B manage_catalogo.py
echo.
pause
goto menu

:criar
cls
echo Criando tabela...
echo.
python migrations\create_servicos_table.py
echo.
pause
goto menu

:popular
cls
echo IMPORTANTE: Ajuste os IDs em app\seeds\seed_servicos.py
echo.
pause
echo.
echo Populando...
echo.
python -c "from app.seeds.seed_servicos import seed_servicos; seed_servicos()"
echo.
pause
goto menu

:listar
cls
python manage_catalogo.py listar
pause
goto menu

:stats
cls
python manage_catalogo.py stats
pause
goto menu

:api
cls
echo Iniciando API em http://localhost:8000
echo Docs em http://localhost:8000/docs
echo.
echo Pressione CTRL+C para parar
echo.
uvicorn main:app --reload
pause
goto menu
