import sys
from core.spark_core import SparkCore
from interfaces.voice_engine import VoiceEngine
from interfaces.voice_engine_edge import EdgeVoiceEngine

def main():
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Привіт! Це тест Spark-1."

    spark = SparkCore()

    # Використати офлайн голос:
    # voice = VoiceEngine()

    # Використати онлайн голос (Edge-TTS):
    voice = EdgeVoiceEngine()

    voice.speak(text)
    print(f"[Spark-1] Озвучено повідомлення: {text}")

if __name__ == "__main__":
    main()
