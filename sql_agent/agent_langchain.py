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
from langchain.agents import create_agent
from langchain.tools import tool

from rich.console import Console
from rich.markdown import Markdown

try:
    from sql_agent.tools import (
        get_schema,
        execute_sql,
        get_table_stats as get_stats_func,
    )
except ImportError:
    from tools import get_schema, execute_sql, get_table_stats as get_stats_func

# DB path
DB_PATH = Path(__file__).parent.parent / "data" / "bookstore.db"
DB_URI = f"sqlite:///{DB_PATH}"

USE_OLLAMA = True
USE_CUSTOM_TOOLS = True


@tool
def get_database_schema() -> str:
    """
    Returns the DB schema with tables and columns.
    """
    print("get_database_schema is called")
    return get_schema()


@tool
def query_database(query: str) -> str:
    """Execute a SQL query and return the results.

    Only SELECT queries are allowed. Validation blocks dangerous operations
    like DROP, DELETE, INSERT, UPDATE.

    Args:
        query: Valid SQL SELECT query string

    Returns:
        Query results as a formatted string
    """
    try:
        print("query_database is called")
        results = execute_sql(query)
        return str(results)
    except Exception as e:  # pylint: disable=broad-except
        return f"Error executing query: {str(e)}"


@tool
def get_table_statistics(table_name: str) -> str:
    """Get statistics about a database table including row count and column info.

    Args:
        table_name: Name of the table to analyze (e.g., 'books', 'orders', 'customers')

    Returns:
        Table statistics including row count, column info, and data distribution
    """
    print(f"called get_table_statistics for {table_name}")
    try:
        return str(get_stats_func(table_name))
    except Exception as e:  # pylint: disable=broad-except
        return f"Error: {str(e)}. Use get_database_schema to see available tables."


def get_llm(model: str = "gpt-4"):
    """Get the configured LLM (openAI or Ollama)."""
    if USE_OLLAMA:
        return ChatOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            model=model,
            temperature=0,
        )
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


def run_agent_custom(user_question: str, model: str = "qwen2.5:7b") -> str:
    """Run agent with custom tools or fallback to built-in SQL agent.

    Args:
        user_question: Natural language question about the database
        model: LLM model to use (default: qwen2.5:7b)

    Returns:
        Answer as a formatted string
    """
    llm = get_llm(model)
    if USE_CUSTOM_TOOLS:
        tools = [get_database_schema, query_database, get_table_statistics]
        agent_graph = create_agent(
            model=llm,
            tools=tools,
            system_prompt="""You are a helpful SQL database assistant.

IMPORTANT: Before querying or analyzing tables, ALWAYS call get_database_schema first to see what tables and columns are available.

When presenting results:
- Use clear headings
- Format numbers with proper separators
- Highlight key insights
- Keep it concise and scannable""",
            debug=False,
        )
        result = agent_graph.invoke(
            {"messages": [{"role": "user", "content": user_question}]}
        )
        return result["messages"][-1].content

    # Fallback to built-in SQL agent
    db = SQLDatabase.from_uri(DB_URI)
    agent_executor = create_sql_agent(
        llm=llm, db=db, agent_type="tool-calling", verbose=True
    )
    result = agent_executor.invoke({"input": user_question})
    return result["output"]


if __name__ == "__main__":
    # Test questions
    # question = "find the top 3 best selling books with amount earned by the bookstore?"
    # question = "which author was most popular in 2025 and tell how many copies of his books were sold & amount earned by bookstore?"
    # question = "can you help remove all the customers from database?"
    question = "tell me some interesting statistics about table orders"

    print("\n" + "=" * 60)
    print("LangChainSQL Agent")
    print("=" * 60 + "\n")

    # answer = run_agent(question, model="qwen2.5:7b")
    answer = run_agent_custom(question, model="qwen2.5:7b")

    console = Console()
    console.print(Markdown(answer))
