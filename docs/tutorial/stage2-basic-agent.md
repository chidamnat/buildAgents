# Stage 2: Basic SQL Agent

**Goal:** Build a ReAct agent that converts natural language to SQL queries.

**Time:** 1-2 hours | **Level:** Intermediate

## What We're Building

```
User: "Who are my top 5 customers by revenue?"
     ↓
Agent: Thinks → Generates SQL → Executes → Returns answer
```

## Architecture

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       ↓
┌──────────────────┐
│   LLM (Qwen)     │ ← Has database schema
└──────┬───────────┘
       ↓
┌──────────────────┐
│  Function Call   │ → execute_sql(query)
└──────┬───────────┘
       ↓
┌──────────────────┐
│   SQL Result     │
└──────┬───────────┘
       ↓
┌──────────────────┐
│  Natural Answer  │
└──────────────────┘
```

## The ReAct Loop

```python
# sql_agent/agent_basic.py
def run_agent(user_question: str) -> str:
    messages = [system_prompt, user_question]

    for iteration in range(max_iterations):
        # 1. Reason - LLM decides what to do
        response = client.chat.completions.create(
            model="qwen2.5:7b",
            messages=messages,
            tools=TOOLS
        )

        # 2. Act - Execute tool if needed
        if response.tool_calls:
            for tool_call in response.tool_calls:
                result = execute_function(tool_call)
                messages.append(result)
        else:
            return response.content  # Final answer
```

**Full code:** [`sql_agent/agent_basic.py`](https://github.com/chidamnat/buildAgents/blob/main/sql_agent/agent_basic.py)

## Building Blocks

### 1. Tools Definition

Tell the LLM what functions it can use:

```python
# sql_agent/tools.py
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_sql",
            "description": "Executes a SQL SELECT query and returns results",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL SELECT query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]
```

### 2. Security Validation

**Critical:** Never trust LLM-generated SQL blindly!

```python
def validate_query(query: str) -> tuple[bool, str]:
    query_upper = query.upper().strip()

    # Only allow SELECT
    if not query_upper.startswith("SELECT"):
        return False, "Only SELECT queries allowed"

    # Block dangerous keywords
    dangerous = ["DROP", "DELETE", "INSERT", "UPDATE"]
    for keyword in dangerous:
        if keyword in query_upper:
            return False, f"Dangerous keyword {keyword} blocked"

    # Prevent SQL injection
    if "--" in query or "/*" in query:
        return False, "SQL comments not allowed"

    return True, ""
```

**Full code:** [`sql_agent/tools.py`](https://github.com/chidamnat/buildAgents/blob/main/sql_agent/tools.py)

### 3. Schema Caching

Give the LLM context about available tables:

```python
schema = get_schema()  # Fetch once, cache globally

system_prompt = f"""You are a SQL agent for a bookstore database.

DATABASE SCHEMA:
{schema}

Generate and execute SQL queries using execute_sql() to answer questions."""
```

## Using Open Source Models

### OpenAI (Requires API key)

```python
from openai import OpenAI
client = OpenAI()  # Uses OPENAI_API_KEY env var
```

### Ollama (Free, runs locally)

```python
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Dummy, not needed
)

# Use models like qwen2.5:7b, llama3.1:8b
```

**Setup:** Install from [ollama.com](https://ollama.com), then `ollama pull qwen2.5:7b`

## Test It

```python
# sql_agent/agent_basic.py
if __name__ == "__main__":
    question = "Show me the top 3 customers by total spending"
    answer = run_agent(question)
    print(answer)
```

Run:
```bash
python -m sql_agent.agent_basic
```

## Example Execution

```
--- Iteration 1 ---
Tool call: execute_sql({
  "query": "SELECT c.name, SUM(o.total_amount) as total
            FROM customers c JOIN orders o ON c.id = o.customer_id
            GROUP BY c.name ORDER BY total DESC LIMIT 3"
})
Result: [{"name": "Alice", "total": 234.50}, ...]

--- Iteration 2 ---
Final answer: The top 3 customers are:
1. Alice - $234.50
2. Bob - $189.23
3. Carol - $156.78
```

## Key Concepts

**ReAct Pattern**
Reasoning + Acting in a loop. Agent thinks, acts, observes, repeats.

**Function Calling**
LLM outputs structured JSON to trigger tool execution. Not just text generation!

**Security-First**
Always validate LLM outputs. They can hallucinate or be prompt-injected.

## Common Issues

!!! warning "Query Validation Failing"
    Check if your query has comments (`--`) or forbidden keywords.

!!! tip "Agent Exceeds Max Iterations"
    Increase `max_iterations` or improve system prompt clarity.

!!! danger "Security Test"
    Try: "Remove the customers table" - Should be blocked!

## Try These Queries

- "What are the 5 most expensive books?"
- "Which author has the most books in stock?"
- "Show total revenue by genre"
- "Find customers who haven't ordered in 60 days"

## Next Step

Working basic agent! Next: [Stage 3: LangChain Version](stage3-langchain.md) to see what frameworks provide (coming soon).
