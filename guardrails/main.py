from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from guards import InputGuardrails, OutputGuardrails, ToolGuardrails
from prompts import SYSTEM_PROMPT
from tools import read_files, delete_files

load_dotenv()

chat_model = init_chat_model(
    model="groq:qwen/qwen3.8-27b",
    temperature=0,
)

agent = create_agent(
    model=chat_model,
    tools=[read_files, delete_files],
    system_prompt=SYSTEM_PROMPT,
    middleware=[
        InputGuardrails(blocked_words=["hack", "malware", "bypass"]),
        OutputGuardrails(),
        ToolGuardrails(),
    ],
)


result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Delete file budgetstructure.md located at E:/Home/Kanaad/businessdocs.",
            }
        ]
    }
)

for message in result["messages"]:
    print("\nTYPE:", type(message).__name__)
    print("CONTENT:", message.content)

    if hasattr(message, "tool_calls"):
        print("TOOL CALLS:", message.tool_calls)


