# Stage 3: LangChain SQL Agent

**Goal:** Rebuild the SQL agent using LangChain to see what frameworks provide.

**Time:** 30-45 min | **Level:** Intermediate

## What We're Building

Same SQL agent as Stage 2, but:
- Less code (~80 lines vs ~110 lines)
- More features (schema validation, uery, schema, list_tables vs just execute_sql)
- Battle-tested reliability
- Built-in security & validation

## Quick Start

```bash
pip install langchain langchain-openai langchain-community langchain-core
python -m sql_agent.agent_langchain
```

## Code Comparison

**Stage 2:** Manual ReAct loop (~110 lines)
```python
for iteration in range(max_iterations):
    response = client.chat.completions.create(...)
    if not response.tool_calls:
        return response.content
    for tool_call in response.tool_calls:
        # Manual tool execution, message management, error handling
```

**Stage 3:** One function call (~80 lines)
```python
llm = ChatOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
agent = create_sql_agent(llm, db, agent_type="tool-calling", verbose=True)
result = agent.invoke({"input": question})  # Everything automatic!
```

## What We Learned Building Stage 3

### 1. Schema Validation Catches Bugs

**The Bug:**
```sql
-- database.py (typo in FK reference)
FOREIGN KEY (customer_id) REFERENCES customer(id)  -- ❌ Should be "customers"
```

**Stage 2:** ✗ Ran fine, bug went unnoticed
**Stage 3:** ✓ Immediate error: `NoSuchTableError: customer`

LangChain uses SQLAlchemy to validate foreign keys, data types, and relationships on startup.

### 2. Security by Design (Not Validation)

**Stage 2 Approach (Blacklist):**
```python
# ~20 lines of validation code
dangerous = ["DROP", "DELETE", "INSERT", "UPDATE"]
if keyword in query: raise Exception("Blocked!")
```
Problem: Might forget keywords or miss edge cases.

**Stage 3 Approach (Whitelist):**
```python
# 0 lines - tools define what's possible
agent = create_sql_agent(...)  # Only SELECT queries allowed
```

**Test it yourself:**
```python
run_agent("Delete all customers from the database")
# Agent responds: "I am only allowed to select data without making
# changes, I can't execute this."
```

Tools provided: `sql_db_query` (SELECT only), `sql_db_schema`, `sql_db_list_tables`
Tools NOT provided: DELETE, INSERT, UPDATE, DROP

**Result:** Dangerous operations are **impossible**, not just blocked.

| Security | Stage 2 | Stage 3 |
|----------|---------|---------|
| **Method** | Blacklist (block bad things) | Whitelist (allow only good things) |
| **Code** | ~20 lines | 0 lines |
| **Safe by default?** | No | Yes |

### 3. Import Structure Matters

When using LangChain as a module, we had to fix imports throughout:

```python
# Before (broke with `python -m sql_agent.database`)
from data_prep import generate_sample_data

# After (works both ways)
try:
    from sql_agent.data_prep import generate_sample_data
except ImportError:
    from data_prep import generate_sample_data
```

Frameworks push you toward better Python packaging practices.

## Key Features

| Feature | Stage 2 | Stage 3 |
|---------|---------|---------|
| **Code size** | 110 lines | 80 lines |
| **Tools** | 1 (execute_sql) | 3 (query, schema, list) |
| **Security** | Manual validation | Impossible by design |
| **Schema validation** | None | FK/type checking |
| **Error handling** | Basic try/catch | Built-in retry |
| **Schema discovery** | Static | Dynamic at runtime |

## Common Issues We Hit

!!! warning "NoSuchTableError: customer"
    **Cause:** Foreign key typo: `REFERENCES customer(id)` instead of `customers(id)`
    **Fix:** LangChain validates schema - fix your FK references!

!!! warning "api_keys is not default parameter"
    **Cause:** Typo `api_keys="ollama"` (plural)
    **Fix:** Use `api_key="ollama"` (singular)

!!! tip "ModuleNotFoundError: No module named 'models'"
    **Cause:** Imports broke when running as module
    **Fix:** Use try/except pattern (see Import Structure above)

## When to Use Each

**Stage 2 (Basic):** Learning, full control, minimal dependencies
**Stage 3 (LangChain):** Production, speed, battle-tested features

## Try These

```python
# Works - better error handling than Stage 2
"Find the top 3 best selling books"

# Fails gracefully - explains why
"Delete all customers"  # Agent: "I can only read data"

# Better errors
"Show me the users table"  # Stage 3: "Table 'users' doesn't exist"
```

## Key Takeaways

1. **Frameworks catch silent bugs** - FK validation found our typo
2. **Security by design > validation** - Whitelist beats blacklist
3. **Less code, more features** - 30% smaller, 200% more capable
4. **Build Stage 2 first** - Understand internals, then use frameworks

---

**Full code:** [`sql_agent/agent_langchain.py`](https://github.com/chidamnat/buildAgents/blob/main/sql_agent/agent_langchain.py)
