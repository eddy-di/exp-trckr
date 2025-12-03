from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.finance.models.account import Account
from apps.finance.serializers import (
    AccountListSerializer,
    AccountCreateSerializer,
    AccountDetailSerializer,
)


class AccountViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(
            user=self.request.user,
            is_deleted=False,
        )

    def get_serializer_class(self):
        if self.action == "list":
            return AccountListSerializer
        if self.action == "create":
            return AccountCreateSerializer
        return AccountDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # ✅ Soft delete only
        instance.soft_delete()
