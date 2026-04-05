# ---------- IMPORTS ----------

from piper.voice import PiperVoice
import numpy as np
import sounddevice as sd
from backend.config import Config

# ---------- CONFIGURATION ----------

cf = Config()
PIPER_MODEL = cf.get_parameter("models.PIPER_MODEL") # or path to piper model
ASSISTANT_NAME = cf.get("assistant.name", "EVA")

# ---------- SPEECH ENGINE ----------

class SpeechEngine():
    def __init__(self):
        self.voice = PiperVoice.load(model_path=PIPER_MODEL)
        self.SAMPLE_RATE = self.voice.config.sample_rate
        
    def speak(self, text: str) -> None:
        audio = self.voice.synthesize(text.encode("ascii", "ignore").decode()) # --> synthesize first
        chunks = []
        for chunk in audio:
            data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            chunks.append(data)
        audio = np.concatenate(chunks)
        audio = audio.astype(np.float32) / 32767.0 # --> or 32768.0
        print(f"\n{ASSISTANT_NAME}: {text}\n")
        sd.play(audio, samplerate=self.SAMPLE_RATE) # --> play audio later
        sd.wait()

#*---------- END OF CODE ----------*