# RadioX n8n Integration - Minimaldurchstich Plan

> **Ziel**: Erste funktionierende Radioshow in 30 Minuten mit n8n-Orchestrierung

## 🎯 Projekt-Übersicht

RadioX wird auf eine **n8n-basierte Orchestrierung** umgestellt. Das Backend liefert fokussierte API-Services, während n8n die Workflow-Orchestrierung übernimmt.

**n8n Instanz**: [n8n.zvv.dev](https://n8n.zvv.dev) (bereits vorhanden)

### Architektur-Prinzip

```
┌─────────────────┐
│ n8n.zvv.dev     │  ← Orchestrierung, Scheduling, Error Handling
│   (n8n Workflow)│
└────────┬────────┘
         │ HTTP API Calls
         ↓
┌─────────────────┐
│  Backend APIs   │  ← Business Logic, Audio Processing
│  (lokal/remote) │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   Supabase DB   │  ← Datenpersistierung
└─────────────────┘
```

## 🚀 Minimaldurchstich (MVP) - 30 Minuten Plan

### Phase 1: Setup (10 Min)

#### 1.1 Backend Setup
- [ ] Minimal FastAPI Server starten
- [ ] 3 API-Endpunkte implementieren:
  - `POST /api/generate-content` - GPT Content Generation
  - `POST /api/generate-audio` - ElevenLabs TTS
  - `POST /api/stream` - Icecast Upload (optional für MVP)
- [ ] Backend muss von n8n.zvv.dev erreichbar sein (öffentliche URL oder Tunnel)

#### 1.2 n8n Setup
- [x] n8n Instanz vorhanden: [n8n.zvv.dev](https://n8n.zvv.dev)
- [ ] n8n Workflow erstellen
- [ ] Backend-URL in n8n konfigurieren
- [ ] Environment Variables in n8n setzen (API Keys)

#### 1.3 Datenbank (optional für MVP)
- [ ] Supabase Connection String
- [ ] Minimal Schema (kann später erweitert werden)

### Phase 2: n8n Workflow (15 Min)

#### 2.1 Basis-Workflow erstellen
```
[Manual Trigger] 
    ↓
[HTTP Request] → POST /api/generate-content
    ↓
[Transform Data] → Format für ElevenLabs
    ↓
[HTTP Request] → POST /api/generate-audio
    ↓
[Save to File] → Audio speichern
    ↓
[HTTP Request] → POST /api/stream (optional)
```

#### 2.2 Workflow-Konfiguration
- **Trigger**: Manual (später: Schedule/Cron)
- **Error Handling**: Retry bei Fehlern
- **Logging**: Alle Schritte loggen

### Phase 3: Test & Validierung (5 Min)

- [ ] Workflow manuell auslösen
- [ ] Content Generation testen
- [ ] Audio Generation testen
- [ ] Audio-Datei validieren

## 📋 Detaillierte Implementierung

### Backend API Endpoints (Minimal)

#### 1. Content Generation
```http
POST /api/generate-content
Content-Type: application/json

{
  "topic": "Tech News",
  "duration": 300,
  "style": "cyberpunk"
}

Response:
{
  "content": "Generated script...",
  "duration": 300,
  "speaker": "marcel"
}
```

#### 2. Audio Generation
```http
POST /api/generate-audio
Content-Type: application/json

{
  "text": "Generated script...",
  "voice_id": "marcel",
  "output_format": "mp3"
}

Response:
{
  "audio_url": "/tmp/audio_123.mp3",
  "duration": 300,
  "file_size": 4567890
}
```

#### 3. Stream Upload (Optional MVP)
```http
POST /api/stream
Content-Type: multipart/form-data

{
  "audio_file": <binary>,
  "metadata": {...}
}
```

### n8n Workflow Nodes

#### Node 1: Manual Trigger
- **Type**: Manual Trigger
- **Purpose**: Workflow manuell starten

#### Node 2: Generate Content
- **Type**: HTTP Request
- **Method**: POST
- **URL**: `https://your-backend-url.com/api/generate-content` (oder lokaler Tunnel)
- **Body**: 
  ```json
  {
    "topic": "{{ $json.topic || 'Tech News' }}",
    "duration": 300,
    "style": "cyberpunk"
  }
  ```

#### Node 3: Transform Content
- **Type**: Code / Function
- **Purpose**: Response für ElevenLabs formatieren
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
- **Type**: HTTP Request
- **Method**: POST
- **URL**: `https://your-backend-url.com/api/generate-audio` (oder lokaler Tunnel)
- **Body**: `{{ $json }}`

#### Node 5: Save Audio
- **Type**: Write Binary File / HTTP Request
- **Purpose**: Audio-Datei speichern oder direkt streamen

### Environment Variables

#### Backend (.env)
```env
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_MARCEL=...
SUPABASE_URL=https://...
SUPABASE_KEY=...
```

#### n8n (in n8n.zvv.dev konfigurieren)
- **Backend URL**: In n8n Workflow als Variable setzen
- **API Keys**: In n8n Credentials speichern
  - OpenAI API Key
  - ElevenLabs API Key
  - Supabase Credentials (optional)

## 🏗️ Projekt-Struktur

```
radiox-n8n/
├── README.md                 # Dieser Plan
├── docker-compose.yml        # Backend (optional)
├── backend/
│   ├── main.py              # FastAPI Server
│   ├── services/
│   │   ├── gpt_service.py   # GPT Integration
│   │   ├── elevenlabs_service.py  # TTS Integration
│   │   └── audio_service.py # Audio Processing
│   └── requirements.txt
├── workflows/
│   └── radiox-workflow.json # n8n Workflow Export
└── docs/
    └── workflow-design.md   # Detailliertes Workflow-Design
```

**Hinweis**: n8n läuft auf [n8n.zvv.dev](https://n8n.zvv.dev), Workflows werden dort erstellt und können als JSON exportiert werden.

## 📝 Schritt-für-Schritt: Erste Show in 30 Min

### Minute 0-5: Backend Setup
```bash
# 1. Backend erstellen
mkdir backend
cd backend

# 2. FastAPI Server (main.py)
# 3. Requirements installieren
pip install fastapi uvicorn openai elevenlabs

# 4. Server starten
uvicorn main:app --reload --port 8000
```

### Minute 5-10: n8n Setup
```bash
# 1. n8n öffnen: https://n8n.zvv.dev
# 2. Neuen Workflow erstellen
# 3. Backend-URL konfigurieren (muss von n8n erreichbar sein)
#    Option A: Backend öffentlich erreichbar machen
#    Option B: ngrok/Cloudflare Tunnel für lokales Backend
# 4. API Keys in n8n Credentials speichern
```

### Minute 10-20: Workflow bauen
1. **Manual Trigger** hinzufügen
2. **HTTP Request** → `/api/generate-content`
3. **Code Node** → Transform für ElevenLabs
4. **HTTP Request** → `/api/generate-audio`
5. **File Write** → Audio speichern

### Minute 20-25: Testen
1. Workflow auslösen
2. Logs prüfen
3. Audio-Datei validieren

### Minute 25-30: Feintuning
1. Error Handling hinzufügen
2. Retry-Logik
3. Logging verbessern

## 🔄 Workflow-Erweiterungen (Post-MVP)

### Phase 2: Scheduling
- [ ] Cron-Trigger für regelmäßige Shows
- [ ] RSS Feed Integration
- [ ] Automatische Content-Aggregation

### Phase 3: Advanced Features
- [ ] Multi-Speaker Support
- [ ] Jingle Integration
- [ ] Audio Mixing
- [ ] Icecast Streaming
- [ ] Supabase Persistierung

### Phase 4: Production
- [ ] Error Monitoring (Sentry)
- [ ] Performance Monitoring
- [ ] Backup & Recovery
- [ ] Scaling Strategy

## 🛠️ Technologie-Stack

### Backend
- **FastAPI** - REST API Framework
- **OpenAI** - GPT Content Generation
- **ElevenLabs** - Text-to-Speech
- **Supabase** - Database (optional MVP)

### Orchestrierung
- **n8n** - Workflow Automation ([n8n.zvv.dev](https://n8n.zvv.dev))
- **Docker** - Containerization (optional für Backend)

## 📚 Ressourcen

- [n8n Documentation](https://docs.n8n.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ElevenLabs API](https://elevenlabs.io/docs)
- [OpenAI API](https://platform.openai.com/docs)

## ✅ Success Criteria (30 Min MVP)

- [x] n8n Workflow läuft durch
- [x] Content wird generiert
- [x] Audio wird erstellt
- [x] Audio-Datei ist abspielbar
- [x] Workflow ist wiederholbar

## 🚨 Known Limitations (MVP)

- Keine Datenbank-Persistierung
- Kein Error Recovery
- Kein Scheduling
- Keine Multi-Speaker Support
- Kein Audio Mixing
- Kein Streaming

**Alles kann später erweitert werden!**

---

## 🎯 Nächste Schritte

1. **JETZT**: Backend API Endpoints implementieren
2. **DANN**: Backend öffentlich erreichbar machen (Tunnel oder Deployment)
3. **DANACH**: n8n Workflow auf [n8n.zvv.dev](https://n8n.zvv.dev) erstellen
4. **SPÄTER**: Erste Show testen & Erweiterungen nach Plan

## 🔗 Wichtige Links

- **n8n Instanz**: [n8n.zvv.dev](https://n8n.zvv.dev)
- **Backend URL**: Wird konfiguriert (muss von n8n erreichbar sein)

## 🌐 Backend für n8n erreichbar machen

Da n8n auf `n8n.zvv.dev` läuft und das Backend lokal entwickelt wird, muss das Backend öffentlich erreichbar sein. Optionen:

### Option 1: Cloudflare Tunnel (Empfohlen) ⭐

**Schnellstart:**
```powershell
# Windows
cd backend
.\start-tunnel.ps1

# Linux/Mac
cd backend
./start-tunnel.sh
```

**Manuell:**
```bash
# Quick Tunnel (24h, kein Account nötig)
cloudflared tunnel --url http://localhost:8000

# URL kopieren (z.B. https://abc123.trycloudflare.com)
# In n8n Workflow verwenden: https://abc123.trycloudflare.com/api/...
```

**Installation:**
- Windows: `choco install cloudflared` oder [Download](https://github.com/cloudflare/cloudflared/releases)
- Linux/Mac: `brew install cloudflared` oder [Download](https://github.com/cloudflare/cloudflared/releases)

Siehe `backend/tunnel-setup.md` für detaillierte Anleitung.

### Option 2: ngrok
```bash
# ngrok installieren: https://ngrok.com/
ngrok http 8000

# URL kopieren (z.B. https://abc123.ngrok.io)
# In n8n Workflow verwenden: https://abc123.ngrok.io/api/...
```

### Option 3: Deployment (Production)
- Vercel / Railway / Render
- Docker Container auf Server
- Eigene Domain mit Reverse Proxy

**Für MVP: Cloudflare Tunnel ist am einfachsten!**

**Let's build! 🚀**

