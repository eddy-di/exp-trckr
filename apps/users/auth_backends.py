from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User


class MultiIdentifierBackend(ModelBackend):
    """
    Authenticate using email, username, or phone
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        try:
            user = User.objects.get(
                Q(email=username) |
                Q(username=username) |
                Q(phone=username)
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active and not user.is_deleted:
            return user

        return None
