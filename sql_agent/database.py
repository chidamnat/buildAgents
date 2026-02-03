"""
Database setup for SQL Agent learning project.

We're creating a simple online bookstore database with:
- Customers (people who buys books)
- Books (inventory)
- Orders (purchases)
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

try:
    from sql_agent.data_prep import generate_sample_data
except ImportError:
    from data_prep import generate_sample_data

# Database file location
DB_PATH = Path(__file__).parent.parent / "data" / "bookstore.db"
print(DB_PATH)


def create_database():
    """
    Creates the database and all tables.
    Steps:
    1. Connect to SQLite database (creates file if dont exist)
    2. Create three tables: customers, books, orders
    3. Close connection
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customers(
            id integer primary key,
            name text,
            email text,
            signup_date text,
            country text
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books(
            id integer primary key,
            title text,
            author text,
            genre text,
            price real,
            stock integer
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders(
            id integer primary key,
            customer_id integer,
            book_id integer,
            quantity integer,
            order_date text,
            total_amount real,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
        """
    )

    conn.commit()
    conn.close()

    print(f"Database created as {DB_PATH}")


def insert_sample_data():
    """
    Inserts sample data into all tables.
        - 10 customers
        - 15 books
        - 20 orders
    """
    books, customers, orders = generate_sample_data(
        num_books=15, num_customers=10, num_orders=20
    )
    # print(orders)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for book in books:
        cursor.execute(
            """
            INSERT into books (id, title, author, genre, price, stock)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (book.id, book.title, book.author_name, book.genre, book.price, book.stock),
        )

    for customer in customers:
        cursor.execute(
            """
            INSERT into customers (id, name, email, signup_date, country)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                customer.id,
                customer.name,
                customer.email,
                customer.signup_date,
                customer.country,
            ),
        )

    for order in orders:
        cursor.execute(
            """
            INSERT INTO orders (customer_id, book_id, quantity, order_date, total_amount)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                order.customer_id,
                order.book_id,
                order.quantity,
                str(order.order_date),
                order.total_amount,
            ),
        )

    conn.commit()
    conn.close()

    print(
        f"Inserted {len(books)} books, {len(customers)} customers, {len(orders)} orders"
    )


create_database()
insert_sample_data()
