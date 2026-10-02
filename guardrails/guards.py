from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import ToolMessage

class InputGuardrails(AgentMiddleware):

    def __init__(self, blocked_words):
        self.blocked_words = blocked_words

    def before_agent(self, state, runtime):
        
        print("INPUT GUARDRAIL ACTIVE")
        messages = state["messages"]
        user_messages = messages[0].content.lower()

        for word in self.blocked_words:
            if word.lower() in user_messages:
                raise ValueError("Input blocked by the guardrail.")

        return None


class OutputGuardrails(AgentMiddleware):

    def after_agent(self, state, runtime):
        print("OUTPUT GUARDRAIL ACTIVE")
        return None

class ToolGuardrails(AgentMiddleware):

    def wrap_tool_call(self, request, handler):

        tool_name = request.tool_call["name"]
        banned_tools = ["delete_files"]

        print(f"[GUARDRAIL] Tool requested: {tool_name}")

        # Block dangerous tool calls
        if tool_name in banned_tools:
            print("[GUARDRAIL] Blocked")

            return ToolMessage(
                content="Tool call blocked by security policy!",
                tool_call_id = request.tool_call["id"]
            )

        print("[GUARDRAIL] Allowed!")

        return handler(request)