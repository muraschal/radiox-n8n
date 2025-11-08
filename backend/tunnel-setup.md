# Cloudflare Tunnel Setup für RadioX Backend

## Installation

### Windows
1. Lade cloudflared herunter: https://github.com/cloudflare/cloudflared/releases
2. Oder mit Chocolatey: `choco install cloudflared`
3. Oder mit Scoop: `scoop install cloudflared`

### Alternative: Quick Install (Windows)
```powershell
# Download und Install
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "$env:TEMP\cloudflared.exe"
Move-Item "$env:TEMP\cloudflared.exe" "$env:LOCALAPPDATA\cloudflared\cloudflared.exe" -Force
$env:Path += ";$env:LOCALAPPDATA\cloudflared"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)
```

## Schnellstart (Ohne Cloudflare Account - Quick Tunnel)

Für schnelles Testen ohne Cloudflare Account:

```bash
cloudflared tunnel --url http://localhost:8000
```

Dies erstellt einen temporären Tunnel (24h gültig) und gibt eine URL aus wie:
`https://random-name.trycloudflare.com`

## Permanenter Tunnel (Mit Cloudflare Account)

### 1. Login
```bash
cloudflared tunnel login
```
Öffnet Browser für Cloudflare Login.

### 2. Tunnel erstellen
```bash
cloudflared tunnel create radiox-backend
```

### 3. Route konfigurieren
```bash
cloudflared tunnel route dns radiox-backend backend.yourdomain.com
```

### 4. Config-Datei erstellen
Erstelle `~/.cloudflared/config.yml`:
```yaml
tunnel: <tunnel-id>
credentials-file: C:\Users\<user>\.cloudflared\<tunnel-id>.json

ingress:
  - hostname: backend.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
```

### 5. Tunnel starten
```bash
cloudflared tunnel run radiox-backend
```

## Für RadioX: Quick Tunnel Script

Für MVP verwenden wir den Quick Tunnel (ohne Account):

```bash
cd backend
.\start-tunnel.ps1
```
