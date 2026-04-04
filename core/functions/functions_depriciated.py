# THESE FUNCTIONS USED TO BE USED BEFORE, PLEASE SWITCH TO IT IF LISTEN FUNCTIONALITY BREAKS
# WARN: This function has a critical bug where process may hang due to PyAudio issues.
#
# def listen():
#     '''
#     Function that Streams audio from Microphone, and outputs recorded audio data as an audio numpy array.
#     '''
#     started = False
#     fs = 16000
#     sound_data = []
#     prev_time = time.time()
#
#     def callback(indata, frames, time_info, status):
#         nonlocal prev_time, started
#         #volume = np.linalg.norm(indata)*10
#         volume = math.sqrt(float((indata * indata).sum())) * 10
#
#         #print(volume)
#         # width = 50  # max bar length
#         # bar = "|" * int(volume)
#         # print(f"\r{bar:<{width}}", end="", flush=True) !--> DO NOT USE (Causes Hang)
#
#         if volume > SPEECH_THRESHOLD: # USER SPEECH DETECTION
#             started = True 
#             prev_time = time.time() 
#
#         if volume > AUDIO_THRESHOLD and started: # AUDIO DETECTION
#             sound_data.append(indata.copy())
#
#     try:
#         with sd.InputStream(samplerate=fs, channels=1, callback=callback):
#             print("[SR]: Listening...")
#             while True:
#                 time.sleep(0.1)
#                 if ((time.time() - prev_time) >= PAUSE_THRESHOLD) and started:
#                     break
#                 # if ((time.time() - prev_time) >= MAX_TIME) and not started: !--> Not required anymore
#                 #     break
#     except KeyboardInterrupt:
#         print("\n[SR]: Interrupted safely.")
#         return np.array([], dtype=np.float32)
#     finally:
#         sd.stop()
#
#     if not sound_data:
#         return np.array([], dtype=np.float32)
#
#     audio = np.concatenate(sound_data, axis=0)
#     audio = audio.astype(np.float32)
#     return audio.flatten()
#
# def speak(Text): !-----> DEPRICIATED OLD LISTEN
#     '''
#     Speak function for EVA. Speaks input Text using nsss and waits for completion (but non-blocking).
#     '''
#     engine = pyttsx3.init("nsss")
#     voices = engine.getProperty("voices")
#     engine.setProperty("voice", voices[0].id)
#     engine.setProperty("rate", 95)
#
#     print(f"\nEVA: {Text}\n")
#     engine.stop()
#     engine.say(Text.encode("ascii", "ignore").decode()) # ignores non-ascii
#     engine.runAndWait()
#
# import pyttsx3 !-----> DEPRICIATED ADVANCED LISTEN
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