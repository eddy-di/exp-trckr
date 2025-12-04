import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.finance.tests.factories import (
    UserFactory,
    CategoryFactory,
    GlobalCategoryFactory,
)
from apps.finance.models import Category


@pytest.mark.django_db
class TestCategoryAPI:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def auth_client(self, client, user):
        client.force_authenticate(user)
        return client

    #
    # LIST: user should receive global + their own categories
    #
    def test_list_categories_includes_global_and_own(self, auth_client, user):
        own_categories = CategoryFactory.create_batch(3, user=user)
        global_categories = GlobalCategoryFactory.create_batch(2)

        url = reverse("category-list")
        response = auth_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 5

        returned_ids = {c["id"] for c in response.data}
        assert all(c.id in returned_ids for c in own_categories +
                   global_categories)

    #
    # RETRIEVE
    #
    def test_retrieve_category(self, auth_client, user):
        cat = CategoryFactory(user=user)

        url = reverse("category-detail", args=[cat.id])
        response = auth_client.get(url)

        assert response.status_code == 200
        assert response.data["id"] == cat.id
        assert response.data["name"] == cat.name

    #
    # CREATE (root category)
    #
    def test_create_category(self, auth_client, user):
        url = reverse("category-list")

        payload = {
            "name": "New Category",
            "parent": None
        }

        response = auth_client.post(url, payload, format="json")
        assert response.status_code == 201

        created = Category.objects.get(id=response.data["id"])
        assert created.user == user
        assert created.name == "New Category"
        assert created.parent is None

    #
    # CREATE with global parent category
    #
    def test_create_category_under_global_parent(self, auth_client, user):
        parent = GlobalCategoryFactory()

        url = reverse("category-list")
        payload = {"name": "Child", "parent": parent.id}

        response = auth_client.post(url, payload, format="json")
        assert response.status_code == 201

    #
    # CREATE forbidden: parent belongs to another user
    #
    def test_create_category_parent_belongs_to_other_user_forbidden(self, auth_client, user):
        foreign_parent = CategoryFactory()  # Different user

        url = reverse("category-list")
        payload = {"name": "Child", "parent": foreign_parent.id}

        response = auth_client.post(url, payload, format="json")
        assert response.status_code == 400
        assert "another user's category" in str(response.data).lower()

    #
    # UPDATE: allowed for user-owned category
    #
    def test_update_category(self, auth_client, user):
        cat = CategoryFactory(user=user)

        url = reverse("category-detail", args=[cat.id])
        payload = {"name": "Updated Name", "parent": None}

        response = auth_client.put(url, payload, format="json")
        assert response.status_code == 200

        cat.refresh_from_db()
        assert cat.name == "Updated Name"

    #
    # UPDATE forbidden on global category (IsOwnerOrReadOnlyGlobal)
    #
    def test_update_global_category_forbidden(self, auth_client):
        global_cat = GlobalCategoryFactory()

        url = reverse("category-detail", args=[global_cat.id])
        payload = {"name": "Should Fail", "parent": None}

        response = auth_client.put(url, payload, format="json")

        # Should be 403 Forbidden
        assert response.status_code == 403

    #
    # PARTIAL UPDATE
    #
    def test_partial_update_category(self, auth_client, user):
        cat = CategoryFactory(user=user)

        url = reverse("category-detail", args=[cat.id])
        payload = {"name": "Partial Update"}

        response = auth_client.patch(url, payload, format="json")
        assert response.status_code == 200

        cat.refresh_from_db()
        assert cat.name == "Partial Update"

    #
    # DESTROY (soft delete)
    #
    def test_destroy_category_soft_delete(self, auth_client, user):
        cat = CategoryFactory(user=user)

        url = reverse("category-detail", args=[cat.id])
        response = auth_client.delete(url)
        assert response.status_code == 204

        cat.refresh_from_db()
        assert cat.is_deleted is True

    #
    # Deleted categories should not appear in list()
    #
    def test_list_excludes_deleted(self, auth_client, user):
        cat = CategoryFactory(user=user)
        cat.soft_delete()

        url = reverse("category-list")
        response = auth_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 0
