from ollama import chat
from ollama import ChatResponse
import json, os
from exec_layer.normal_exec.normal_exec import command_registry

MODEL = "qwen3:4b-q4_K_M" # --> or gemma3 or pheem49/Luna:qwen3-4b
#MODEL_SMALL = "qwen3:0.6b" # commented to prevent errors on runtime, uncomment if required
CHAT_LOG = "database/chat_log.json"
MAX_HISTORY = 50

SYSTEM_MESSAGE = "You are EVA, an AI Assistant. Respond in short in only 1-2 sentences max, or maybe even less, until and unless specified by the user or absolutely necessary. Never respond with emojis. Use the tools (with proper input) only when the user asks for a task to be done."

SYSTEM_MESSAGE_EXEC = """You are a system that converts tool execution results into a short user-facing friendly message.
Rules:
•⁠ Be concise, and keep your message short and pretty.
• Do not just list everything, only include what seems to be important (no need to mention waits, for example).
•⁠ Do NOT ever add any extra info and do NOT use any information OTHER than what was given to you.
•⁠ Do not hallucinate.
•⁠ Only use the provided data. (ignore \"None\")"""

TOOLS = command_registry

def get_llm_response(query):
    tool_used = False
    tool_payload = []

    if not os.path.exists(CHAT_LOG):
        history = []
    else:
        try:
            with open(CHAT_LOG, "r") as file:
                history = json.load(file)
        except Exception as e:
            print(f"[ERR - chat_log]: {e}")
            history = []

    response: ChatResponse = chat(model=MODEL, messages=[
        {
            'role': 'system',
            'content': SYSTEM_MESSAGE
        },
        *history[-5:],
        {
            'role': 'user',
            'content': query
        },
    ], tools=list(TOOLS.values()), stream=False, think=False)

    if response.message.tool_calls:
        for tool in response.message.tool_calls or []:
            try:
                func = TOOLS.get(tool.function.name)
                if func:
                    result = func(**tool.function.arguments)
                    print("TOOL WAS CALLED")
                    tool_payload.append({
                        "tool": tool.function.name,
                        "args": tool.function.arguments,
                        "result": result
                    })
                    tool_used = True
            except Exception as e:
                print(f"[ERR]: {e}")

    if tool_used:
        response: ChatResponse = chat(
            model=MODEL, # or MODEL_SMALL
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_MESSAGE # or SYSTEM_MESSAGE_SMALL
                },
                history[-5:], # --> No history required if using MODEL_SMALL, do give for better results
                {
                    "role": "assistant",
                    "tool_calls": response.message.tool_calls
                },
                {
                    "role": "tool",
                    "content": json.dumps(tool_payload)
                }
            ], stream=False, think=False)

    history.append({"role": "user", "content": query})
    history.append({"role":"assistant","content":response.message.content})
    history = history[-MAX_HISTORY:]

    with open(CHAT_LOG, "w") as file:
        json.dump(history, file, indent=2)

    return response.message.content

#*---------- END OF CODE ----------*