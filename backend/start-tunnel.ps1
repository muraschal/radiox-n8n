# Cloudflare Tunnel Start Script für RadioX Backend
# Erstellt einen Quick Tunnel (24h gültig) ohne Cloudflare Account

Write-Host "🚇 Starting Cloudflare Tunnel für RadioX Backend..." -ForegroundColor Cyan

# Prüfe ob cloudflared installiert ist
$cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue

if (-not $cloudflared) {
    Write-Host "❌ cloudflared nicht gefunden!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installation:" -ForegroundColor Yellow
    Write-Host "1. Download: https://github.com/cloudflare/cloudflared/releases/latest" -ForegroundColor White
    Write-Host "2. Oder mit Chocolatey: choco install cloudflared" -ForegroundColor White
    Write-Host "3. Oder mit Scoop: scoop install cloudflared" -ForegroundColor White
    Write-Host ""
    Write-Host "Quick Install (PowerShell als Admin):" -ForegroundColor Yellow
    Write-Host 'Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "$env:LOCALAPPDATA\cloudflared\cloudflared.exe"' -ForegroundColor Gray
    exit 1
}

# Prüfe ob Backend läuft
Write-Host "🔍 Prüfe ob Backend auf Port 8000 läuft..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Backend läuft!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend läuft nicht auf Port 8000!" -ForegroundColor Red
    Write-Host "   Starte zuerst den Backend-Server:" -ForegroundColor Yellow
    Write-Host "   python main.py" -ForegroundColor White
    exit 1
}

# Starte Tunnel
Write-Host ""
Write-Host "🌐 Starte Cloudflare Tunnel..." -ForegroundColor Cyan
Write-Host "   Backend URL wird öffentlich verfügbar sein" -ForegroundColor Gray
Write-Host "   Tunnel ist 24 Stunden gültig" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  WICHTIG: Kopiere die URL die jetzt erscheint!" -ForegroundColor Yellow
Write-Host "   Diese URL musst du in n8n verwenden!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Drücke Ctrl+C zum Beenden" -ForegroundColor Gray
Write-Host ""

# Starte cloudflared
cloudflared tunnel --url http://localhost:8000

