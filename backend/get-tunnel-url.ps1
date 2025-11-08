# Script zum Finden der Cloudflare Tunnel URL
Write-Host "🔍 Cloudflare Tunnel URL Finder" -ForegroundColor Cyan
Write-Host ""

# Prüfe ob Tunnel läuft
$tunnel = Get-Process cloudflared -ErrorAction SilentlyContinue
if (-not $tunnel) {
    Write-Host "❌ Cloudflare Tunnel läuft NICHT!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Starte den Tunnel mit:" -ForegroundColor Yellow
    Write-Host "  cd backend" -ForegroundColor White
    Write-Host "  .\start-tunnel-with-backend.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "Die URL wird dann im Terminal angezeigt!" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Cloudflare Tunnel läuft (PID: $($tunnel.Id))" -ForegroundColor Green
Write-Host ""
Write-Host "📋 So findest du die URL:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Öffne das Terminal wo cloudflared läuft" -ForegroundColor White
Write-Host "2. Suche nach einer Zeile wie:" -ForegroundColor White
Write-Host "   'https://xxxxx-xxxxx.trycloudflare.com'" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Kopiere diese URL" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Die URL sieht so aus:" -ForegroundColor Yellow
Write-Host "   https://abc123-def456.trycloudflare.com" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Tipp: Die URL wird direkt nach dem Start angezeigt!" -ForegroundColor Cyan

