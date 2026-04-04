from core.functions.speech import SpeechEngine
from core.functions.listener import mic_exec, Listener
#from main_dir.eva import main_task_exec
from core.brain.function_llm import llm_exec
from core.brain.primary_llm import get_llm_response
#import subprocess

def run_eva():
    #subprocess.Popen(["open", "main_dir/gui/index.html"])
    listener = Listener() # --> Initialises listener
    sp_engine = SpeechEngine()
    while True:
        query = mic_exec(listener=listener)
        if not query:
            continue
        sp_engine.speak(get_llm_response(query))
        if "exit" in query or "bye" in query or "shut down" in query or "shutdown" in query or "goodbye" in query:
            listener.shutdown()
            exit(0)
            break

if (__name__ == "__main__"):
    run_eva()

#*---------- END OF CODE ----------*