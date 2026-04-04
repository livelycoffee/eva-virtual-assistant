from piper.voice import PiperVoice
import numpy as np
import sounddevice as sd
import time

PIPER_MODEL = "models/voice_models/piper-model.onnx" # or path to piper model
# NOTE: Make sure you have a matching .onnx.json file for your model

class SpeechEngine():
    def __init__(self):
        self.voice = PiperVoice.load(model_path=PIPER_MODEL)
        self.SAMPLE_RATE = self.voice.config.sample_rate
        
    def speak(self, text: str) -> None:
        audio = self.voice.synthesize(text)
        chunks = []
        for chunk in audio:
            data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            chunks.append(data)
        audio = np.concatenate(chunks)
        audio = audio.astype(np.float32) / 32767.0 # --> or 32768.0
        print(f"\nEVA: {text}\n")
        sd.play(audio, samplerate=self.SAMPLE_RATE)
        sd.wait()
        time.sleep(0.02)

#*---------- END OF CODE ----------*