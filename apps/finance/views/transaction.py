from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.db import transaction as db_transaction

from apps.finance.models import Transaction
from apps.finance.serializers import (
    TransactionListSerializer,
    TransactionCreateSerializer,
    TransactionDetailSerializer,
)

uuid_param = [OpenApiParameter(
    name="id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH,)]


@extend_schema_view(
    list=extend_schema(
        summary="List transactions",
        description="Returns all user transactions.",
        responses=TransactionListSerializer(many=True),
        tags=['transactions'],
    ),
    retrieve=extend_schema(
        summary="Retrieve a transaction",
        responses=TransactionDetailSerializer,
        tags=['transactions'],
        parameters=uuid_param,
    ),
    create=extend_schema(
        summary="Create a transaction",
        request=TransactionCreateSerializer,
        responses=TransactionDetailSerializer,
        tags=['transactions'],
    ),
    update=extend_schema(
        summary="Update a transaction",
        request=TransactionDetailSerializer,
        responses=TransactionDetailSerializer,
        tags=['transactions'],
        parameters=uuid_param,
    ),
    partial_update=extend_schema(
        summary="Partially update a transaction",
        request=TransactionDetailSerializer,
        responses=TransactionDetailSerializer,
        tags=['transactions'],
        parameters=uuid_param,
    ),
    destroy=extend_schema(
        summary="Soft delete a transaction",
        tags=['transactions'],
        parameters=uuid_param,
    ),
)
class TransactionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user,
            is_deleted=False,
        ).select_related("account", "category")

    def get_serializer_class(self):
        if self.action == "list":
            return TransactionListSerializer
        if self.action == "create":
            return TransactionCreateSerializer
        return TransactionDetailSerializer

    @db_transaction.atomic
    def perform_create(self, serializer):
        transaction_obj = serializer.save(user=self.request.user)

        account = transaction_obj.account
        amount = transaction_obj.amount

        if transaction_obj.type == Transaction.TransactionType.INCOME:
            account.balance += amount
        else:  # EXPENSE
            account.balance -= amount

        account.save(update_fields=["balance"])

    @db_transaction.atomic
    def perform_destroy(self, instance):
        account = instance.account
        amount = instance.amount

        # ✅ Reverse the original operation
        if instance.type == Transaction.TransactionType.INCOME:
            account.balance -= amount
        else:  # EXPENSE
            account.balance += amount

        account.save(update_fields=["balance"])

        instance.soft_delete()
