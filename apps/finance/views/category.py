from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.finance.models import Category
from apps.finance.serializers import CategorySerializer, CategoryCreateUpdateSerializer
from apps.finance.permissions import IsOwnerOrReadOnlyGlobal

int_id = [OpenApiParameter(
    name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH,)]


@extend_schema_view(
    list=extend_schema(
        summary="List categories",
        description="Returns global and user-specific categories.",
        responses=CategorySerializer(many=True),
        tags=['categories'],
    ),
    retrieve=extend_schema(
        summary="Retrieve a category",
        responses=CategorySerializer,
        tags=['categories'],
        parameters=int_id,
    ),
    create=extend_schema(
        summary="Create a category",
        request=CategorySerializer,
        responses=CategorySerializer,
        tags=['categories'],
    ),
    update=extend_schema(
        summary='Update a category',
        request=CategoryCreateUpdateSerializer,
        responses=CategorySerializer,
        tags=['categories'],
        parameters=int_id,
    ),
    partial_update=extend_schema(
        summary='Partially update a category',
        request=CategoryCreateUpdateSerializer,
        responses=CategorySerializer,
        tags=['categories'],
        parameters=int_id,
    ),
    destroy=extend_schema(
        summary="Soft delete a category",
        tags=['categories'],
        parameters=int_id,
    ),
)
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
