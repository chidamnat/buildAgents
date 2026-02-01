import random
from typing import Generator
from models.book import BookFactory
from models.customer import CustomerFactory
from models.order import OrderFactory


def generate_books(num_books=10) -> Generator:
    print("Generating books")
    for _ in range(num_books):
        yield BookFactory.create()


def generate_customers(num_customers=5):
    print("Generating customers")
    for _ in range(num_customers):
        yield CustomerFactory.create()


def generate_orders(num_orders, books, customer_ids):
    print("Generating orders")
    book_ids = [book.id for book in books]
    prices = [book.price for book in books]
    for _ in range(num_orders):
        book_idx = random.randint(0, len(books) - 1)
        yield OrderFactory.create(
            book_id=book_ids[book_idx],
            customer_id=random.choice(customer_ids),
            book_price=prices[book_idx],
        )


def generate_sample_data(num_books=20, num_customers=20, num_orders=30):
    books = list(generate_books(num_books))
    customers = list(generate_customers(num_customers))
    customer_ids = [customer.id for customer in customers]
    orders = list(generate_orders(num_orders, books, customer_ids))
    return books, customers, orders


if __name__ == "__main__":
    generate_sample_data()
