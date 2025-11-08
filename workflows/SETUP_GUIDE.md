# 🎙️ RadioX Show Workflow - Schnellaufbau in n8n

## Schritt 1: n8n öffnen
Gehe zu: **[n8n.zvv.dev](https://n8n.zvv.dev)**

## Schritt 2: Neuen Workflow erstellen
1. Klicke auf **"New Workflow"**
2. Benenne ihn: `RadioX - Show Generation`

## Schritt 3: Nodes hinzufügen

### Node 1: Manual Trigger
1. Klicke auf **"+"** → Suche `Manual Trigger`
2. Name: `Start Show`
3. Fertig - keine Konfiguration nötig

### Node 2: Generate Content (HTTP Request)
1. Klicke auf **"+"** → Suche `HTTP Request`
2. Name: `Generate Content`
3. Konfiguration:
   - **Method**: `POST`
   - **URL**: `https://DEINE-TUNNEL-URL.trycloudflare.com/api/generate-content`
     - ⚠️ **WICHTIG**: Ersetze `DEINE-TUNNEL-URL` mit deiner Cloudflare Tunnel URL!
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
4. Verbinde mit `Start Show`

### Node 3: Transform Content (Code)
1. Klicke auf **"+"** → Suche `Code`
2. Name: `Transform for ElevenLabs`
3. Konfiguration:
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
4. Verbinde mit `Generate Content`

### Node 4: Generate Audio (HTTP Request)
1. Klicke auf **"+"** → Suche `HTTP Request`
2. Name: `Generate Audio`
3. Konfiguration:
   - **Method**: `POST`
   - **URL**: `https://DEINE-TUNNEL-URL.trycloudflare.com/api/generate-audio`
   - **Authentication**: `None`
   - **Body Content Type**: `JSON`
   - **Body**: `{{ $json }}`
4. Verbinde mit `Transform for ElevenLabs`

### Node 5: Download Audio (HTTP Request)
1. Klicke auf **"+"** → Suche `HTTP Request`
2. Name: `Download Audio`
3. Konfiguration:
   - **Method**: `GET`
   - **URL**: `https://DEINE-TUNNEL-URL.trycloudflare.com{{ $json.file_path }}`
   - **Authentication**: `None`
   - **Options** → **Response** → **Response Format**: `File`
4. Verbinde mit `Generate Audio`

### Node 6: Save Audio (Write Binary File) - Optional
1. Klicke auf **"+"** → Suche `Write Binary File`
2. Name: `Save Audio`
3. Konfiguration:
   - **File Name**: `radiox-show-{{ $now.format('YYYY-MM-DD-HHmmss') }}.mp3`
   - **Data Property Name**: `data`
4. Verbinde mit `Download Audio`

## Schritt 4: Workflow testen

1. Klicke auf **"Save"** (oben rechts)
2. Klicke auf **"Execute Workflow"** (Play Button)
3. Prüfe die Ausgabe jedes Nodes:
   - ✅ `Generate Content` → Sollte Content zurückgeben
   - ✅ `Transform` → Sollte formatierten Content zurückgeben
   - ✅ `Generate Audio` → Sollte Audio-Info zurückgeben
   - ✅ `Download Audio` → Sollte Audio-Datei zurückgeben
   - ✅ `Save Audio` → Sollte Datei speichern

## 🎉 Fertig!

Wenn alles funktioniert, hast du:
- ✅ Content generiert
- ✅ Audio erstellt
- ✅ Audio-Datei gespeichert

**Deine erste Radioshow ist fertig! 🚀**

## 🔧 Anpassungen

### Thema ändern
Im `Generate Content` Node → Body → `topic` ändern

### Dauer ändern
Im `Generate Content` Node → Body → `duration` ändern (in Sekunden)

### Stil ändern
Im `Generate Content` Node → Body → `style` ändern (z.B. "gta", "cyberpunk")

## 🐛 Troubleshooting

### "Backend nicht erreichbar"
- Prüfe ob Backend läuft: `http://localhost:8000/health`
- Prüfe ob Cloudflare Tunnel läuft
- Teste Tunnel-URL im Browser: `https://deine-url.trycloudflare.com/health`

### "Content Generation failed"
- Prüfe OpenAI API Key im Backend `.env`
- Prüfe Backend Logs

### "Audio Generation failed"
- Prüfe ElevenLabs API Key im Backend `.env`
- Prüfe Voice ID im Backend `.env`
- Prüfe Backend Logs

### "File not found"
- Prüfe ob `file_path` im `Generate Audio` Response korrekt ist
- Prüfe ob Backend die Datei wirklich erstellt hat

