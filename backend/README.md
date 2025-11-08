# RadioX Backend API

Minimal FastAPI Backend für n8n Integration - Erste Radioshow in 30 Minuten.

## 🚀 Quick Start

### 1. Environment Setup

```bash
# .env Datei erstellen
cp env.template .env

# .env bearbeiten und API Keys eintragen:
# - OPENAI_API_KEY
# - ELEVENLABS_API_KEY
# - ELEVENLABS_VOICE_MARCEL
```

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. Server starten

```bash
# Development Mode
python main.py

# Oder mit uvicorn direkt
uvicorn main:app --reload --port 8000
```

Server läuft auf: `http://localhost:8000`

## 📡 API Endpoints

### Health Check
```http
GET /
GET /health
```

### Content Generation
```http
POST /api/generate-content
Content-Type: application/json

{
  "topic": "Tech News",
  "duration": 300,
  "style": "cyberpunk"
}
```

### Audio Generation
```http
POST /api/generate-audio
Content-Type: application/json

{
  "text": "Generated script...",
  "voice_id": "marcel",
  "output_format": "mp3"
}
```

### Get Audio File
```http
GET /api/audio/{file_path}
```

## 🔧 Environment Variables

Siehe `env.template` für alle benötigten Variablen.

**Wichtig:**
- `OPENAI_API_KEY` - OpenAI API Key
- `ELEVENLABS_API_KEY` - ElevenLabs API Key
- `ELEVENLABS_VOICE_MARCEL` - Voice ID für Marcel

## 🌐 Für n8n erreichbar machen

Da n8n auf `n8n.zvv.dev` läuft, muss das Backend öffentlich erreichbar sein:

```bash
# Option 1: ngrok (schnellste Lösung)
ngrok http 8000

# Option 2: Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8000
```

Die generierte URL dann in n8n Workflow verwenden.

## 📝 Testing

```bash
# Health Check
curl http://localhost:8000/health

# Content Generation
curl -X POST http://localhost:8000/api/generate-content \
  -H "Content-Type: application/json" \
  -d '{"topic": "Tech News", "duration": 300, "style": "cyberpunk"}'

# Audio Generation
curl -X POST http://localhost:8000/api/generate-audio \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test.", "output_format": "mp3"}'
```

## 🏗️ Projekt-Struktur

```
backend/
├── main.py                 # FastAPI App
├── services/
│   ├── gpt_service.py      # GPT Content Generation
│   └── elevenlabs_service.py  # ElevenLabs TTS
├── requirements.txt        # Python Dependencies
├── env.template           # Environment Template
└── README.md             # Diese Datei
```

## 🐛 Troubleshooting

**Service initialization failed:**
- Prüfe ob alle Environment Variables gesetzt sind
- Prüfe ob API Keys gültig sind

**Audio generation failed:**
- Prüfe ElevenLabs API Key
- Prüfe Voice ID

**CORS Errors:**
- CORS ist aktuell für alle Origins erlaubt (nur für Development!)
- In Production einschränken

