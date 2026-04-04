from ollama import chat
from ollama import ChatResponse
from exec_layer.normal_exec.main_exec import command_registry

MODEL = "functiongemma"
DEFAULT_SYS_MESSAGE = "You are an AI Assistant that can do tool calling using the following given tools. Execute given query properly and use the correct tool(s) with proper parameters as required accordingly."

def llm_exec(query: str) -> None:
    '''
    Function to request FunctionGemma LLM to execute tasks on the User Device!

    Args:
        query (str): Give a proper prompt to get the right tasks done. (eg. Open Chrome, or Search Youtube for DanTDM)

    Returns:
        None
    '''
    prompt = f"User: {query}\nEVA (FUNCTION EXECUTOR - You): "
    response: ChatResponse = chat(model=MODEL, messages=[
        {
            'role': 'system',
            'content': "You are EVA, an AI Assistant. Respond in short in only 1-2 sentences. Execute given query properly and use the correct tool(s) as required accordingly. IGNORE if user has not given any tasks or task is not a function executing query."
        },
        {
            'role': 'user',
            'content': prompt
        },
    ], tools=list(command_registry.values()))

    for tool in response.message.tool_calls or []:
        try:
            func = command_registry.get(tool.function.name)
            if func:
                func(**tool.function.arguments)
            return True
        except:
            return False

    return False

#*---------- END OF CODE ----------*