# Stage 4: Custom Tools with LangChain

**Goal:** Extend LangChain agents with custom tools beyond built-in capabilities.

**Time:** 45-60 min | **Level:** Intermediate-Advanced

## What We're Building

```
Stage 3: Built-in SQL agent (limited to framework tools)
Stage 4: Custom tool agent (add YOUR tools)

New capability: get_table_statistics()
- Row counts
- Column info & types
- Min/max/avg for numeric columns
- Null value counts
```

## Why Custom Tools?

**Stage 3 limitation:** Built-in `create_sql_agent` only provides:
- `sql_db_query` - Execute SELECT queries
- `sql_db_schema` - Get table schemas
- `sql_db_list_tables` - List available tables

**What if you need:**
- Table statistics (our example)
- Data validation rules
- Custom business logic
- Integration with external APIs
- Specialized data transformations

**Solution:** Create custom tools with `@tool` decorator!

## Quick Start

```bash
python -m sql_agent.agent_langchain
# Uses run_agent_custom() with custom tools
```

## Code Comparison

### Stage 3: Built-in Agent
```python
from langchain_community.agent_toolkits import create_sql_agent

llm = ChatOpenAI(...)
db = SQLDatabase.from_uri(DB_URI)
agent = create_sql_agent(llm, db, agent_type="tool-calling")
result = agent.invoke({"input": question})
```
Can't add custom tools but easy to use

### Stage 4: Custom Tools Agent
```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def get_table_statistics(table_name: str) -> str:
    """Get statistics about a database table."""
    return str(get_stats_func(table_name))

tools = [get_database_schema, query_database, get_table_statistics]
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful SQL assistant..."
)
result = agent.invoke({"messages": [{"role": "user", "content": question}]})
```
Full control over tools and extensible

## Building Custom Tools: The Journey

### Step 1: Define Custom Tools with `@tool`

```python
from langchain.tools import tool

@tool
def get_database_schema() -> str:
    """Returns the DB schema with tables and columns."""
    return get_schema()

@tool
def query_database(query: str) -> str:
    """Execute a SQL query and return results.

    Args:
        query: Valid SQL SELECT query string
    """
    try:
        results = execute_sql(query)
        return str(results)
    except Exception as e:
        return f"Error executing query: {str(e)}"

@tool
def get_table_statistics(table_name: str) -> str:
    """Get statistics about a database table.

    Args:
        table_name: Name of the table to analyze
    """
    try:
        return str(get_stats_func(table_name))
    except Exception as e:
        return f"Error: {str(e)}. Use get_database_schema to see available tables."
```

**Key Points:**
- `@tool` decorator makes functions agent-compatible
- Docstrings become tool descriptions (LLM reads these!)
- Args section helps LLM understand parameters
- Return strings (agents work with text)

### Step 2: The API Evolution Challenge
After few attempts at fumbling with older LangChain API, the newest one works with `create_agent`
**What Actually Works:** 
```python
from langchain.agents import create_agent

# Good to check what's available (depending on your version)
from langchain import agents
print(dir(agents))
# ['AgentState', 'create_agent', 'factory', 'middleware', 'structured_output']

# Use create_agent - returns a ready-to-use graph
agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt="...",
    debug=True
)

# Invoke directly (no AgentExecutor needed!)
result = agent_graph.invoke(
    {"messages": [{"role": "user", "content": question}]}
)
answer = result["messages"][-1].content
```

### Step 3: Tool Error Handling

**Problem:** Tools that raise exceptions crash the agent.

**Bad:**
```python
@tool
def get_table_statistics(table_name: str) -> str:
    return str(get_stats_func(table_name))  # Raises if table doesn't exist
```

**Test it:**
```python
question = "Show me statistics for the sales table"
# Exception: Table sales does not exist
# Agent crashes completely
```

**Good:** Return error messages instead
```python
@tool
def get_table_statistics(table_name: str) -> str:
    try:
        return str(get_stats_func(table_name))
    except Exception as e:
        return f"Error: {str(e)}. Use get_database_schema to see available tables."
```

**Now it works:**
```python
question = "Show me statistics for the sales table"
# Agent sees: "Error: Table sales does not exist. Use get_database_schema..."
# Agent calls get_database_schema to see available tables
# Agent responds: "The available tables are: books, customers, orders..."
# Graceful recovery!
```

