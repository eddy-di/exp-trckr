from django.db import models
from common.models import BaseModel


class Transaction(BaseModel):
    class TransactionType(models.TextChoices):
        EXPENSE = "expense", "Expense"
        INCOME = "income", "Income"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    account = models.ForeignKey(
        "finance.Account",
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    category = models.ForeignKey(
        "finance.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )

    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        db_index=True,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    description = models.TextField(blank=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "type"]),
            models.Index(fields=["account"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.type.upper()} | {self.amount}"
