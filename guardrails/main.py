from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from guards import InputGuardrails, OutputGuardrails
from prompts import SYSTEM_PROMPT

load_dotenv()

chat_model = init_chat_model(
    model="groq:qwen/qwen3.8-27b",
    temperature=0,
)

agent = create_agent(
    model=chat_model,
    tools=[],
    system_prompt=SYSTEM_PROMPT,
    middleware=[
        InputGuardrails(blocked_words=["hack", "malware", "bypass"]),
        OutputGuardrails(),
    ],
)


result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Search topic in reinforcement learning for agentic ai.",
            }
        ]
    }
)


print(result["messages"][-1].content)