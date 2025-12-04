import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

from common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, username=None, password=None, **extra_fields):
        if not email and not phone and not username:
            raise ValueError(
                "Either email, username, or phone must be provided")

        if email:
            email = self.normalize_email(email)
            extra_fields["email"] = email

        if phone:
            extra_fields['phone'] = phone

        if username:
            extra_fields['username'] = username

        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not email:
            raise ValueError("Superuser must have an email")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom User model for Expense Tracker
    """

    # ✅ All three identifiers
    email = models.EmailField(unique=True,
                              blank=True, db_index=True)
    username = models.CharField(
        max_length=150, unique=True, null=True, blank=True, db_index=True)
    phone = models.CharField(max_length=20, unique=True,
                             null=True, blank=True, db_index=True)

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    currency = models.CharField(max_length=3, default="USD")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # email & password only

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        if self.email:
            return self.email
        if self.username:
            return self.username
        else:
            return self.phone

    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "is_active", "deleted_at"])

    def restore(self):
        """
        Restores a soft-deleted object.
        """
        self.is_deleted = False
        self.is_active = True
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "is_active", "deleted_at"])
