from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import MultiFieldTokenObtainPairSerializer, RegisterResponseSerializer, RegisterSerializer


class MultiFieldTokenObtainPairView(TokenObtainPairView):
    serializer_class = MultiFieldTokenObtainPairSerializer


@extend_schema(
    summary="User registration",
    description=(
        "Register a new user using email, username and/or phone. "
        "Returns JWT access and refresh tokens immediately after successful registration."
    ),
    request=RegisterSerializer,
    responses={
        201: RegisterResponseSerializer,
        400: OpenApiTypes.OBJECT,
    },
)
class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # ✅ Issue JWT immediately after registration
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "username": user.username,
                    "phone": user.phone,
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )
