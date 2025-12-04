import pytest
from apps.finance.serializers import (
    CategorySerializer,
    CategoryCreateUpdateSerializer,
)
from apps.finance.tests.factories import (
    CategoryFactory,
    GlobalCategoryFactory,
    UserFactory,
)


@pytest.mark.django_db
def test_category_serializer_fields():
    cat = CategoryFactory()
    data = CategorySerializer(cat).data

    assert set(data.keys()) == {"id", "name", "parent", "is_root"}


@pytest.mark.django_db
def test_category_is_root_property():
    root = CategoryFactory(parent=None)
    child = CategoryFactory(parent=root)

    root_data = CategorySerializer(root).data
    child_data = CategorySerializer(child).data

    assert root_data["is_root"] is True
    assert child_data["is_root"] is False


@pytest.mark.django_db
def test_category_create_serializer_valid_parent__ok_for_global():
    user = UserFactory()
    parent = GlobalCategoryFactory()

    serializer = CategoryCreateUpdateSerializer(
        data={"name": "Child", "parent": parent.id},
        context={"request": type("obj", (), {"user": user})()},
    )

    assert serializer.is_valid()


@pytest.mark.django_db
def test_category_create_serializer_invalid_parent_of_other_user():
    user = UserFactory()
    other_parent = CategoryFactory()  # Another user's category

    serializer = CategoryCreateUpdateSerializer(
        data={"name": "Child", "parent": other_parent.id},
        context={"request": type("obj", (), {"user": user})()},
    )

    assert serializer.is_valid() is False
    assert "cannot attach" in str(serializer.errors).lower()
