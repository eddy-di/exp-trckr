from django.db import models
from common.models import BaseModel


class Account(BaseModel):
    class AccountType(models.TextChoices):
        MAIN = "main", "Main"
        SAVINGS = "savings", "Savings"
        CASH = "cash", "Cash"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    name = models.CharField(max_length=100)

    type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.MAIN,
        db_index=True,
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    class Meta:
        db_table = "accounts"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "type"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.type})"
