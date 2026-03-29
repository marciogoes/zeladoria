@echo off
REM ============================================
REM Script de Atualizacao - Windows BAT
REM Sistema de Zeladoria Urbana - Belem/PA
REM Versao: 2.0.2 (Simplificado)
REM ============================================

echo.
echo ========================================================
echo    Sistema de Zeladoria Urbana - Belem/PA
echo    Script de Atualizacao v2.0.2
echo ========================================================
echo.

REM Verificar se esta no diretorio correto
if not exist "main.py" (
    echo [ERRO] Execute este script no diretorio raiz do projeto!
    echo.
    pause
    exit /b 1
)

REM Parar servidor se estiver rodando
echo [INFO] Verificando se o servidor esta rodando...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [INFO] Parando servidor Python...
    taskkill /F /IM python.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo [OK] Servidor parado
) else (
    echo [INFO] Nenhum servidor rodando
)

REM Criar timestamp para backup
for /f "tokens=1-4 delims=/:. " %%a in ("%date% %time%") do (
    set TIMESTAMP=%%a%%b%%c_%%d
)
set BACKUP_DIR=backups

echo.
echo [INFO] Criando backups...

REM Criar diretorio de backups
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Backup do banco de dados
if exist "zeladoria.db" (
    copy "zeladoria.db" "%BACKUP_DIR%\zeladoria_backup_%TIMESTAMP%.db" >nul 2>&1
    if errorlevel 1 (
        echo [AVISO] Erro ao fazer backup do banco
    ) else (
        echo [OK] Backup do banco criado
    )
) else (
    echo [INFO] Banco de dados nao encontrado
)

REM Backup do .env
if exist ".env" (
    copy ".env" "%BACKUP_DIR%\.env_backup_%TIMESTAMP%" >nul 2>&1
    if errorlevel 1 (
        echo [AVISO] Erro ao fazer backup do .env
    ) else (
        echo [OK] Backup do .env criado
    )
)

REM Ativar ambiente virtual
echo.
echo [INFO] Ativando ambiente virtual...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Ambiente virtual ativado
) else (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo [INFO] Execute install.bat primeiro
    pause
    exit /b 1
)

REM Atualizar pip
echo.
echo [INFO] Atualizando pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip atualizado

REM Atualizar dependencias
echo.
echo [INFO] Atualizando dependencias Python...
echo [INFO] Isso pode demorar alguns minutos...
pip install --upgrade -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERRO] Erro ao atualizar dependencias
    pause
    exit /b 1
) else (
    echo [OK] Dependencias atualizadas
)

REM Verificar .env
echo.
echo [INFO] Verificando arquivo .env...
if exist ".env.example" (
    if exist ".env" (
        echo [OK] Arquivos .env encontrados
    )
)

REM Verificar integridade do banco
echo.
echo [INFO] Verificando integridade do banco de dados...
python -c "from app.database import engine; from sqlalchemy import text; conn = engine.connect(); conn.execute(text('SELECT 1')); conn.close(); print('[OK] Banco OK')" 2>nul
if errorlevel 1 (
    echo [ERRO] Erro na verificacao do banco
) else (
    echo [OK] Banco de dados verificado
)

REM Limpar cache Python
echo.
echo [INFO] Limpando cache Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
echo [OK] Cache limpo

REM Resumo
echo.
echo ========================================================
echo    ATUALIZACAO CONCLUIDA COM SUCESSO!
echo ========================================================
echo.

echo [INFO] Proximos passos:
echo   1. Revise o .env se necessario
echo   2. Inicie o servidor: start.bat
echo   3. Teste o sistema no navegador
echo.

set /p START_SERVER="Deseja iniciar o servidor agora? (s/n): "
if /i "%START_SERVER%"=="s" (
    echo.
    echo [INFO] Iniciando servidor...
    if exist "start.bat" (
        call start.bat
    ) else (
        echo [INFO] Inicie manualmente com: start.bat
    )
)

echo.
echo Atualizacao completa!
echo.
pause
