"""
Vollständiger System Check für RadioX
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

def check_environment():
    """Prüfe Environment Variables"""
    print("=" * 60)
    print("1. ENVIRONMENT VARIABLES CHECK")
    print("=" * 60)
    
    checks = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
        "ELEVENLABS_API_KEY": os.getenv("ELEVENLABS_API_KEY"),
        "ELEVENLABS_VOICE_MARCEL": os.getenv("ELEVENLABS_VOICE_MARCEL"),
    }
    
    all_ok = True
    for key, value in checks.items():
        if value:
            status = "OK" if len(str(value)) > 10 else "SHORT"
            print(f"   {status:4} {key}: {'*' * min(20, len(str(value)))}")
        else:
            print(f"   MISS {key}: NOT SET")
            all_ok = False
    
    return all_ok

def check_gpt_service():
    """Test GPT Service"""
    print("\n" + "=" * 60)
    print("2. GPT SERVICE CHECK")
    print("=" * 60)
    
    try:
        from services.gpt_service import GPTService
        gpt = GPTService()
        print("   OK   GPT Service initialisiert")
        
        # Quick test
        result = gpt.generate_content(
            topic="Test",
            duration=30,
            style="cyberpunk"
        )
        print(f"   OK   Content Generation: {len(result['content'])} Zeichen")
        print(f"   OK   Speaker: {result['speaker']}")
        return True
    except Exception as e:
        print(f"   FAIL GPT Service: {str(e)}")
        return False

def check_elevenlabs_service():
    """Test ElevenLabs Service"""
    print("\n" + "=" * 60)
    print("3. ELEVENLABS SERVICE CHECK")
    print("=" * 60)
    
    try:
        from services.elevenlabs_service import ElevenLabsService
        el = ElevenLabsService()
        print("   OK   ElevenLabs Service initialisiert")
        
        # Test mit kurzem Text
        result = el.generate_audio(
            text="Test",
            output_format="mp3"
        )
        print(f"   OK   Audio Generation: {result['file_size']} bytes")
        return True
    except Exception as e:
        error_msg = str(e)
        if "missing_permissions" in error_msg or "401" in error_msg:
            print(f"   WARN ElevenLabs: API Key hat keine text_to_speech Permission")
            print(f"        Bitte prüfe ElevenLabs Account Settings")
        else:
            print(f"   FAIL ElevenLabs Service: {error_msg[:100]}")
        return False

def check_backend_server():
    """Prüfe ob Backend Server läuft"""
    print("\n" + "=" * 60)
    print("4. BACKEND SERVER CHECK")
    print("=" * 60)
    
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("   OK   Backend Server läuft auf Port 8000")
            return True
        else:
            print(f"   WARN Backend Server: Status {response.status_code}")
            return False
    except Exception as e:
        print("   WARN Backend Server läuft NICHT")
        print(f"        Starte mit: python -m uvicorn main:app --host 0.0.0.0 --port 8000")
        return False

def check_cloudflare_tunnel():
    """Prüfe Cloudflare Tunnel"""
    print("\n" + "=" * 60)
    print("5. CLOUDFLARE TUNNEL CHECK")
    print("=" * 60)
    
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name']):
            if 'cloudflared' in proc.info['name'].lower():
                print(f"   OK   Cloudflare Tunnel läuft (PID: {proc.info['pid']})")
                print("        URL sollte im Terminal sichtbar sein")
                return True
    except:
        pass
    
    print("   WARN Cloudflare Tunnel läuft NICHT")
    print("        Starte mit: cd backend; .\\start-tunnel-with-backend.ps1")
    return False

def main():
    """Hauptfunktion"""
    print("\n")
    print("=" * 60)
    print("RADIOX SYSTEM CHECK")
    print("=" * 60)
    print()
    
    results = {
        "Environment": check_environment(),
        "GPT Service": check_gpt_service(),
        "ElevenLabs Service": check_elevenlabs_service(),
        "Backend Server": check_backend_server(),
        "Cloudflare Tunnel": check_cloudflare_tunnel(),
    }
    
    print("\n" + "=" * 60)
    print("ZUSAMMENFASSUNG")
    print("=" * 60)
    
    for name, result in results.items():
        status = "OK" if result else "WARN"
        print(f"   {status:4} {name}")
    
    all_critical = results["Environment"] and results["GPT Service"]
    
    if all_critical:
        print("\n" + "=" * 60)
        print("SYSTEM BEREIT FÜR n8n INTEGRATION!")
        print("=" * 60)
        print("\nNächste Schritte:")
        print("1. Cloudflare Tunnel URL kopieren")
        print("2. n8n öffnen: https://n8n.zvv.dev")
        print("3. Workflow importieren: workflows/radiox-show-workflow.json")
        print("4. Tunnel-URL in Workflow eintragen")
        print("5. Workflow testen!")
    else:
        print("\n" + "=" * 60)
        print("SYSTEM NICHT VOLLSTÄNDIG KONFIGURIERT")
        print("=" * 60)
        print("\nBitte behebe die oben genannten Probleme.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAbgebrochen.")
    except Exception as e:
        print(f"\n\nFehler: {str(e)}")
        import traceback
        traceback.print_exc()

