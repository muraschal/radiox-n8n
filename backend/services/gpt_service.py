"""
GPT Service für Content Generation
"""
import os
from typing import Optional
from openai import OpenAI


class GPTService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    def generate_content(
        self,
        topic: str,
        duration: int = 300,
        style: str = "cyberpunk"
    ) -> dict:
        """
        Generiert Radio-Show Content mit GPT
        
        Args:
            topic: Thema der Show
            duration: Dauer in Sekunden
            style: Stil (cyberpunk, gta, etc.)
        
        Returns:
            dict mit content, duration, speaker
        """
        # Berechne ungefähre Wortanzahl (150 WPM = ~2.5 Wörter/Sekunde)
        words_per_second = 2.5
        target_words = int(duration * words_per_second)
        
        prompt = f"""Erstelle ein Radio-Show-Script im {style}-Stil zum Thema "{topic}".

Anforderungen:
- Länge: ca. {target_words} Wörter (für {duration} Sekunden Audio)
- Stil: {style}, modern, unterhaltsam
- Format: Direkte Rede, als würde ein Radio-Moderator sprechen
- Keine Markdown, keine Formatierung, nur reiner Text
- Beginne direkt mit dem Inhalt, keine Einleitung

Script:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Du bist ein kreativer Radio-Show-Autor im Cyberpunk/GTA-Stil. Erstelle unterhaltsame, dynamische Radio-Content."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Standard-Speaker (kann später erweitert werden)
            speaker = "marcel"
            
            return {
                "content": content,
                "duration": duration,
                "speaker": speaker,
                "word_count": len(content.split()),
                "style": style
            }
        
        except Exception as e:
            raise Exception(f"GPT Content Generation failed: {str(e)}")

