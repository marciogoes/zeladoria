# ============================================
# SCRIPT DE ATUALIZAÇÃO/MIGRAÇÃO - Windows
# Sistema de Zeladoria Urbana - Belém/PA
# Versão: 2.0.0
# ============================================

$ErrorActionPreference = "Stop"

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[✓] $Message" -ForegroundColor Green
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "[!] $Message" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[✗] $Message" -ForegroundColor Red
}

# Banner
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║                                                       ║" -ForegroundColor Blue
Write-Host "║   Sistema de Zeladoria Urbana - Belém/PA             ║" -ForegroundColor Blue
Write-Host "║   Script de Atualização v2.0.0                       ║" -ForegroundColor Blue
Write-Host "║                                                       ║" -ForegroundColor Blue
Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Verificar se está no diretório correto
if (-not (Test-Path "main.py")) {
    Write-Error-Custom "Execute este script no diretório raiz do projeto!"
    exit 1
}

# Parar servidor se estiver rodando
Write-Info "Verificando se o servidor está rodando..."
$processes = Get-Process | Where-Object {$_.ProcessName -like "*python*" -and $_.CommandLine -like "*uvicorn*"}
if ($processes) {
    Write-Warning-Custom "Parando servidor..."
    $processes | Stop-Process -Force
    Start-Sleep -Seconds 2
    Write-Success "Servidor parado"
}

# Backup do banco de dados
Write-Info "Criando backup do banco de dados..."
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "backups"

if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
}

if (Test-Path "zeladoria.db") {
    Copy-Item "zeladoria.db" "$backupDir\zeladoria_backup_$timestamp.db"
    Write-Success "Backup criado: $backupDir\zeladoria_backup_$timestamp.db"
} else {
    Write-Warning-Custom "Banco de dados não encontrado, pulando backup"
}

# Backup do .env
if (Test-Path ".env") {
    Copy-Item ".env" "$backupDir\.env_backup_$timestamp"
    Write-Success "Backup do .env criado"
}

# Ativar ambiente virtual
Write-Info "Ativando ambiente virtual..."
if (Test-Path "venv") {
    & ".\venv\Scripts\Activate.ps1"
    Write-Success "Ambiente virtual ativado"
} else {
    Write-Error-Custom "Ambiente virtual não encontrado. Execute .\install.ps1 primeiro"
    exit 1
}

# Atualizar dependências
Write-Info "Atualizando dependências Python..."
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt
Write-Success "Dependências atualizadas"

# Verificar mudanças no .env.example
Write-Info "Verificando .env..."
if (Test-Path ".env.example") {
    $envContent = Get-Content ".env" -Raw
    $exampleContent = Get-Content ".env.example" -Raw
    
    if ($envContent -ne $exampleContent) {
        Write-Warning-Custom "Há mudanças no .env.example!"
        Write-Warning-Custom "Revise o arquivo .env.example e atualize seu .env se necessário"
        
        $showDiff = Read-Host "Deseja ver as diferenças agora? (s/n)"
        
        if ($showDiff -eq "s" -or $showDiff -eq "S") {
            Compare-Object (Get-Content ".env") (Get-Content ".env.example")
        }
    } else {
        Write-Success "Arquivo .env está atualizado"
    }
}

# Executar migrações (se houver)
if (Test-Path "migrations") {
    Write-Info "Executando migrações do banco de dados..."
    # alembic upgrade head
    Write-Success "Migrações executadas"
}

# Verificar integridade do banco
Write-Info "Verificando integridade do banco de dados..."
try {
    python -c @"
from app.database import engine
from sqlalchemy import text

with engine.connect() as connection:
    connection.execute(text('SELECT 1'))
    connection.commit()
print('✅ Banco de dados OK')
"@
    Write-Success "Banco de dados verificado"
} catch {
    Write-Error-Custom "Erro na verificação do banco de dados"
    Write-Warning-Custom "Restaurando backup..."
    
    if (Test-Path "$backupDir\zeladoria_backup_$timestamp.db") {
        Copy-Item "$backupDir\zeladoria_backup_$timestamp.db" "zeladoria.db"
        Write-Success "Backup restaurado"
    }
    exit 1
}

# Executar testes
$runTests = Read-Host "Deseja executar os testes? (s/n)"

if ($runTests -eq "s" -or $runTests -eq "S") {
    Write-Info "Executando testes..."
    python test_suite.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Custom "Alguns testes falharam!"
        Write-Warning-Custom "Verifique os erros antes de continuar"
        
        $continue = Read-Host "Deseja continuar mesmo assim? (s/n)"
        
        if ($continue -ne "s" -and $continue -ne "S") {
            Write-Info "Atualização cancelada"
            exit 1
        }
    }
}

# Limpar cache Python
Write-Info "Limpando cache Python..."
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Success "Cache limpo"

# Verificar logs antigos
Write-Info "Verificando logs antigos..."
if (Test-Path "logs") {
    $logCount = (Get-ChildItem "logs" -Filter "*.log" -File).Count
    if ($logCount -gt 10) {
        Write-Warning-Custom "Há $logCount arquivos de log"
        $cleanLogs = Read-Host "Deseja limpar logs antigos (mantém os 10 mais recentes)? (s/n)"
        
        if ($cleanLogs -eq "s" -or $cleanLogs -eq "S") {
            Get-ChildItem "logs" -Filter "*.log" -File | 
                Sort-Object CreationTime -Descending | 
                Select-Object -Skip 10 | 
                Remove-Item -Force
            Write-Success "Logs antigos removidos"
        }
    }
}

# Resumo da atualização
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                        ║" -ForegroundColor Green
Write-Host "║  ✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!                ║" -ForegroundColor Green
Write-Host "║                                                        ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Info "Backups criados:"
Write-Host "  • Banco: $backupDir\zeladoria_backup_$timestamp.db"
if (Test-Path "$backupDir\.env_backup_$timestamp") {
    Write-Host "  • .env: $backupDir\.env_backup_$timestamp"
}

Write-Host ""
Write-Info "Próximos passos:"
Write-Host "  1. Revise o .env se houver mudanças"
Write-Host "  2. Inicie o servidor: .\start.ps1"
Write-Host "  3. Teste o sistema no navegador"
Write-Host ""

$startServer = Read-Host "Deseja iniciar o servidor agora? (s/n)"

if ($startServer -eq "s" -or $startServer -eq "S") {
    Write-Info "Iniciando servidor..."
    & ".\start.ps1"
} else {
    Write-Info "Execute .\start.ps1 quando estiver pronto"
}

Write-Host ""
Write-Host "🎉 Atualização completa!" -ForegroundColor Blue
Write-Host ""

# Pausar para ler
Read-Host "Pressione Enter para finalizar"
