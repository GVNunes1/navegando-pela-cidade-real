"""Configuração do projeto para desenvolvimento local e Vercel/Supabase."""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
if os.getenv("VERCEL") and SECRET_KEY == "development-only-change-me":
    raise RuntimeError("Configure SECRET_KEY nas variáveis de ambiente da Vercel.")

ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,.vercel.app").split(",") if host.strip()]
CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]
CSRF_TRUSTED_ORIGINS += [origin.strip() for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin.strip()]
if os.getenv("VERCEL_URL"):
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ['VERCEL_URL']}")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "boituvaplaces.apps.BoituvaplacesConfig",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "piplaces.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "piplaces.wsgi.application"

DATABASE_URL = os.getenv("DATABASE_URL")
if os.getenv("VERCEL") and not DATABASE_URL:
    raise RuntimeError("Configure DATABASE_URL do Supabase nas variáveis da Vercel.")
DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL or f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=0,
        conn_health_checks=True,
        ssl_require=bool(DATABASE_URL),
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {"staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"}}
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = bool(os.getenv("VERCEL"))
CSRF_COOKIE_SECURE = bool(os.getenv("VERCEL"))
SECURE_SSL_REDIRECT = bool(os.getenv("VERCEL"))
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
