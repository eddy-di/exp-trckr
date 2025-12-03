from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User


class RegisterResponseSerializer(serializers.Serializer):
    user = serializers.DictField()
    access = serializers.CharField()
    refresh = serializers.CharField()


class MultiFieldTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Login with email OR username OR phone + password.

    Frontend sends:
      {
        "identifier": "...",   # email / username / phone
        "password": "..."
      }
    """

    # This tells DRF which field to expect instead of "username"/"email"
    username_field = "identifier"

    def validate(self, attrs):
        identifier = attrs.get(self.username_field)
        password = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError(
                "Identifier and password are required.")

        # Use your MultiIdentifierBackend (it takes username=identifier)
        user = authenticate(
            request=self.context.get("request"),
            username=identifier,
            password=password,
        )

        if user is None:
            raise AuthenticationFailed("Invalid credentials.")

        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        # Same token generation logic as SimpleJWT's TokenObtainPairSerializer
        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        # (optional) include some user info
        data["user"] = {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "phone": user.phone,
        }

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone",
            "password1",
            "password2",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")

        validate_password(password1)

        # Require at least ONE identifier
        if not attrs.get("email") and not attrs.get("username") and not attrs.get("phone"):
            raise serializers.ValidationError(
                "At least one of email, username or phone is required."
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password1")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save(update_fields=["password"])

        return user
