# Cloudflare Tunnel Start Script mit automatischem Backend-Check
# Erstellt einen Quick Tunnel (24h gültig) ohne Cloudflare Account

Write-Host "🚇 RadioX Backend Tunnel Setup" -ForegroundColor Cyan
Write-Host ""

# Prüfe ob cloudflared installiert ist
$cloudflaredPath = "$env:LOCALAPPDATA\cloudflared\cloudflared.exe"
if (-not (Test-Path $cloudflaredPath)) {
    Write-Host "📥 Installiere cloudflared..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path "$env:LOCALAPPDATA\cloudflared" | Out-Null
    Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile $cloudflaredPath
    Write-Host "✅ cloudflared installiert!" -ForegroundColor Green
}

# Füge cloudflared zum PATH hinzu (für diese Session)
$env:Path += ";$env:LOCALAPPDATA\cloudflared"

# Prüfe ob Backend läuft
Write-Host "🔍 Prüfe Backend..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Backend läuft auf Port 8000!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend läuft nicht auf Port 8000!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Starte Backend in einem neuen Terminal:" -ForegroundColor Yellow
    Write-Host "  cd backend" -ForegroundColor White
    Write-Host "  python -m uvicorn main:app --host 0.0.0.0 --port 8000" -ForegroundColor White
    Write-Host ""
    Write-Host "Dann starte dieses Script erneut." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🌐 Starte Cloudflare Tunnel..." -ForegroundColor Cyan
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "⚠️  WICHTIG: Kopiere die URL die jetzt erscheint!" -ForegroundColor Yellow
Write-Host "   Diese URL musst du in n8n verwenden!" -ForegroundColor Yellow
Write-Host "   Format: https://xxxxx.trycloudflare.com" -ForegroundColor Gray
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "Drücke Ctrl+C zum Beenden" -ForegroundColor Gray
Write-Host ""

# Starte cloudflared
& $cloudflaredPath tunnel --url http://localhost:8000

