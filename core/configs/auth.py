AUTHENTICATION_BACKENDS = [
    "apps.users.auth_backends.MultiIdentifierBackend",
    # "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "users.User"
