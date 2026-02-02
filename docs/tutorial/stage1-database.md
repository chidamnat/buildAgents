# Stage 1: Database Setup

**Goal:** Create a SQLite database with realistic bookstore data.

**Time:** 30 min | **Level:** Beginner

## What We're Building

A bookstore database with 3 tables:

- `customers` - Who buys books
- `books` - Inventory
- `orders` - Purchase records

## Quick Start

```bash
# Install dependencies
pip install faker factory-boy

# Create database
python -m sql_agent.database
```

## Two Approaches

### Option 1: Simple (Learning)

Hardcode a few records to understand the structure:

```python
books = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "Classic", 12.99, 50),
    Book(2, "1984", "George Orwell", "Dystopian", 14.99, 30),
]
```

**Pros:** Easy to understand, no dependencies
**Cons:** Tedious for large datasets

### Option 2: Factory Boy + Faker (Recommended)

Generate realistic test data automatically:

```python
class BookFactory(factory.Factory):
    class Meta:
        model = Book

    id = factory.LazyFunction(lambda: random.randint(10000, 1000000))
    title = factory.Faker("sentence", nb_words=4)
    author_name = factory.Faker("name")
    genre = factory.LazyFunction(
        lambda: random.choice(["thriller", "fiction", "technology"])
    )
    price = factory.LazyFunction(lambda: round(random.uniform(10.0, 101.5), 2))
    stock = factory.LazyFunction(lambda: random.randint(1, 100))
```

**Pros:** Scalable, realistic data, industry standard
**Cons:** Slight learning curve

**Full code:** [`sql_agent/models/book.py`](https://github.com/chidamnat/buildAgents/blob/main/sql_agent/models/book.py)

## Database Schema

```python
# sql_agent/database.py
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    genre TEXT,
    price REAL,
    stock INTEGER
)
```

Similar tables for `customers` and `orders` with foreign keys.

**Full schema:** [`sql_agent/database.py`](https://github.com/chidamnat/buildAgents/blob/main/sql_agent/database.py)

## Data Generation

```python
# sql_agent/data_prep.py
def generate_sample_data(num_books=20, num_customers=20, num_orders=30):
    books = list(generate_books(num_books))
    customers = list(generate_customers(num_customers))
    orders = list(generate_orders(num_orders, books, customers))
    return books, customers, orders
```

Uses generators for memory efficiency with large datasets.

**Full code:** [`sql_agent/data_prep.py`](https://github.com/chidamnat/buildAgents/blob/main/sql_agent/data_prep.py)

## Verify Your Database

```bash
sqlite3 data/bookstore.db

SELECT COUNT(*) FROM books;     # Should see 15-20 books
SELECT COUNT(*) FROM customers; # Should see 10-20 customers
SELECT COUNT(*) FROM orders;    # Should see 20-30 orders
```

## Key Concepts

**Factory Pattern**
Separates object creation from usage. Change data generation without touching database code.

**Faker**
Generates realistic fake data (names, emails, dates). Essential for testing.

**Foreign Keys**
`orders.customer_id → customers.id` ensures referential integrity.

## Common Issues

!!! warning "Module Not Found"
    Run as module: `python -m sql_agent.database` from project root.

!!! tip "Import Errors with Factories"
    Ensure `sql_agent/__init__.py` exists (can be empty).

## Next Step

Database ready! Move to [Stage 2: Basic Agent](stage2-basic-agent.md) to query it with natural language.
