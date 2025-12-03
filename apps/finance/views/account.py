from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.finance.models.account import Account
from apps.finance.serializers import (
    AccountListSerializer,
    AccountCreateSerializer,
    AccountDetailSerializer,
)

uuid_param = [OpenApiParameter(
    name="id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH,)]


@extend_schema_view(
    list=extend_schema(
        summary="List user accounts",
        description="Returns all non-deleted accounts of the authenticated user.",
        responses=AccountListSerializer(many=True),
        tags=['accounts'],
    ),
    retrieve=extend_schema(
        summary="Retrieve an account",
        responses=AccountDetailSerializer,
        tags=['accounts'],
        parameters=uuid_param,
    ),
    create=extend_schema(
        summary="Create an account",
        request=AccountCreateSerializer,
        responses=AccountDetailSerializer,
        tags=['accounts'],
    ),
    update=extend_schema(
        summary="Update an account",
        request=AccountDetailSerializer,
        responses=AccountDetailSerializer,
        tags=['accounts'],
        parameters=uuid_param,
    ),
    partial_update=extend_schema(
        summary="Partially update an account",
        request=AccountDetailSerializer,
        responses=AccountDetailSerializer,
        tags=['accounts'],
        parameters=uuid_param,
    ),
    destroy=extend_schema(
        summary="Soft delete an account",
        description="Marks the account as deleted instead of physical removal.",
        tags=['accounts'],
        parameters=uuid_param,
    ),
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
