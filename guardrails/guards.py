from langchain.agents.middleware import before_agent

@before_agent
def input_guardrail(state, runtime):
    print("INPUT GUARDRAIL EXECUTED")

    return None

