"""
Tools that the SQL agent can use to interact with the database.

In the ReAct pattern, these are the "Actions" the agent can take.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any

# path to bookstore DB
DB_PATH = Path(__file__).parent.parent / "data" / "bookstore.db"


def get_schema() -> str:
    """
    Returns a description of the DB schema.

    This tool will help the agent understand what tables and columns exist.
    The agent will call this first to know what data is available.

    Returns:
        String description of all tables and their columns
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name from sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """
    )
    tables = cursor.fetchall()
    schema_description = "Database Schema:\n\n"

    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema_description += f"Table: {table_name}\n"
        schema_description += "Columns:\n"

        for col in columns:
            # col format: (id, name, type, notnull)
            col_name = col[1]
            col_type = col[2]
            is_pk = " (PRIMARY KEY)" if col[5] else ""
            schema_description += f". - {col_name}: {col_type}{is_pk}\n"

        schema_description += "\n"

    conn.close()
    return schema_description


def validate_query(query: str) -> tuple[bool, str]:
    """
    Validates if sql query is safe to execute.

    Args:
        query: SQL query

    Returns:
        Tuple of (is_valid, error_message)
        - if valid: (True, "")
        - if invalid: (False, "reason why")
    """
    query_upper = query.upper().strip()
    # dangerous sql keywords
    dangerous_keywords = [
        "DROP",
        "DELETE",
        "TRUNCATE",
        "INSERT",
        "UPDATE",
        "ALTER",
        "CREATE",
        "REPLACE",
    ]

    if not query_upper.startswith("SELECT") or query_upper.startswith("WITH"):
        return False, "Only SELECT queries and CTEs are allowed"

    for keyword in dangerous_keywords:
        if keyword in query_upper:
            return False, f"Dangerous keyword {keyword} not allowed"

    # check for any prompt injection attack
    if "--" in query or "/*" in query:
        return False, "SQL comments are not allowed"

    return True, ""


def execute_sql(query: str) -> List[Dict[str, Any]]:
    """
    executes sql

    Args:
        query: sql query to be executed

    Returns:
        List of dictionaries (each dict is a row with col_names as keys)
    """
    # validate the query
    is_valid, error_msg = validate_query(query)
    if not is_valid:
        raise Exception(f"Invalid query {error_msg}")

    conn = sqlite3.connect(DB_PATH)
    # makes rows accessible as dict instead of tuples
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        conn.close()
        return results
    except Exception as e:
        conn.close()
        raise Exception(f"SQL Error: {str(e)}")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_sql",
            "description": "Executes a SQL SELECT query on the bookstore database and returns the result. Only use SELECT queries - no INSERT, UPDATE, or DELETE.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "THE SQL SELECT query to execute. Example: 'SELECT * FROM customers LIMIT 5'",
                    }
                },
                "required": ["query"],
            },
        },
    },
]

AVAILABLE_FUNCTIONS = {"get_schema": get_schema, "execute_sql": execute_sql}
# print(execute_sql("SELECT * FROM books"))
