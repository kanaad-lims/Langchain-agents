## Contains the tools available to the Agent

from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import arxiv

@tool
def web_search(query: str) -> str:
    """
    Search the internet for current or up-to-date information.
    
    Use this tool when the user asks about recent events,
    current information, news, or facts that may have changed.
    """
    search = DuckDuckGoSearchRun()
    answer = search.invoke(query)
    return answer

@tool
def arxiv_search(query: str) -> dict:
    """
    Search the arXiv repository for papers.
    """
    try:
        search = arxiv.Search(
            query=query,
            max_results=1,
            sort_by=arxiv.SortCriterion.Relevance
        )

        client = arxiv.Client()

        paper = {}

        for result in client.results(search):
            paper = {
                "title": result.title.strip(),
                "summary": result.summary.strip()
            }

        return paper

    except Exception as e:
        print(f"[ERROR] arxiv fetch failed: {e}")
        return {}

@tool
def calculator(expression: str) -> str:
    """
    Evaluate mathematical expression.
    """

    try:
        return str(f"Answer is: {eval(expression)}")
    except Exception as e:
        return f"Error evaluating the expression: {e}"

if __name__ == "__main__":
    #result = web_search.invoke("Latest Trends in Agentic AI")
    #result = arxiv_search.invoke("OmniScientist")
    result = calculator.invoke("2 * 8")
    print(result)