import pytest
from apps.users.models import User
from django.utils import timezone


@pytest.mark.django_db
class TestUserModel:

    def test_str_email(self):
        user = User.objects.create_user(email="a@b.com", password="pass")
        assert str(user) == "a@b.com"

    def test_str_username(self):
        user = User.objects.create_user(username="tester", password="pass")
        assert str(user) == "tester"

    def test_str_phone(self):
        user = User.objects.create_user(phone="12345", password="pass")
        assert str(user) == "12345"

    def test_soft_delete(self):
        user = User.objects.create_user(email="a@b.com", password="pass")
        user.soft_delete()

        user.refresh_from_db()
        assert user.is_deleted is True
        assert user.is_active is False
        assert user.deleted_at is not None

    def test_restore(self):
        user = User.objects.create_user(email="a@b.com", password="pass")
        user.soft_delete()

        user.restore()
        user.refresh_from_db()

        assert user.is_deleted is False
        assert user.is_active is True
        assert user.deleted_at is None

    def test_create_user_requires_identifier(self):
        with pytest.raises(ValueError):
            User.objects.create_user(password="pass")

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@site.com",
            password="Admin123!"
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.is_active is True
