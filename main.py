# Contains Agent ---> Model + Tools access

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.redis import RedisSaver
from langchain.agents.middleware import ToolCallLimitMiddleware
from tools import web_search, arxiv_search, calculator
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
import os
import redis


load_dotenv()

#checkpointer = InMemorySaver()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)

#Redis checkpointer
checkpointer = RedisSaver(redis_client=redis_client)
checkpointer.setup()


chat_model = init_chat_model(
    model="qwen/qwen3.8-27b",
    model_provider="groq",
    temperature=0,
)


agent = create_agent(
    model=chat_model,
    tools=[web_search, arxiv_search, calculator],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
    middleware=[
        ToolCallLimitMiddleware(
            run_limit=5,
            exit_behavior="end",
        ),
        ToolCallLimitMiddleware(
            tool_name="arxiv_search",
            run_limit=4,
            exit_behavior="end"
        ),
        ToolCallLimitMiddleware(
            tool_name="web_search",
            run_limit=3,
            exit_behavior="end"
        )
        
    ]
)

result = agent.invoke(
    {
        "messages":
        [
            {
                "role": "user",
                "content": "Give the answer to: (434*343)+121",
            }
        ]
    },
    config={
        "configurable": {
            "thread_id": "research-session-1"
        }
    },
)




for message in result["messages"]:
    print("\n==============================")
    print("MESSAGE TYPE:", type(message).__name__)
    print("CONTENT:", message.content)

    if hasattr(message, "tool_calls") and message.tool_calls:
        print("TOOL CALLS:")

        for tool_call in message.tool_calls:
            print("  Tool:", tool_call["name"])
            print("  Arguments:", tool_call["args"])

# print("\n\nSECOND INVOCATION")
# print(result["messages"][-1].content)
