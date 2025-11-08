"""
RadioX Backend API - Minimaldurchstich für n8n Integration
"""
import os
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from services.gpt_service import GPTService
from services.elevenlabs_service import ElevenLabsService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RadioX Backend API",
    description="Minimal API für n8n Integration - Erste Radioshow in 30 Min",
    version="0.1.0"
)

# CORS Middleware (für n8n Zugriff)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Production einschränken!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
try:
    gpt_service = GPTService()
    elevenlabs_service = ElevenLabsService()
except Exception as e:
    print(f"Warning: Service initialization failed: {e}")
    print("Make sure all environment variables are set correctly.")


# Request/Response Models
class GenerateContentRequest(BaseModel):
    topic: str
    duration: int = 300
    style: str = "cyberpunk"


class GenerateContentResponse(BaseModel):
    content: str
    duration: int
    speaker: str
    word_count: Optional[int] = None
    style: Optional[str] = None


class GenerateAudioRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None
    output_format: str = "mp3"


class GenerateAudioResponse(BaseModel):
    audio_url: str
    file_path: str
    duration: int
    file_size: int
    format: str
    voice_id: str


# Health Check
@app.get("/")
async def root():
    return {
        "message": "RadioX Backend API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "generate_content": "/api/generate-content",
            "generate_audio": "/api/generate-audio",
            "stream": "/api/stream"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


# API Endpoints

@app.post("/api/generate-content", response_model=GenerateContentResponse)
async def generate_content(request: GenerateContentRequest):
    """
    Generiert Radio-Show Content mit GPT
    
    Args:
        request: GenerateContentRequest mit topic, duration, style
    
    Returns:
        GenerateContentResponse mit generiertem Content
    """
    try:
        result = gpt_service.generate_content(
            topic=request.topic,
            duration=request.duration,
            style=request.style
        )
        return GenerateContentResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Content generation failed: {str(e)}"
        )


@app.post("/api/generate-audio", response_model=GenerateAudioResponse)
async def generate_audio(request: GenerateAudioRequest):
    """
    Generiert Audio aus Text mit ElevenLabs TTS
    
    Args:
        request: GenerateAudioRequest mit text, voice_id, output_format
    
    Returns:
        GenerateAudioResponse mit Audio-Informationen
    """
    try:
        result = elevenlabs_service.generate_audio(
            text=request.text,
            voice_id=request.voice_id,
            output_format=request.output_format
        )
        return GenerateAudioResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Audio generation failed: {str(e)}"
        )


@app.get("/api/audio/{file_path:path}")
async def get_audio(file_path: str):
    """
    Liefert generierte Audio-Datei
    
    Args:
        file_path: Pfad zur Audio-Datei
    
    Returns:
        Audio-Datei als FileResponse
    """
    try:
        audio_file = Path(file_path)
        if not audio_file.exists():
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        return FileResponse(
            path=audio_file,
            media_type="audio/mpeg",
            filename=audio_file.name
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve audio: {str(e)}"
        )


@app.post("/api/stream")
async def stream_audio(audio_file: UploadFile = File(...)):
    """
    Stream Upload Endpoint (Optional für MVP)
    
    Args:
        audio_file: Audio-Datei zum Upload
    
    Returns:
        Upload-Status
    """
    # TODO: Implementierung für Icecast/Streaming
    return {
        "message": "Stream endpoint - Not yet implemented",
        "filename": audio_file.filename,
        "status": "placeholder"
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )

