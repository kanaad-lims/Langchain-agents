from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()
completion = client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[
      {
        "role": "user",
        "content": "Will u use the tools available to you? I wil be giving u access to tools and based on the query, u will decide which tool is to be used. Will u be able to do that?"
      }
    ],
    temperature=0,
    max_completion_tokens=2048,
    top_p=1,
    reasoning_effort="default",
    stream=True,
    stop=None
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
