# ---------- IMPORTS ----------

import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import time
import math
import queue
from backend.config import Config

# ---------- CONFIGURATION SETUP ----------

config = Config()

MODEL_SIZE = config.get("models.WHISPER_MODEL", "tiny")
USER_NAME = config.get("user.name", "USER")

PAUSE_THRESHOLD = config.get("listener.PAUSE_THRESHOLD", 1.2)
SPEECH_THRESHOLD = config.get("listener.SPEECH_THRESHOLD", 3.6)
AUDIO_THRESHOLD = config.get("listener.AUDIO_THRESHOLD", 0.1)
LOOP_SLEEP_TIME = config.get("listener.LOOP_SLEEP_TIME", 0.03)
STREAM_LIFETIME = config.get("listener.STREAM_LIFETIME", 3)

SAMPLE_RATE = 16000 # Needs to support dynamic selection in the future (DO NOT ADD TO CONFIG)

# ---------- LISTENER CLASS ----------

class Listener:
    def __init__(self):
        self.started = False
        self.sound_data = []
        self.prev_time = time.time()
        self.audio_queue = queue.Queue()

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE, 
            channels=1, 
            callback=self.callback
        )

    def callback(self, indata, frames, time_info, status):
        volume = math.sqrt(np.dot(indata.ravel(), indata.ravel())) * 10

        if volume > SPEECH_THRESHOLD: # USER SPEECH DETECTION
            self.started = True 
            self.prev_time = time.time() 

        if volume > AUDIO_THRESHOLD and self.started: # AUDIO DETECTION
            try:
                self.audio_queue.put_nowait(indata.copy())
            except queue.Full:
                pass # --> Drop frames instead of blocking (improved stability)

    def listen(self) -> np.typing.NDArray[np.float32]:
        self.started = False
        self.sound_data = []
        self.prev_time = time.time()

        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break

        self.stream.start()
        while True: # INNER LOOP
            time.sleep(LOOP_SLEEP_TIME)
            try:
                chunk = self.audio_queue.get(timeout=0.5)
                self.sound_data.append(chunk)
            except queue.Empty:
                continue

            if ((time.time() - self.prev_time) >= STREAM_LIFETIME) and not self.started: # --> Temporary macos hang fix
                self.stream.stop()
                self.stream.start()

            if ((time.time() - self.prev_time) >= PAUSE_THRESHOLD) and self.started:
                break
        self.stream.stop()

        while True:
            try:
                self.sound_data.append(self.audio_queue.get_nowait())
            except queue.Empty:
                break
        
        sound_data = self.sound_data
        self.sound_data = []

        if not sound_data:
            return np.array([], dtype=np.float32)

        audio = np.concatenate(sound_data, axis=0)
        audio = audio.astype(np.float32)
        return audio.flatten()
    
    def shutdown(self):
        if self.stream.active:
            self.stream.stop()
        self.stream.close()

# ---------- FASTER-WHISPER TRANSCRIBER ----------

class FS_Transcriber:
    def __init__(self):
        self.model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8") # or CUDA with float32
    
    def transcribe(self, audio) -> str:
        try:
            segments, info = self.model.transcribe(audio, language = "en", task="translate", condition_on_previous_text=False)
            query = "".join([segment.text.strip() for segment in segments])
            return query
        except Exception as e:
            print(f"[ERR - transcriber]: {e}")
            return ""
        
# ---------- MAIN MIC+TRANSCRIBE EXEC FUNCTION ----------

def listen_and_transcribe(listener: Listener, transcriber: FS_Transcriber) -> str:
    query = ""
    print("[SR]: Listening...")
    audio = listener.listen()
    print("[SR]: Audio recorded.")
    if len(audio) != 0:
        print("[SR]: Recognising...")
        query = transcriber.transcribe(audio)
    if query:
        print(f"\n{USER_NAME}: {str(query)}")
    query = str(query).lower()
    return query

#*---------- END OF CODE ----------*