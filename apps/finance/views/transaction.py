from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.finance.models import Transaction
from apps.finance.serializers import (
    TransactionListSerializer,
    TransactionCreateSerializer,
    TransactionDetailSerializer,
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
