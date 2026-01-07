import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play

async def main():
    text = "Привіт, я Поліна, український голос."
    voice = "uk-UA-PolinaNeural"
    outfile = "polina.mp3"

    # Генеруємо файл
    tts = edge_tts.Communicate(text, voice=voice)
    await tts.save(outfile)

    # Відтворюємо файл через ffmpeg
    sound = AudioSegment.from_file(outfile, format="mp3")
    play(sound)

asyncio.run(main())
