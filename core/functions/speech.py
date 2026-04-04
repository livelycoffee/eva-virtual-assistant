from piper.voice import PiperVoice
import numpy as np
import sounddevice as sd

PIPER_MODEL = "models/voice_models/en_US-hfc_female-medium.onnx"

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
        audio = audio.astype(np.float32) / 32767.0
        print(f"\nEVA: {text}\n")
        sd.play(audio, samplerate=self.SAMPLE_RATE)
        sd.wait()

# import pyttsx3 !-----> DEPRICIATED
#
# class old_SpeechEngine():
#     def __init__(self):
#         self.engine = pyttsx3.init("nsss")
#         # voices = self.engine.getProperty("voices")
#         # self.engine.setProperty("voice", voices[0].id)
#         # self.engine.setProperty("rate", 95) !--> NOT WORKING
#
#     def speak(self, text: str) -> None:
#         print(f"\nEVA: {text}\n")
#         self.engine = pyttsx3.init("nsss")
#         self.engine.say(text.encode("ascii", "ignore").decode()) # ignores non-ascii
#         self.engine.runAndWait()
#         self.engine.stop()
#
#     def speech_shutdown(self) -> None:
#         self.engine.stop()

#*---------- END OF CODE ----------*