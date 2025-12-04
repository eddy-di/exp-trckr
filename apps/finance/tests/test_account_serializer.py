import pytest
from apps.finance.serializers import (
    AccountListSerializer,
    AccountCreateSerializer,
    AccountDetailSerializer,
)
from apps.finance.tests.factories import AccountFactory


@pytest.mark.django_db
def test_account_list_serializer():
    acc = AccountFactory()
    data = AccountListSerializer(acc).data

    assert set(data.keys()) == {"id", "name", "type", "balance", "created_at"}


@pytest.mark.django_db
def test_account_create_serializer():
    acc = AccountFactory.build()
    serializer = AccountCreateSerializer(acc)

    assert "id" in serializer.fields
    assert "balance" in serializer.fields
    assert serializer.fields["id"].read_only is True
    assert serializer.fields["balance"].read_only is True


@pytest.mark.django_db
def test_account_detail_serializer():
    acc = AccountFactory()
    data = AccountDetailSerializer(acc).data

    assert "updated_at" in data
    assert data["name"] == acc.name
