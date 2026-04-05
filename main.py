# ---------- IMPORTS ----------

from core.functions.speech import SpeechEngine
from core.functions.listener import listen_and_transcribe, Listener, FS_Transcriber
from core.brain.primary_llm import get_llm_response

# ---------- MAIN ----------

def run_eva():
    listener = Listener() # --> Initialises listener
    sp_engine = SpeechEngine() # --> Initialises Speech Engine
    fs_transcriber = FS_Transcriber() # --> Initialises transcriber
    try:
        while True:
            query = listen_and_transcribe(listener=listener, transcriber=fs_transcriber)
            if not query:
                continue

            sp_engine.speak(get_llm_response(query))
            if "exit" in query or "bye" in query or "goodbye" in query or "go away" in query: # --> Fallback exit
                listener.shutdown()
                exit()
                break # --> Just in case
    finally:
        listener.shutdown()

if (__name__ == "__main__"):
    run_eva()

#*---------- END OF CODE ----------*