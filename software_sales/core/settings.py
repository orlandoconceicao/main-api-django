from pathlib import Path
from datetime import timedelta
from decouple import AutoConfig
import dj_database_url
import os

# NÃO LÊ .env LOCAL
config = AutoConfig(search_path=None)

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default=".onrender.com,localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",")]
)


# APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",
    "django_filters",
    "drf_yasg",

    "software_sales.core.apps.CoreConfig",
    "software_sales.courses.apps.CoursesConfig",
]


# MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ROOT
ROOT_URLCONF = "software_sales.core.urls"
WSGI_APPLICATION = "software_sales.core.wsgi.application"
ASGI_APPLICATION = "software_sales.core.asgi.application"


# DATABASE (SÓ RENDER)
DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
}


# TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# STATIC
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# DEFAULT
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# USER MODEL
AUTH_USER_MODEL = "courses.Usuario"


# CORS
CORS_ALLOW_ALL_ORIGINS = True


# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}


# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}


# SWAGGER
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "VALIDATOR_URL": None,
}


# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = ""


# RENDER FIX
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

CSRF_TRUSTED_ORIGINS = [
    "https://software-sales.onrender.com",
]