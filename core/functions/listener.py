import sounddevice as sd
import numpy as np
from numpy.typing import NDArray
from faster_whisper import WhisperModel
import time
import math
import queue

MODEL_SIZE = "tiny" # or "small"
MODEL = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8") # or CUDA with float32

#MAX_TIME = 10 # seconds !--> Not required anymore
PAUSE_THRESHOLD = 1.2 # seconds
SPEECH_THRESHOLD = 3.6 # old - 3.5
AUDIO_THRESHOLD = 0.1 # old - 0.1

SAMPLE_RATE = 16000
LOOP_SLEEP_TIME = 0.03 # seconds

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
        #self.stream.start()

    def callback(self, indata, frames, time_info, status):
        volume = math.sqrt(np.dot(indata.ravel(), indata.ravel())) * 10

        if volume > SPEECH_THRESHOLD: # USER SPEECH DETECTION
            self.started = True 
            self.prev_time = time.time() 

        if volume > AUDIO_THRESHOLD and self.started: # AUDIO DETECTION
            self.audio_queue.put(indata.copy())

    def listen(self) -> NDArray[np.float32]:
        self.started = False
        self.sound_data = []
        self.prev_time = time.time()

        self.stream.start()
        print("[SR]: Listening...")
        while True: # INNER LOOP
            time.sleep(LOOP_SLEEP_TIME)
            try:
                chunk = self.audio_queue.get(timeout=0.5)
                self.sound_data.append(chunk)
            except queue.Empty:
                continue
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

def mic_exec(listener: Listener) -> str:
    '''
    Main MIC Executor for EVA. Listens and Recognises User Query and Outputs a Sanitised Query
    '''
    while True:
        query = ""
        audio = listener.listen()
        if len(audio) != 0:
            print("[SR]: Recognising...")
            try:
                segments, info = MODEL.transcribe(audio, language = "en", task="translate", condition_on_previous_text=False)
                query = "".join([segment.text.strip() for segment in segments])
            except:
                print()
                return ""
        print(f"\nUSER: {str(query)}")
        query = str(query).lower()
        return query

#*---------- END OF CODE ----------*