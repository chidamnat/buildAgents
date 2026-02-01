import factory
import random


class Order:
    """A simple order model"""

    def __init__(self, customer_id, book_id, quantity, order_date, book_price):
        self.customer_id = customer_id
        self.book_id = book_id
        self.quantity = quantity
        self.order_date = order_date
        self.total_amount = quantity * book_price

    def __str__(self):
        return (
            f"{self.book_id} (quantity: {self.quantity}) "
            f"ordered for {self.total_amount} on {self.order_date}"
        )

    def __repr__(self):
        return (
            f"{self.book_id} (quantity: {self.quantity}) "
            f"ordered for {self.total_amount} on {self.order_date}"
        )


class OrderFactory(factory.Factory):
    """Factory to create instances of the Order class."""

    class Meta:
        model = Order

    customer_id = factory.LazyFunction(lambda: random.randint(1, 100))
    book_id = factory.LazyFunction(lambda: random.randint(1, 100))
    quantity = factory.LazyFunction(lambda: random.randint(1, 3))
    order_date = factory.Faker("date_between", start_date="-1y", end_date="today")
    # ideally price * quantity
    # total_amount = factory.LazyFunction(lambda: round(random.uniform(10.0, 200.0), 2))
