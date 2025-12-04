import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.mark.django_db
class TestAuthAPI:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="test@example.com",
            password="TestPass123!",
            username="tester",
            phone="996554123456"
        )

    #
    # REGISTER API
    #
    def test_register_success(self, client):
        url = "/api/v1/auth/register/"

        payload = {
            "email": "new@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        response = client.post(url, payload, format="json")

        assert response.status_code == 201
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["email"] == "new@example.com"

        assert User.objects.filter(email="new@example.com").exists()

    def test_register_password_mismatch(self, client):
        url = "/api/v1/auth/register/"

        payload = {
            "email": "wrong@example.com",
            "password1": "Pass123!",
            "password2": "DIFFERENT!",
        }

        response = client.post(url, payload, format="json")

        assert response.status_code == 400
        assert "Passwords do not match" in str(response.data)

    def test_register_requires_identifier(self, client):
        url = "/api/v1/auth/register/"

        payload = {
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        response = client.post(url, payload, format="json")

        assert response.status_code == 400
        assert "email, username or phone" in str(response.data).lower()

    #
    # LOGIN API
    #
    def test_login_with_email(self, client, user):
        url = reverse('token_obtain_pair')

        payload = {
            "identifier": "test@example.com",
            "password": "TestPass123!",
        }

        response = client.post(url, payload, format="json")

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["email"] == "test@example.com"

    def test_login_with_username(self, client, user):
        url = reverse('token_obtain_pair')

        payload = {
            "identifier": "tester",
            "password": "TestPass123!",
        }

        response = client.post(url, payload, format="json")

        assert response.status_code == 200
        assert response.data["user"]["username"] == "tester"

    def test_login_with_phone(self, client, user):
        print('user:', user)
        print('user.phone:', user.phone)
        url = reverse('token_obtain_pair')

        payload = {
            "identifier": '996554123456',
            "password": "TestPass123!",
        }

        response = client.post(url, payload, format="json")

        assert response.status_code == 200
        assert response.data["user"]["phone"] == "996554123456"

    def test_login_invalid_credentials(self, client, user):
        url = reverse('token_obtain_pair')

        payload = {
            "identifier": "test@example.com",
            "password": "WRONGPASSWORD",
        }

        response = client.post(url, payload, format="json")

        assert response.status_code == 401
        assert "Invalid credentials" in str(response.data)

    def test_login_inactive_user(self, client):
        user = User.objects.create_user(
            email="inactive@example.com",
            password="TestPass123!"
        )
        user.is_active = False
        user.save()

        url = reverse('token_obtain_pair')

        response = client.post(url, {
            "identifier": "inactive@example.com",
            "password": "TestPass123!"
        })

        assert response.status_code == 401
        assert "invalid credentials" in str(response.data).lower()

    #
    # TOKEN REFRESH
    #
    def test_token_refresh(self, client, user):
        token_url = "/api/v1/auth/token/"

        login = client.post(token_url, {
            "identifier": "test@example.com",
            "password": "TestPass123!",
        }, format="json")

        refresh = login.data["refresh"]

        refresh_url = "/api/v1/auth/token/refresh/"
        response = client.post(
            refresh_url, {"refresh": refresh}, format="json")

        assert response.status_code == 200
        assert "access" in response.data

    #
    # TOKEN VERIFY
    #
    def test_token_verify(self, client, user):
        token_url = "/api/v1/auth/token/"

        login = client.post(token_url, {
            "identifier": "test@example.com",
            "password": "TestPass123!",
        })

        access = login.data["access"]

        verify_url = "/api/v1/auth/token/verify/"
        response = client.post(verify_url, {"token": access}, format="json")

        assert response.status_code == 200
