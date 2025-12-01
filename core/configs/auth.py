AUTHENTICATION_BACKENDS = [
    "apps.users.auth_backends.MultiIdentifierBackend",
]

AUTH_USER_MODEL = "users.User"
