from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from apps.finance.models import Category
from apps.finance.serializers import CategorySerializer, CategoryCreateUpdateSerializer
from apps.finance.permissions import IsOwnerOrReadOnlyGlobal


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyGlobal]

    def get_queryset(self):
        user = self.request.user

        return Category.objects.filter(
            Q(user=user) | Q(user__isnull=True),
            is_deleted=False,
        ).select_related("parent")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CategoryCreateUpdateSerializer
        return CategorySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # ✅ Soft delete instead of hard delete
        instance.soft_delete()
