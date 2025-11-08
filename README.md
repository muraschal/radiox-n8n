# RadioX n8n Integration - Minimaldurchstich Plan

> **Ziel**: Erste funktionierende Radioshow in 30 Minuten mit n8n-Orchestrierung

## 🎯 Projekt-Übersicht

RadioX wird auf eine **n8n-basierte Orchestrierung** umgestellt. Das Backend liefert fokussierte API-Services, während n8n die Workflow-Orchestrierung übernimmt.

### Architektur-Prinzip

```
┌─────────────────┐
│   n8n Workflow  │  ← Orchestrierung, Scheduling, Error Handling
└────────┬────────┘
         │ HTTP API Calls
         ↓
┌─────────────────┐
│  Backend APIs   │  ← Business Logic, Audio Processing
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

#### 1.2 n8n Setup
- [ ] n8n Docker Container starten
- [ ] n8n Webhook konfigurieren
- [ ] Environment Variables setzen (API Keys)

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
- **URL**: `http://backend:8000/api/generate-content`
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
- **URL**: `http://backend:8000/api/generate-audio`
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

#### n8n (.env)
```env
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=...
BACKEND_URL=http://backend:8000
```

## 🏗️ Projekt-Struktur

```
radiox-n8n/
├── README.md                 # Dieser Plan
├── docker-compose.yml        # n8n + Backend
├── backend/
│   ├── main.py              # FastAPI Server
│   ├── services/
│   │   ├── gpt_service.py   # GPT Integration
│   │   ├── elevenlabs_service.py  # TTS Integration
│   │   └── audio_service.py # Audio Processing
│   └── requirements.txt
├── n8n/
│   ├── workflows/           # n8n Workflow Exports
│   └── .env
└── docs/
    └── workflow-design.md   # Detailliertes Workflow-Design
```

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
# 1. n8n Docker starten
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# 2. n8n öffnen: http://localhost:5678
# 3. Workflow erstellen
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
- **n8n** - Workflow Automation
- **Docker** - Containerization

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
2. **DANN**: n8n Workflow erstellen
3. **DANACH**: Erste Show testen
4. **SPÄTER**: Erweiterungen nach Plan

**Let's build! 🚀**

