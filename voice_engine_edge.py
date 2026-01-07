import asyncio
import edge_tts
import subprocess
import os

class EdgeVoiceEngine:
    def __init__(self, voice: str = "uk-UA-PolinaNeural", rate: str = "+0%"):
        self.voice = voice
        self.rate = rate

    def speak(self, text: str, outfile: str = "output.mp3"):
        if not text:
            return

        async def _speak():
            tts = edge_tts.Communicate(text, voice=self.voice, rate=self.rate)
            await tts.save(outfile)

        asyncio.run(_speak())
        print(f"[Edge-TTS] Збережено у файл: {outfile}")

        # Автоматичне відтворення через ffplay
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", outfile],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
