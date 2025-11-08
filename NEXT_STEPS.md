# 🎯 Nächste Schritte - Erste Radioshow in 30 Min

## ✅ Was bereits fertig ist:

1. **Backend API** läuft auf `http://localhost:8000`
   - ✅ GPT Content Generation Endpoint
   - ✅ ElevenLabs TTS Endpoint
   - ✅ Health Check

2. **Cloudflare Tunnel** (falls gestartet)
   - Öffentliche URL für n8n Zugriff

## 🚀 Jetzt: n8n Workflow erstellen

### Schritt 1: n8n öffnen
Gehe zu: **[n8n.zvv.dev](https://n8n.zvv.dev)**

### Schritt 2: Neuen Workflow erstellen

1. Klicke auf **"New Workflow"**
2. Benenne ihn: `RadioX - Erste Show`

### Schritt 3: Workflow aufbauen

#### Node 1: Manual Trigger
- **Type**: `Manual Trigger`
- **Name**: `Start Show`

#### Node 2: Generate Content
- **Type**: `HTTP Request`
- **Name**: `Generate Content`
- **Method**: `POST`
- **URL**: `https://deine-tunnel-url.trycloudflare.com/api/generate-content`
  - ⚠️ **WICHTIG**: Ersetze `deine-tunnel-url` mit deiner Cloudflare Tunnel URL!
- **Authentication**: `None`
- **Body Content Type**: `JSON`
- **Body**:
```json
{
  "topic": "Tech News",
  "duration": 300,
  "style": "cyberpunk"
}
```

#### Node 3: Transform Content
- **Type**: `Code`
- **Name**: `Transform for ElevenLabs`
- **Language**: `JavaScript`
- **Code**:
```javascript
const content = $input.item.json.content;
const speaker = $input.item.json.speaker || 'marcel';

return {
  text: content,
  voice_id: speaker,
  output_format: 'mp3'
};
```

#### Node 4: Generate Audio
- **Type**: `HTTP Request`
- **Name**: `Generate Audio`
- **Method**: `POST`
- **URL**: `https://deine-tunnel-url.trycloudflare.com/api/generate-audio`
- **Authentication**: `None`
- **Body Content Type**: `JSON`
- **Body**: `{{ $json }}`

#### Node 5: Get Audio File
- **Type**: `HTTP Request`
- **Name**: `Download Audio`
- **Method**: `GET`
- **URL**: `https://deine-tunnel-url.trycloudflare.com{{ $json.file_path }}`
- **Response Format**: `File`

#### Node 6: Save Audio (Optional)
- **Type**: `Write Binary File`
- **Name**: `Save Audio`
- **File Name**: `radiox-show-{{ $now.format('YYYY-MM-DD-HHmmss') }}.mp3`
- **File Path**: `/tmp/` (oder dein gewünschter Pfad)

### Schritt 4: Workflow verbinden

Verbinde die Nodes in dieser Reihenfolge:
```
Manual Trigger → Generate Content → Transform → Generate Audio → Download Audio → Save Audio
```

### Schritt 5: Testen

1. Klicke auf **"Execute Workflow"** (Play Button)
2. Prüfe die Ausgabe jedes Nodes
3. Audio-Datei sollte generiert werden!

## 🔍 Troubleshooting

### Backend nicht erreichbar?
- Prüfe ob Backend läuft: `http://localhost:8000/health`
- Prüfe Cloudflare Tunnel URL
- Teste URL im Browser: `https://deine-url.trycloudflare.com/health`

### Fehler in n8n?
- Prüfe ob alle URLs korrekt sind
- Prüfe ob Body-Format JSON ist
- Prüfe Logs in jedem Node

### Audio wird nicht generiert?
- Prüfe ElevenLabs API Key im Backend
- Prüfe ob Voice ID korrekt ist
- Prüfe Backend Logs

## 📝 Workflow Export

Nach erfolgreichem Test:
1. Klicke auf **"Save"**
2. Export als JSON: **"Download"** → **"Download as File"**
3. Speichere in `workflows/radiox-first-show.json`

## 🎉 Success!

Wenn alles funktioniert:
- ✅ Content wird generiert
- ✅ Audio wird erstellt
- ✅ Audio-Datei ist abspielbar
- ✅ Workflow ist wiederholbar

**Dann hast du deine erste Radioshow in 30 Minuten! 🚀**

