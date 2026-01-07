import asyncio
import edge_tts

async def main():
    text = "Hello, this is a test with Edge TTS."
    voice = "en-US-GuyNeural"   # стабільний англійський голос
    tts = edge_tts.Communicate(text, voice=voice)
    await tts.save("test.mp3")

asyncio.run(main())
