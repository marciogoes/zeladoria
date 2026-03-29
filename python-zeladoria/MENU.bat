@echo off
title CATALOGO DE SERVICOS - Menu Principal
color 0B

:inicio
cls
echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║                                                          ║
echo  ║     CATALOGO DE SERVICOS - ZELADORIA BELEM               ║
echo  ║                                                          ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.
echo  PRIMEIRA VEZ? INSTALE AS DEPENDENCIAS:
echo  ════════════════════════════════════════════════════════
echo  [I] Instalar Dependencias (SQLAlchemy, FastAPI, etc)
echo.
echo  SETUP INICIAL (Execute uma vez):
echo  ════════════════════════════════════════════════════════
echo  [1] Diagnostico do Sistema
echo  [2] Criar Tabela no Banco
echo  [3] Popular com 100+ Servicos
echo.
echo  USO DIARIO:
echo  ════════════════════════════════════════════════════════
echo  [4] Listar Servicos
echo  [5] Ver Estatisticas  
echo  [6] Menu Python Completo
echo.
echo  API:
echo  ════════════════════════════════════════════════════════
echo  [7] Iniciar Servidor API
echo.
echo  [0] Sair
echo.
echo  ════════════════════════════════════════════════════════
echo.

set /p opcao="  Digite sua opcao e pressione ENTER: "

if /i "%opcao%"=="I" goto instalar
if "%opcao%"=="1" goto diagnostico
if "%opcao%"=="2" goto criar_tabela
if "%opcao%"=="3" goto popular
if "%opcao%"=="4" goto listar
if "%opcao%"=="5" goto stats
if "%opcao%"=="6" goto menu_python
if "%opcao%"=="7" goto api
if "%opcao%"=="0" goto sair

echo.
echo  OPCAO INVALIDA! Tente novamente...
timeout /t 2 >nul
goto inicio

:instalar
cls
echo.
echo  ══════════════════════════════════════════════════════════
echo   INSTALAR DEPENDENCIAS
echo  ══════════════════════════════════════════════════════════
echo.
if exist INSTALAR_DEPENDENCIAS.bat (
    call INSTALAR_DEPENDENCIAS.bat
) else (
    echo Instalando dependencias...
    echo.
    pip install sqlalchemy fastapi uvicorn pydantic pymysql
    echo.
    echo Instalacao concluida!
    echo.
    pause
)
goto inicio

:diagnostico
cls
echo.
echo  Executando diagnostico...
echo.
if exist DIAGNOSTICO.bat (
    call DIAGNOSTICO.bat
) else (
    python --version
    echo.
    cd
    echo.
    pause
)
goto inicio

:criar_tabela
cls
echo.
echo  ══════════════════════════════════════════════════════════
echo   CRIAR TABELA NO BANCO
echo  ══════════════════════════════════════════════════════════
echo.
echo  Criando tabela servicos_secretaria...
echo.
python migrations\create_servicos_table.py
echo.
echo  Pressione qualquer tecla para voltar ao menu...
pause >nul
goto inicio

:popular
cls
echo.
echo  ══════════════════════════════════════════════════════════
echo   POPULAR BANCO COM SERVICOS
echo  ══════════════════════════════════════════════════════════
echo.
echo  ATENCAO: Ajuste os IDs em app\seeds\seed_servicos.py
echo.
echo  Pressione qualquer tecla para continuar...
pause >nul
echo.
echo  Populando banco...
echo.
python -c "from app.seeds.seed_servicos import seed_servicos; seed_servicos()"
echo.
echo  Pressione qualquer tecla para voltar ao menu...
pause >nul
goto inicio

:listar
cls
echo.
echo  ══════════════════════════════════════════════════════════
echo   LISTAR SERVICOS
echo  ══════════════════════════════════════════════════════════
echo.
python manage_catalogo.py listar
echo.
echo  Pressione qualquer tecla para voltar ao menu...
pause >nul
goto inicio

:stats
cls
echo.
echo  ══════════════════════════════════════════════════════════
echo   ESTATISTICAS
echo  ══════════════════════════════════════════════════════════
echo.
python manage_catalogo.py stats
echo.
echo  Pressione qualquer tecla para voltar ao menu...
pause >nul
goto inicio

:menu_python
cls
python manage_catalogo.py
goto inicio

:api
cls
echo.
echo  ══════════════════════════════════════════════════════════
echo   INICIAR SERVIDOR API
echo  ══════════════════════════════════════════════════════════
echo.
echo  Servidor sera iniciado em: http://localhost:8000
echo  Documentacao em: http://localhost:8000/docs
echo.
echo  Pressione CTRL+C para parar o servidor
echo.
uvicorn main:app --reload
pause
goto inicio

:sair
cls
echo.
echo  Ate logo!
echo.
timeout /t 1 >nul
exit
