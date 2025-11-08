# RadioX n8n Workflows

## 📦 Workflow Import

### RadioX Show Generation

**Datei**: `radiox-show-workflow.json`

Vollständiger Workflow für die Generierung einer Radioshow:
1. Content Generation (GPT)
2. Audio Generation (ElevenLabs)
3. Audio Download & Save

### Import in n8n

1. Gehe zu [n8n.zvv.dev](https://n8n.zvv.dev)
2. Klicke auf **"Workflows"** → **"Import from File"**
3. Wähle `radiox-show-workflow.json`
4. **WICHTIG**: Passe die Backend URL an:
   - Öffne Node "Generate Content"
   - Ersetze `https://your-tunnel-url.trycloudflare.com` mit deiner Cloudflare Tunnel URL
   - Wiederhole für "Generate Audio" und "Download Audio"

### Environment Variable (Optional)

Du kannst auch eine Environment Variable in n8n setzen:
- **Name**: `BACKEND_URL`
- **Value**: `https://deine-tunnel-url.trycloudflare.com`

Dann werden die URLs automatisch verwendet.

### Workflow verwenden

1. Klicke auf **"Execute Workflow"** (Play Button)
2. Optional: Parameter anpassen:
   - `topic`: Thema der Show
   - `duration`: Dauer in Sekunden
   - `style`: Stil (cyberpunk, gta, etc.)
3. Workflow läuft durch alle Schritte
4. Audio-Datei wird gespeichert

## 🔧 Anpassungen

### Backend URL ändern

In jedem HTTP Request Node:
- URL Feld: Ersetze `your-tunnel-url` mit deiner URL
- Oder verwende Environment Variable `BACKEND_URL`

### Parameter anpassen

Im "Generate Content" Node:
- `topic`: Ändere das Thema
- `duration`: Ändere die Dauer (in Sekunden)
- `style`: Ändere den Stil

### Audio Format ändern

Im "Transform for ElevenLabs" Node:
- Ändere `output_format` von `mp3` zu `wav` oder anderen Formaten

## 🐛 Troubleshooting

### Backend nicht erreichbar
- Prüfe ob Backend läuft: `http://localhost:8000/health`
- Prüfe Cloudflare Tunnel URL
- Teste URL im Browser

### Fehler in Workflow
- Prüfe Logs in jedem Node
- Prüfe ob alle URLs korrekt sind
- Prüfe ob Body-Format JSON ist

### Audio wird nicht generiert
- Prüfe ElevenLabs API Key im Backend
- Prüfe ob Voice ID korrekt ist
- Prüfe Backend Logs

