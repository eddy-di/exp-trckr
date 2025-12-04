import pytest
from django.urls import reverse
from decimal import Decimal
from rest_framework.test import APIClient

from apps.finance.tests.factories import (
    UserFactory,
    AccountFactory,
    CategoryFactory,
    GlobalCategoryFactory,
    TransactionFactory,
)
from apps.finance.models import Transaction


@pytest.mark.django_db
class TestTransactionAPI:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def auth_client(self, client, user):
        client.force_authenticate(user)
        return client

    #
    # LIST
    #
    def test_list_transactions(self, auth_client, user):
        TransactionFactory.create_batch(3, user=user)
        TransactionFactory.create_batch(2)  # other user

        url = reverse("transaction-list")
        response = auth_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 3

    #
    # RETRIEVE
    #
    def test_retrieve_transaction(self, auth_client, user):
        tx = TransactionFactory(user=user)

        url = reverse("transaction-detail", args=[tx.id])
        response = auth_client.get(url)

        assert response.status_code == 200
        assert response.data["id"] == str(tx.id)

    #
    # CREATE — positive (INCOME increases balance)
    #
    def test_create_transaction_income_increases_balance(self, auth_client, user):
        account = AccountFactory(user=user, balance=Decimal("100.00"))
        category = CategoryFactory(user=user)

        url = reverse("transaction-list")

        payload = {
            "account": str(account.id),
            "category": str(category.id),
            "type": "income",
            "amount": "50.00",
            "description": "Test income"
        }

        response = auth_client.post(url, payload, format="json")
        assert response.status_code == 201

        account.refresh_from_db()
        assert account.balance == Decimal("150.00")

    #
    # CREATE — EXPENSE decreases balance
    #
    def test_create_transaction_expense_decreases_balance(self, auth_client, user):
        account = AccountFactory(user=user, balance=Decimal("200.00"))

        url = reverse("transaction-list")

        payload = {
            "account": str(account.id),
            "category": None,
            "type": "expense",
            "amount": "75.00",
            "description": "",
        }

        response = auth_client.post(url, payload, format="json")
        assert response.status_code == 201

        account.refresh_from_db()
        assert account.balance == Decimal("125.00")

    #
    # VALIDATION — cannot use another user's account
    #
    def test_create_transaction_other_user_account_forbidden(self, auth_client, user):
        other_account = AccountFactory()  # belongs to someone else

        url = reverse("transaction-list")

        payload = {
            "account": str(other_account.id),
            "category": None,
            "type": "income",
            "amount": "10.00",
            "description": "",
        }

        response = auth_client.post(url, payload, format="json")
        assert response.status_code == 400
        assert "own accounts" in str(response.data).lower()

    #
    # VALIDATION — cannot use another user's category (unless global)
    #
    def test_create_transaction_other_user_category_forbidden(self, auth_client, user):
        account = AccountFactory(user=user)
        other_category = CategoryFactory()  # belongs to another user

        url = reverse("transaction-list")

        payload = {
            "account": str(account.id),
            "category": str(other_category.id),
            "type": "income",
            "amount": "10.00",
            "description": "",
        }

        response = auth_client.post(url, payload, format="json")
        assert response.status_code == 400
        assert "own or global categories" in str(response.data).lower()

    #
    # VALIDATION — GLOBAL category is allowed
    #
    def test_create_transaction_global_category_allowed(self, auth_client, user):
        account = AccountFactory(user=user)
        global_category = GlobalCategoryFactory()  # user=None

        url = reverse("transaction-list")

        payload = {
            "account": str(account.id),
            "category": str(global_category.id),
            "type": "income",
            "amount": "20.00",
            "description": "",
        }

        response = auth_client.post(url, payload, format="json")
        assert response.status_code == 201

    #
    # DESTROY — soft delete restores balance
    #
    def test_destroy_transaction_restores_balance(self, auth_client, user):
        account = AccountFactory(user=user, balance=Decimal("100.00"))

        tx = TransactionFactory(
            user=user,
            account=account,
            type=Transaction.TransactionType.EXPENSE,
            amount=Decimal("40.00")
        )

        # Apply initial balance impact manually (your system does this on create)
        account.balance -= Decimal("40.00")
        account.save()

        url = reverse("transaction-detail", args=[tx.id])
        response = auth_client.delete(url)

        assert response.status_code == 204

        account.refresh_from_db()
        assert account.balance == Decimal("100.00")

        tx.refresh_from_db()
        assert tx.is_deleted is True
