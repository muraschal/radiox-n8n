"""
Direkter Test der Services ohne HTTP
"""
import os
import sys
import io
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Lade env.local
load_dotenv('env.local')

from services.gpt_service import GPTService
from services.elevenlabs_service import ElevenLabsService

def test_gpt_service():
    """Test GPT Service direkt"""
    print("🧠 Testing GPT Service...")
    try:
        gpt = GPTService()
        print("   ✅ GPT Service initialisiert")
        
        # Test Content Generation
        print("   📝 Generiere Test-Content...")
        result = gpt.generate_content(
            topic="Tech News",
            duration=60,
            style="cyberpunk"
        )
        
        print(f"   ✅ Content generiert!")
        print(f"   📊 Länge: {len(result['content'])} Zeichen")
        print(f"   📊 Wörter: {result.get('word_count', 'N/A')}")
        print(f"   🎙️  Speaker: {result['speaker']}")
        print(f"   🎨 Stil: {result['style']}")
        print(f"\n   📄 Content Preview (erste 200 Zeichen):")
        print(f"   {result['content'][:200]}...")
        
        return result
        
    except Exception as e:
        print(f"   ❌ Fehler: {str(e)}")
        return None

def test_elevenlabs_service():
    """Test ElevenLabs Service direkt"""
    print("\n🎤 Testing ElevenLabs Service...")
    try:
        el = ElevenLabsService()
        print("   ✅ ElevenLabs Service initialisiert")
        
        # Test Audio Generation
        test_text = "Hallo, dies ist ein Test für RadioX. Die Audio-Generierung funktioniert einwandfrei."
        print(f"   🔊 Generiere Test-Audio...")
        print(f"   📝 Text: {test_text}")
        
        result = el.generate_audio(
            text=test_text,
            voice_id=None,  # Verwendet Standard (Marcel)
            output_format="mp3"
        )
        
        print(f"   ✅ Audio generiert!")
        print(f"   📁 Datei: {result['file_path']}")
        print(f"   📊 Größe: {result['file_size']} bytes")
        print(f"   ⏱️  Dauer: ~{result['duration']} Sekunden")
        print(f"   🎙️  Voice: {result['voice_id']}")
        print(f"   📦 Format: {result['format']}")
        
        return result
        
    except Exception as e:
        print(f"   ❌ Fehler: {str(e)}")
        return None

def test_full_pipeline():
    """Test vollständige Pipeline"""
    print("\n🎬 Testing Full Pipeline...")
    print("=" * 60)
    
    # Step 1: Content Generation
    content_result = test_gpt_service()
    if not content_result:
        print("\n❌ Pipeline abgebrochen: Content Generation fehlgeschlagen")
        return False
    
    # Step 2: Audio Generation
    audio_result = test_elevenlabs_service()
    if not audio_result:
        print("\n❌ Pipeline abgebrochen: Audio Generation fehlgeschlagen")
        return False
    
    print("\n" + "=" * 60)
    print("✅ VOLLSTÄNDIGE PIPELINE ERFOLGREICH!")
    print("=" * 60)
    print(f"\n📄 Content: {len(content_result['content'])} Zeichen")
    print(f"🎵 Audio: {audio_result['file_path']}")
    print(f"📊 Audio Größe: {audio_result['file_size']} bytes")
    print(f"\n🎉 Alles funktioniert! Bereit für n8n Integration!")
    
    return True

if __name__ == "__main__":
    print("🚀 RadioX Service Direct Test")
    print("=" * 60)
    
    # Test einzelne Services
    test_gpt_service()
    test_elevenlabs_service()
    
    # Test vollständige Pipeline
    print("\n" + "=" * 60)
    response = input("\nVollständige Pipeline testen? (j/n): ")
    if response.lower() in ['j', 'y', 'yes', 'ja']:
        test_full_pipeline()
    else:
        print("\n✅ Service Tests abgeschlossen!")

