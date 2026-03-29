# ========================================
# Script de Instalação Automatizada - Windows
# Sistema de Zeladoria Urbana - Belém/PA
# Versão: 2.0.0
# ========================================

# Configurar política de execução se necessário
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Cores para output
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
Write-Host "║   Instalação Automatizada v2.0.0                     ║" -ForegroundColor Blue
Write-Host "║                                                       ║" -ForegroundColor Blue
Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Verificar Python
Write-Info "Verificando Python..."
try {
    $pythonVersion = (python --version 2>&1) -replace "Python ", ""
    Write-Success "Python $pythonVersion encontrado"
} catch {
    Write-Error-Custom "Python 3 não encontrado. Por favor, instale Python 3.8+"
    Write-Host "Download: https://www.python.org/downloads/"
    exit 1
}

# Verificar pip
Write-Info "Verificando pip..."
try {
    $pipVersion = (pip --version 2>&1)
    Write-Success "pip encontrado"
} catch {
    Write-Error-Custom "pip não encontrado. Instalando..."
    python -m ensurepip --upgrade
}

# Criar ambiente virtual
Write-Info "Criando ambiente virtual..."
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Success "Ambiente virtual criado"
} else {
    Write-Warning-Custom "Ambiente virtual já existe"
}

# Ativar ambiente virtual
Write-Info "Ativando ambiente virtual..."
& ".\venv\Scripts\Activate.ps1"
Write-Success "Ambiente virtual ativado"

# Instalar dependências
Write-Info "Instalando dependências Python..."
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Success "Dependências instaladas"

# Criar diretórios necessários
Write-Info "Criando estrutura de diretórios..."
@("uploads", "logs", "backups") | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ | Out-Null
    }
}
Write-Success "Diretórios criados"

# Configurar .env
Write-Info "Configurando arquivo .env..."
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Success "Arquivo .env criado a partir do .env.example"
        Write-Warning-Custom "IMPORTANTE: Edite o arquivo .env com suas configurações!"
    } else {
        # Gerar SECRET_KEY
        $secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
        
        @"
# Configurações do Banco de Dados
DATABASE_URL=sqlite:///./zeladoria.db

# Segurança
SECRET_KEY=$secretKey

# API
API_URL=http://localhost:8001

# Ambiente
ENVIRONMENT=development
DEBUG=True

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8001

# Uploads
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=5242880

# Logs
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Success "Arquivo .env criado com configurações padrão"
    }
} else {
    Write-Warning-Custom "Arquivo .env já existe, mantendo configurações atuais"
}

# Inicializar banco de dados
Write-Info "Inicializando banco de dados..."
if (-not (Test-Path "zeladoria.db")) {
    python -c @"
from app.database import engine, Base
from app.models import *
Base.metadata.create_all(bind=engine)
print('Banco de dados criado com sucesso!')
"@
    Write-Success "Banco de dados criado"
} else {
    Write-Warning-Custom "Banco de dados já existe"
}

# Popular dados de teste
$populate = Read-Host "Deseja popular o banco com dados de teste? (s/n)"
if ($populate -eq "s" -or $populate -eq "S") {
    Write-Info "Populando banco de dados..."
    python seed.py
    Write-Success "Dados de teste inseridos"
}

# Verificar Node.js (opcional)
Write-Info "Verificando Node.js..."
try {
    $nodeVersion = (node --version 2>&1)
    Write-Success "Node.js $nodeVersion encontrado"
    
    if (Test-Path "frontend-react") {
        Write-Info "Instalando dependências do frontend..."
        Set-Location "frontend-react"
        npm install
        Set-Location ".."
        Write-Success "Dependências do frontend instaladas"
    }
} catch {
    Write-Warning-Custom "Node.js não encontrado (opcional para frontend React)"
}

# Criar script de inicialização
Write-Info "Criando script de inicialização..."
@"
# Script de Inicialização - Windows
Write-Host "🚀 Iniciando Sistema de Zeladoria Urbana..." -ForegroundColor Blue

# Ativar ambiente virtual
& ".\venv\Scripts\Activate.ps1"

