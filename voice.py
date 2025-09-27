from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def tts(text):
  audio = elevenlabs.text_to_speech.convert(
      text=text,
      voice_id="qAZH0aMXY8tw1QufPN0D",
      model_id="eleven_multilingual_v2",
      output_format="mp3_44100_128",
  )

  with open("eleven_output.mp3","wb") as f:
    for chunk in audio:
      f.write(chunk)
  
  

if __name__ == "__main__":
  tts("tariffs for everyone")

