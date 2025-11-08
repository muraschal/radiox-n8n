"""
ElevenLabs Service für Text-to-Speech
"""
import os
import tempfile
from pathlib import Path
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings


class ElevenLabsService:
    def __init__(self):
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable is required")
        
        self.client = ElevenLabs(api_key=api_key)
        
        # Voice IDs aus Environment (kann später erweitert werden)
        self.voice_marcel = os.getenv("ELEVENLABS_VOICE_MARCEL")
        if not self.voice_marcel:
            raise ValueError("ELEVENLABS_VOICE_MARCEL environment variable is required")
    
    def generate_audio(
        self,
        text: str,
        voice_id: str = None,
        output_format: str = "mp3"
    ) -> dict:
        """
        Generiert Audio aus Text mit ElevenLabs
        
        Args:
            text: Text zum Konvertieren
            voice_id: Voice ID (default: marcel)
            output_format: Audio Format (mp3, wav, etc.)
        
        Returns:
            dict mit audio_url, duration, file_size
        """
        # Verwende Standard-Voice falls nicht angegeben
        if not voice_id:
            voice_id = self.voice_marcel
        
        # Voice Settings
        voice_settings = VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True
        )
        
        try:
            # Generiere Audio mit neuer API
            audio_generator = self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id="eleven_multilingual_v2",
                voice_settings=voice_settings
            )
            
            # Konvertiere Generator zu Bytes
            audio_bytes = b"".join(audio_generator)
            
            # Speichere temporär
            temp_dir = Path(tempfile.gettempdir())
            output_file = temp_dir / f"radiox_audio_{os.urandom(8).hex()}.{output_format}"
            
            with open(output_file, "wb") as f:
                f.write(audio_bytes)
            
            file_size = output_file.stat().st_size
            
            # Geschätzte Dauer (11.025 kHz, 16-bit, mono = ~22KB/Sekunde für MP3)
            # Grobe Schätzung basierend auf Dateigröße
            estimated_duration = int(file_size / 22000)  # Sehr grobe Schätzung
            
            return {
                "audio_url": str(output_file),
                "file_path": str(output_file),
                "duration": estimated_duration,
                "file_size": file_size,
                "format": output_format,
                "voice_id": voice_id
            }
        
        except Exception as e:
            raise Exception(f"ElevenLabs Audio Generation failed: {str(e)}")

