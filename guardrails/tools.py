from langchain.tools import tool
from pathlib import Path

PROXY_DIR = Path("proxy_dir.txt").resolve()

# writing harmless tool and harmful tool

@tool

def read_files(filename: str) -> str:
    """
    Read the content of the file
    """
    return f"Content of the {filename} are: This is a sample file!"


@tool
def delete_files(filename: str) -> str:
    """
    Delete the targeted file
    """
    return f"File {filename} deleted successfully!"