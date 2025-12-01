import environ
from pathlib import Path

env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

print('BASE_DIR:', BASE_DIR)

environ.Env.read_env(BASE_DIR / ".env")

print('DB_NAME:', env("DB_NAME"))
print('DB_USER:', env("DB_USER"))
print('DB_PASS:', env("DB_PASS"))
print('DB_HOST:', env("DB_HOST"))
print('DB_PORT:', env("DB_PORT"))
# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASS"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
