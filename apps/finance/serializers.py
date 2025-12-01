from rest_framework import serializers
from apps.finance.models import Category


class CategorySerializer(serializers.ModelSerializer):
    is_root = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "parent",
            "is_root",
        ]


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent"]

    def validate_parent(self, parent):
        user = self.context["request"].user

        # Allow parenting under global categories
        if parent and parent.user not in (None, user):
            raise serializers.ValidationError(
                "You cannot attach a category under another user's category."
            )

        return parent
