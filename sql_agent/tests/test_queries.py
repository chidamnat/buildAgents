import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "bookstore.db"
print(DB_PATH)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn):
    conn.close()


def execute_and_display(cursor, sql, title):
    """Helper to run query and display results nicely."""
    print(f"\n{'='*50}")
    print(f"{title}")
    print("=" * 50)

    rows = cursor.execute(sql).fetchall()
    columns = [desc[0] for desc in cursor.description]
    print(" | ".join(columns))
    print("-" * 50)

    for row in rows:
        print(" | ".join(str(val) for val in row))

    print(f"\nTotal: {len(rows)} rows\n")


def see_all_books(cursor):
    sql = "SELECT * FROM books LIMIT 5;"
    execute_and_display(cursor, sql, "See all books")


def find_expensive_books(cursor):
    sql = "SELECT title, author, price FROM books ORDER BY price DESC LIMIT 5;"
    execute_and_display(cursor, sql, "find expensive books")


def view_customer_order_history(cursor):
    sql = """
        SELECT customers.name, books.title, orders.quantity, orders.total_amount
        FROM orders
        JOIN customers
          ON orders.customer_id = customers.id
        JOIN books
          ON orders.book_id = books.id
        LIMIT 5;
    """
    execute_and_display(cursor, sql, "view customer order history")


def total_sales_by_genre(cursor):
    sql = """
        SELECT books.genre, sum(orders.total_amount) as total_sales
        FROM orders
        JOIN books 
          ON orders.book_id = books.id
        GROUP BY 1
        ORDER BY 2 DESC;
    """
    execute_and_display(cursor, sql, "total sale by genre")


conn, cursor = get_connection()
see_all_books(cursor)
find_expensive_books(cursor)
view_customer_order_history(cursor)
total_sales_by_genre(cursor)
close_connection(conn)
