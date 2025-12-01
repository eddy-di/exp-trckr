from django.db import models
from common.models import BaseModel


class Category(BaseModel):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=100)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",   # ✅ reverse access
    )

    class Meta:
        db_table = "categories"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name", "parent"],
                name="uniq_user_category_per_level",
            )
        ]

    def __str__(self):
        return self.name

    @property
    def is_root(self) -> bool:
        return self.parent_id is None
