Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "POPULANDO BANCO DE DADOS - ZELADORIA BELEM/PA" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

python popular_banco.py

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PROCESSO CONCLUIDO!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pressione qualquer tecla para fechar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
