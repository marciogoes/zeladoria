@echo off

for /f "tokens=1-4 delims=/:. " %%a in ("%date% %time%") do (
    set TIMESTAMP=%%a%%b%%c_%%d
)
set BACKUP_DIR=backups
set BACKUP_FILE=%BACKUP_DIR%\zeladoria_backup_%TIMESTAMP%.zip

echo [INFO] Criando backup...

if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

powershell -command "Compress-Archive -Path zeladoria.db,.env,uploads,logs -DestinationPath '%BACKUP_FILE%' -Force"

if %errorlevel% equ 0 (
    echo [OK] Backup criado: %BACKUP_FILE%
) else (
    echo [ERRO] Erro ao criar backup
)

pause
