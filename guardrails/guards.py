from langchain.agents.middleware import AgentMiddleware

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

