"""
LangChain SQL Agent - Stage 3

Two approaches:
- Built in SQL Agent
- Custom Tools Agent
"""

from pathlib import Path
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent

from langchain.tools import tool

try:
    from sql_agent.tools import get_schema, execute_sql
except ImportError:
    from tools import get_schema, execute_sql

# DB path
DB_PATH = Path(__file__).parent.parent / "data" / "bookstore.db"
DB_URI = f"sqlite:///{DB_PATH}"

USE_OLLAMA = True
USE_CUSTOM_TOOLS = False


@tool
def get_database_schema() -> str:
    """
    Returns the DB schema with tables and columns.
    """
    print("get_database_schema is called")
    return get_schema()


@tool
def query_database(query: str) -> str:
    """
    Execute the SQL query and returns the results.
    (Allows only SELECT queries and validation in stage 2 blocks DROP/DELETE/INSERT)

    Args:
        query: valid SQL select query string

    Returns:
        Query results
    """
    try:
        print("query_database is called")
        results = execute_sql(query)
        return str(results)
    except Exception as e:
        return f"Error: {str(e)}"


def get_llm(model: str = "gpt-4"):
    """Get the configured LLM (openAI or Ollama)."""
    if USE_OLLAMA:
        return ChatOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            model=model,
            temperature=0,
        )
    else:
        return ChatOpenAI(model=model, temperature=0)


def run_agent(user_question: str, model: str = "qwen2.5:7b") -> str:
    """
    LangChain SQL Agent

    - Automatic ReAct loop
    - Built-in SQL tools
    - Error handling
    - Schema discovery

    Args:
        user question: natural language question
        model: LLM model to use

    Returns:
        Answer as string
    """
    llm = get_llm(model)
    db = SQLDatabase.from_uri(DB_URI)
    agent_executor = create_sql_agent(
        llm=llm, db=db, agent_type="tool-calling", verbose=True
    )
    result = agent_executor.invoke({"input": user_question})
    return result["output"]


if __name__ == "__main__":
    question = "find the top 3 best selling books with amount earned by the bookstore?"
    # question = "which author was most popular in 2025 and tell how many copies of his books were sold & amount earned by bookstore?"
    # question = "can you help remove all the customers from database?"
    print("\n" + "=" * 60)
    print("LangChainSQL Agent (stage 3)")
    print("=" * 60 + "\n")

    answer = run_agent(question, model="qwen2.5:7b")
