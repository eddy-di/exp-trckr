import pytest
from apps.users.serializers import (
    RegisterSerializer,
    MultiFieldTokenObtainPairSerializer,
)
from apps.users.models import User
from rest_framework.exceptions import AuthenticationFailed


@pytest.mark.django_db
def test_register_serializer_validation_success():
    serializer = RegisterSerializer(
        data={
            "email": "new@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
    )
    assert serializer.is_valid()


@pytest.mark.django_db
def test_register_serializer_password_mismatch():
    serializer = RegisterSerializer(
        data={
            "email": "new@example.com",
            "password1": "Strong123!",
            "password2": "Different!",
        }
    )
    assert serializer.is_valid() is False
    assert "Passwords do not match" in str(serializer.errors)


@pytest.mark.django_db
def test_register_serializer_requires_identifier():
    serializer = RegisterSerializer(
        data={
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
    )
    assert serializer.is_valid() is False
    assert "at least one" in str(serializer.errors).lower()


@pytest.mark.django_db
def test_multifield_token_serializer_success():
    user = User.objects.create_user(email="a@b.com", password="TestPass123!")

    serializer = MultiFieldTokenObtainPairSerializer(
        data={"identifier": "a@b.com", "password": "TestPass123!"}
    )
    serializer.is_valid()

    assert "access" in serializer.validated_data
    assert "refresh" in serializer.validated_data


@pytest.mark.django_db
def test_multifield_token_invalid_credentials():
    serializer = MultiFieldTokenObtainPairSerializer(
        data={"identifier": "nosuchuser@example.com", "password": "invalid"}
    )
    with pytest.raises(AuthenticationFailed):
        serializer.is_valid(raise_exception=True)
