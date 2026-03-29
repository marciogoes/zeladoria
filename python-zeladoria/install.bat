@echo off
REM ============================================
REM Script de Instalacao - Windows BAT
REM Sistema de Zeladoria Urbana - Belem/PA
REM Versao: 2.0.2 (Simplificado)
REM ============================================

echo.
echo ========================================================
echo    Sistema de Zeladoria Urbana - Belem/PA
echo    Instalacao Automatizada v2.0.2
echo ========================================================
echo.

REM Verificar Python
echo [INFO] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python 3 nao encontrado!
    echo.
    echo Por favor, instale Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo Certifique-se de marcar "Add Python to PATH"!
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% encontrado

REM Verificar pip
echo [INFO] Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] pip nao encontrado. Instalando...
    python -m ensurepip --upgrade
)
echo [OK] pip encontrado

REM Criar ambiente virtual
echo [INFO] Criando ambiente virtual...
if not exist "venv" (
    python -m venv venv
    echo [OK] Ambiente virtual criado
) else (
    echo [INFO] Ambiente virtual ja existe
)

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Erro ao ativar ambiente virtual
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado

REM Instalar dependencias
echo [INFO] Instalando dependencias Python...
echo [INFO] Isso pode demorar alguns minutos...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo [OK] Dependencias instaladas

REM Criar diretorios
echo [INFO] Criando estrutura de diretorios...
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
echo [OK] Diretorios criados

REM Configurar .env
echo [INFO] Configurando arquivo .env...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo [OK] Arquivo .env criado a partir do .env.example
        echo [AVISO] IMPORTANTE: Edite o arquivo .env!
    ) else (
        (
            echo # Configuracoes do Banco de Dados
            echo DATABASE_URL=sqlite:///./zeladoria.db
            echo.
            echo # Seguranca
            echo SECRET_KEY=sua-chave-secreta-mude-em-producao
            echo.
            echo # API
            echo API_URL=http://localhost:8001
            echo.
            echo # Ambiente
            echo ENVIRONMENT=development
            echo DEBUG=True
            echo.
            echo # CORS
            echo ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8001
            echo.
            echo # Uploads
            echo UPLOAD_DIR=./uploads
            echo MAX_UPLOAD_SIZE=5242880
            echo.
            echo # Logs
            echo LOG_LEVEL=INFO
            echo LOG_FILE=./logs/app.log
        ) > .env
        echo [OK] Arquivo .env criado com configuracoes padrao
    )
) else (
    echo [INFO] Arquivo .env ja existe
)

REM Inicializar banco de dados
echo [INFO] Inicializando banco de dados...
if not exist "zeladoria.db" (
    python -c "from app.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine); print('[OK] Banco criado')"
    echo [OK] Banco de dados criado
) else (
    echo [INFO] Banco de dados ja existe
)

REM Popular dados de teste
set /p POPULATE="Deseja popular o banco com dados de teste? (s/n): "
if /i "%POPULATE%"=="s" (
    echo [INFO] Populando banco de dados...
    python seed.py
    echo [OK] Dados de teste inseridos
)

REM Criar scripts auxiliares
echo [INFO] Criando scripts auxiliares...

REM Script start.bat
(
echo @echo off
echo echo Iniciando Sistema de Zeladoria Urbana...
echo.
echo call venv\Scripts\activate.bat
echo.
echo echo [INFO] Iniciando backend na porta 8001...
echo start /B python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
echo.
echo timeout /t 3 /nobreak ^>nul
echo.
echo echo.
echo echo ========================================================
echo echo    Sistema de Zeladoria Urbana - Pronto!
echo echo ========================================================
echo echo.
echo echo  Frontend: http://localhost:8001/static/
echo echo  API: http://localhost:8001/api
echo echo  Docs: http://localhost:8001/docs
echo echo.
echo echo  Login de Teste ^(Gestor^):
echo echo  Email: maria.santos@belem.pa.gov.br
echo echo  Senha: senha123
echo echo.
echo echo ========================================================
echo echo.
echo echo Pressione Ctrl+C para parar o servidor
echo.
echo pause
) > start.bat

REM Script stop.bat
(
echo @echo off
echo echo Parando Sistema de Zeladoria Urbana...
echo.
echo taskkill /F /IM python.exe ^>nul 2^>^&1
echo.
echo echo [OK] Backend parado
echo pause
) > stop.bat

REM Script backup.bat
(
echo @echo off
echo.
echo for /f "tokens=1-4 delims=/:. " %%%%a in ^("%%date%% %%time%%"^) do ^(
echo     set TIMESTAMP=%%%%a%%%%b%%%%c_%%%%d
echo ^)
echo set BACKUP_DIR=backups
echo set BACKUP_FILE=%%BACKUP_DIR%%\zeladoria_backup_%%TIMESTAMP%%.zip
echo.
echo echo [INFO] Criando backup...
echo.
echo if not exist %%BACKUP_DIR%% mkdir %%BACKUP_DIR%%
echo.
echo powershell -command "Compress-Archive -Path zeladoria.db,.env,uploads,logs -DestinationPath '%%BACKUP_FILE%%' -Force"
echo.
echo if %%errorlevel%% equ 0 ^(
echo     echo [OK] Backup criado: %%BACKUP_FILE%%
echo ^) else ^(
echo     echo [ERRO] Erro ao criar backup
echo ^)
echo.
echo pause
) > backup.bat

echo [OK] Scripts criados: start.bat, stop.bat, backup.bat

REM Testes basicos
echo [INFO] Executando testes basicos...
python -c "from app.main import app; from app.database import engine; from app.models import Usuario, Chamado, Categoria; print('[OK] Modulos OK')" 2>nul
if errorlevel 1 (
    echo [AVISO] Testes basicos falharam
) else (
    echo [OK] Testes basicos passaram
)

REM Resumo final
echo.
echo ========================================================
echo    INSTALACAO CONCLUIDA COM SUCESSO!
echo ========================================================
echo.

echo [INFO] Proximos passos:
echo.
echo   1. Edite o arquivo .env se necessario
echo   2. Execute: start.bat
echo   3. Acesse: http://localhost:8001/static/index.html
echo   4. Login: maria.santos@belem.pa.gov.br / senha123
echo.

echo [INFO] Scripts disponiveis:
echo   - start.bat   (Iniciar o sistema)
echo   - stop.bat    (Parar o sistema)
echo   - backup.bat  (Fazer backup manual)
echo.

set /p START="Deseja iniciar o servidor agora? (s/n): "
if /i "%START%"=="s" (
    echo.
    echo Iniciando servidor...
    call start.bat
) else (
    echo.
    echo Execute start.bat quando estiver pronto!
)

pause
