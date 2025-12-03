from rest_framework import serializers
from apps.finance.models import Category, Account, Transaction


class CategorySerializer(serializers.ModelSerializer):
    is_root = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "parent",
            "is_root",
        ]


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent"]

    def validate_parent(self, parent):
        user = self.context["request"].user

        # Allow parenting under global categories
        if parent and parent.user not in (None, user):
            raise serializers.ValidationError(
                "You cannot attach a category under another user's category."
            )

        return parent


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "type",
            "balance",
            "created_at",
        ]


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "type",
            "balance",
        ]
        read_only_fields = ["id", "balance"]


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "type",
            "balance",
            "created_at",
            "updated_at",
        ]


class TransactionListSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source="account.name", read_only=True)
    category_name = serializers.CharField(
        source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "type",
            "amount",
            "account",
            "account_name",
            "category",
            "category_name",
            "created_at",
        ]


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "category",
            "type",
            "amount",
            "description",
        ]
        read_only_fields = ["id"]

    def validate_account(self, account: Account):
        request = self.context["request"]

        if account.user != request.user:
            raise serializers.ValidationError(
                "You can only use your own accounts."
            )
        return account

    def validate_category(self, category: Category | None):
        if category is None:
            return None

        request = self.context["request"]

        # allow global categories (user=None) OR own categories
        if category.user is not None and category.user != request.user:
            raise serializers.ValidationError(
                "You can only use your own or global categories."
            )
        return category


class TransactionDetailSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source="account.name", read_only=True)
    category_name = serializers.CharField(
        source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "type",
            "amount",
            "account",
            "account_name",
            "category",
            "category_name",
            "description",
            "created_at",
            "updated_at",
        ]
