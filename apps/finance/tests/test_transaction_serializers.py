import pytest
from decimal import Decimal

from apps.finance.serializers import (
    TransactionListSerializer,
    TransactionDetailSerializer,
    TransactionCreateSerializer,
)
from apps.finance.tests.factories import (
    TransactionFactory,
    AccountFactory,
    CategoryFactory,
    UserFactory,
    GlobalCategoryFactory,
)


@pytest.mark.django_db
def test_transaction_list_serializer_fields():
    tx = TransactionFactory()
    data = TransactionListSerializer(tx).data

    assert set(data.keys()) == {
        "id",
        "type",
        "amount",
        "account",
        "account_name",
        "category",
        "category_name",
        "created_at",
    }


@pytest.mark.django_db
def test_transaction_detail_serializer_fields():
    tx = TransactionFactory()
    data = TransactionDetailSerializer(tx).data

    assert "updated_at" in data
    assert data["account_name"] == tx.account.name


@pytest.mark.django_db
def test_transaction_create_serializer_validates_own_account():
    user = UserFactory()
    other_user_account = AccountFactory()
    category = CategoryFactory(user=user)

    serializer = TransactionCreateSerializer(
        data={
            "account": other_user_account.id,
            "category": category.id,
            "type": "income",
            "amount": "10.00",
        },
        context={"request": type("obj", (), {"user": user})()},
    )

    assert serializer.is_valid() is False
    assert "own accounts" in str(serializer.errors).lower()


@pytest.mark.django_db
def test_transaction_create_serializer_allows_global_category():
    user = UserFactory()
    account = AccountFactory(user=user)
    global_category = GlobalCategoryFactory()

    serializer = TransactionCreateSerializer(
        data={
            "account": account.id,
            "category": global_category.id,
            "type": "income",
            "amount": "10.00",
        },
        context={"request": type("obj", (), {"user": user})()},
    )

    assert serializer.is_valid() is True