# Iniciar backend
Write-Host "📡 Iniciando backend na porta 8001..." -ForegroundColor Cyan
Start-Process python -ArgumentList "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8001" -NoNewWindow

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  Sistema de Zeladoria Urbana - Pronto!        ║" -ForegroundColor Green
Write-Host "╠════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "║                                                ║" -ForegroundColor Green
Write-Host "║  🌐 Frontend: http://localhost:8001/static/   ║" -ForegroundColor Green
Write-Host "║  📡 API: http://localhost:8001/api            ║" -ForegroundColor Green
Write-Host "║  📚 Docs: http://localhost:8001/docs          ║" -ForegroundColor Green
Write-Host "║                                                ║" -ForegroundColor Green
Write-Host "║  👤 Login de Teste (Gestor):                  ║" -ForegroundColor Green
Write-Host "║  Email: maria.santos@belem.pa.gov.br          ║" -ForegroundColor Green
Write-Host "║  Senha: senha123                              ║" -ForegroundColor Green
Write-Host "║                                                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow

# Aguardar
Read-Host "Pressione Enter para sair"
"@ | Out-File -FilePath "start.ps1" -Encoding UTF8

Write-Success "Script de inicialização criado (start.ps1)"

# Criar script de parada
Write-Info "Criando script de parada..."
@"
# Script de Parada - Windows
Write-Host "🛑 Parando Sistema de Zeladoria Urbana..." -ForegroundColor Yellow

# Parar processo uvicorn
Get-Process | Where-Object {`$_.ProcessName -like "*python*" -and `$_.CommandLine -like "*uvicorn*"} | Stop-Process -Force

Write-Host "✅ Backend parado" -ForegroundColor Green
"@ | Out-File -FilePath "stop.ps1" -Encoding UTF8

Write-Success "Script de parada criado (stop.ps1)"

# Criar script de backup
Write-Info "Criando script de backup..."
@"
# Script de Backup - Windows
`$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
`$backupDir = "backups"
`$backupFile = "`$backupDir\zeladoria_backup_`$timestamp.zip"

Write-Host "💾 Criando backup..." -ForegroundColor Blue

# Criar diretório se não existir
if (-not (Test-Path `$backupDir)) {
    New-Item -ItemType Directory -Path `$backupDir | Out-Null
}

# Fazer backup
Compress-Archive -Path zeladoria.db, .env, uploads, logs -DestinationPath `$backupFile -Force

if (`$?) {
    Write-Host "✅ Backup criado: `$backupFile" -ForegroundColor Green
    
    # Manter apenas os últimos 7 backups
    Get-ChildItem `$backupDir -Filter "zeladoria_backup_*.zip" | 
        Sort-Object CreationTime -Descending | 
        Select-Object -Skip 7 | 
        Remove-Item -Force
    
    Write-Host "🗑️  Backups antigos removidos (mantidos últimos 7)" -ForegroundColor Yellow
} else {
    Write-Host "❌ Erro ao criar backup" -ForegroundColor Red
    exit 1
}
"@ | Out-File -FilePath "backup.ps1" -Encoding UTF8

Write-Success "Script de backup criado (backup.ps1)"

# Testes básicos
Write-Info "Executando testes básicos..."
try {
    python -c @"
from app.main import app
from app.database import engine
from app.models import Usuario, Chamado, Categoria
print('✅ Todos os módulos importados com sucesso')
"@
    Write-Success "Testes básicos passaram"
} catch {
    Write-Error-Custom "Testes básicos falharam"
    exit 1
}

# Resumo final
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                        ║" -ForegroundColor Green
Write-Host "║  ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!                 ║" -ForegroundColor Green
Write-Host "║                                                        ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Info "Próximos passos:"
Write-Host ""
Write-Host "  1. Edite o arquivo .env se necessário"
Write-Host "  2. Execute: .\start.ps1"
Write-Host "  3. Acesse: http://localhost:8001/static/index.html"
Write-Host "  4. Login: maria.santos@belem.pa.gov.br / senha123"
Write-Host ""

Write-Info "Scripts disponíveis:"
Write-Host "  • .\start.ps1  - Iniciar o sistema"
Write-Host "  • .\stop.ps1   - Parar o sistema"
Write-Host "  • .\backup.ps1 - Fazer backup manual"
Write-Host ""

Write-Info "Documentação:"
Write-Host "  • INDEX.md - Índice da documentação"
Write-Host "  • QUICK_REFERENCE.md - Referência rápida"
Write-Host "  • RESUMO_CONSOLIDADO.md - Visão geral completa"
Write-Host ""

Write-Host "🎉 Sistema pronto para uso!" -ForegroundColor Blue
Write-Host ""

# Pausar para ler
Read-Host "Pressione Enter para finalizar"
