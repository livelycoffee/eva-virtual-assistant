from core.functions.speech import SpeechEngine
from core.functions.listener import listen_and_transcribe, Listener
from core.brain.primary_llm import get_llm_response

def run_eva():
    listener = Listener() # --> Initialises listener
    sp_engine = SpeechEngine() # --> Initialises Speech Engine

    while True:
        query = listen_and_transcribe(listener=listener)
        if not query:
            continue

        sp_engine.speak(get_llm_response(query))
        if "exit" in query or "bye" in query or "goodbye" or "go away" in query:
            listener.shutdown()
            exit()
            break # --> Just in case

if (__name__ == "__main__"):
    run_eva()

#*---------- END OF CODE ----------*