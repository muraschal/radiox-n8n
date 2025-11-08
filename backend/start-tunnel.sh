#!/bin/bash
# Cloudflare Tunnel Start Script für RadioX Backend
# Erstellt einen Quick Tunnel (24h gültig) ohne Cloudflare Account

echo "🚇 Starting Cloudflare Tunnel für RadioX Backend..."

# Prüfe ob cloudflared installiert ist
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared nicht gefunden!"
    echo ""
    echo "Installation:"
    echo "  macOS: brew install cloudflared"
    echo "  Linux: https://github.com/cloudflare/cloudflared/releases"
    exit 1
fi

# Prüfe ob Backend läuft
echo "🔍 Prüfe ob Backend auf Port 8000 läuft..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend läuft nicht auf Port 8000!"
    echo "   Starte zuerst den Backend-Server:"
    echo "   python main.py"
    exit 1
fi

echo "✅ Backend läuft!"
echo ""
echo "🌐 Starte Cloudflare Tunnel..."
echo "   Backend URL wird öffentlich verfügbar sein"
echo "   Tunnel ist 24 Stunden gültig"
echo ""
echo "⚠️  WICHTIG: Kopiere die URL die jetzt erscheint!"
echo "   Diese URL musst du in n8n verwenden!"
echo ""
echo "Drücke Ctrl+C zum Beenden"
echo ""

# Starte cloudflared
cloudflared tunnel --url http://localhost:8000


