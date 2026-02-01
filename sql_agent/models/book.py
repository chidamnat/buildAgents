import factory
import random


class Book:
    """A simple Book model."""

    def __init__(self, id, title, author_name, genre, price, stock):
        self.id = id
        self.title = title
        self.author_name = author_name
        self.genre = genre
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"'{self.title}' by {self.author_name} (genre - {self.genre}) (price - {self.price}) (stock available - {self.stock})"

    def __repr__(self):
        return f"'{self.title}' by {self.author_name} (genre - {self.genre}) (price - {self.price}) (stock available - {self.stock})"


class BookFactory(factory.Factory):
    """Factory to create instances of the Book class."""

    class Meta:
        model = Book

    id = factory.LazyFunction(lambda: random.randint(10000, 1000000))
    title = factory.Faker("sentence", nb_words=4)
    author_name = factory.Faker("name")
    genre = factory.LazyFunction(
        lambda: random.choice(
            ["thriller", "fiction", "non-fiction", "textbook", "technology"]
        )
    )
    price = factory.LazyFunction(lambda: round(random.uniform(10.0, 101.5), 2))
    stock = factory.LazyFunction(lambda: random.randint(1, 100))
