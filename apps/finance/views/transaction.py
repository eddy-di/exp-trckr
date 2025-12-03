from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # ✅ Soft delete instead of physical delete
        instance.soft_delete()