### Step 4: System Prompts Matter

**Without guidance:**
```python
system_prompt="You are a helpful SQL database assistant."
```
Result: Agent might skip calling `get_database_schema` and guess table names.

**With guidance:**
```python
system_prompt="""You are a helpful SQL database assistant.

IMPORTANT: Before querying or analyzing tables, ALWAYS call get_database_schema
first to see what tables and columns are available.

When presenting results:
- Use clear headings
- Format numbers with proper separators
- Highlight key insights
- Keep it concise and scannable"""
```
Result: Agent checks schema first, avoids errors.

```
The table orders contains 20 rows and has the following columns:

• id: An integer column that serves as the primary key...
• customer_id: An integer column with values ranging from...
• total_amount: A real number column representing...
```

## Key Differences: Built-in vs Custom

| Aspect | Stage 3 (Built-in) | Stage 4 (Custom) |
|--------|-------------------|------------------|
| **Setup** | `create_sql_agent()` | `create_agent()` |
| **Tools** | Framework-provided | You define with `@tool` |
| **API** | Stable, simple | Version-dependent |
| **Flexibility** | Low | High |
| **Error handling** | Built-in | You implement |
| **Input format** | `{"input": question}` | `{"messages": [...]}` |
| **Output format** | `result["output"]` | `result["messages"][-1].content` |
| **Use case** | Standard SQL queries | Custom functionality |

## Code Structure

```python
# 1. Import
from langchain.agents import create_agent
from langchain.tools import tool

# 2. Define tools
@tool
def my_custom_tool(arg: str) -> str:
    """Tool description for LLM."""
    try:
        return do_something(arg)
    except Exception as e:
        return f"Error: {str(e)}"

# 3. Create agent
tools = [tool1, tool2, tool3]
agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt="Instructions for the agent...",
    debug=True
)

# 4. Invoke
result = agent_graph.invoke(
    {"messages": [{"role": "user", "content": question}]}
)
answer = result["messages"][-1].content
```

## Common Issues & Solutions


!!! warning "Agent crashes on tool errors"
    **Cause:** Tool raises exception instead of returning error string
    **Fix:** Add try/except in tools, return error messages
    ```python
    try:
        return process(data)
    except Exception as e:
        return f"Error: {str(e)}"
    ```

!!! warning "Agent doesn't call get_database_schema first"
    **Cause:** System prompt doesn't instruct to check schema
    **Fix:** Add "IMPORTANT: Before querying, ALWAYS call get_database_schema first"

## When to Use Each Approach

### Use Built-in Agent (Stage 3) when:
- Standard SQL queries are enough
- You want simplicity
- You trust framework tools
- Prototyping quickly

### Use Custom Tools (Stage 4) when:
- Need functionality beyond built-in tools
- Want control over tool behavior
- Integrating with external systems
- Implementing business logic
- Need custom error handling
- Building domain-specific agents

## Real-World Example

**Question:** "Tell me some interesting statistics about table orders"

**Agent execution:**
```
1. Calls: get_database_schema()
   Response: "Database Schema: ..."

2. Calls: get_table_statistics("orders")
   Response: {"table_name": "orders", "row_count": 20, "columns": [...]}

3. Final answer (formatted):
   The table orders contains 20 rows and has the following columns:
   • id: Integer (1-20, avg: 10.5)
   • customer_id: Integer (119,188-905,613, avg: 398,034.9)
   • quantity: Integer (1-3, avg: 1.85)
   • total_amount: Real ($30.64-$287.28, avg: $114.29)
```



## Try These

```python
# Works - custom tool provides rich stats
"Tell me interesting statistics about table orders"

# Works - graceful error handling
"Show statistics for the sales table"
# Agent: "Table doesn't exist. Available: books, customers, orders"

# Works - agent combines tools
"Which table has the most rows?"
# Calls get_database_schema, then get_table_statistics for each table
```
---

**Full code:** [`sql_agent/agent_langchain.py`](../../sql_agent/agent_langchain.py)

**Compare:** gent()` (Stage 3) vs `run_agent_custom()` (Stage 4) in the same file to see the differences!
