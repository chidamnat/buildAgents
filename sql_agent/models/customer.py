import factory
import random


class Customer:
    """A simple Customer model."""

    def __init__(self, id, name, email, signup_date, country):
        self.id = id
        self.name = name
        self.email = email
        self.signup_date = signup_date
        self.country = country

    def __str__(self):
        return f"{self.name} ({self.email}) (signup date - {self.signup_date}) from {self.country}"

    def __repr__(self):
        return f"{self.name} ({self.email}) (signup date - {self.signup_date}) from {self.country}"


class CustomerFactory(factory.Factory):
    """Factory to create instances of the Customer class."""

    class Meta:
        model = Customer

    id = factory.LazyFunction(lambda: random.randint(10000, 1000000))
    name = factory.Faker("name")
    email = factory.Faker("email")
    signup_date = factory.Faker("date")
    country = factory.Faker("country")
