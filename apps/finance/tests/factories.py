from decimal import Decimal
import factory
from factory.django import DjangoModelFactory
from apps.finance.models.account import Account
from apps.finance.models.category import Category
from apps.finance.models.transaction import Transaction
from apps.users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Account {n}")
    type = "main"
    balance = Decimal("100.00")


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Category {n}")


class GlobalCategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    user = None
    name = factory.Sequence(lambda n: f"Global Category {n}")


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    account = factory.SubFactory(
        AccountFactory, user=factory.SelfAttribute("..user"))
    category = factory.SubFactory(
        CategoryFactory, user=factory.SelfAttribute("..user"))
    type = Transaction.TransactionType.INCOME
    amount = Decimal("50.00")
    description = "Test transaction"
