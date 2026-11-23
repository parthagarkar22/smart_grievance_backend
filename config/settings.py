
from pathlib import Path
from datetime import timedelta
import os
import sys
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# =========================
# GDAL / GEOS
# =========================
# Windows local: use Program Files paths if present.
# Linux (Oracle/Render): set GDAL_LIBRARY_PATH / GEOS_LIBRARY_PATH in env, or leave unset.
if sys.platform.startswith("win"):
    GDAL_LIBRARY_PATH = os.getenv(
        "GDAL_LIBRARY_PATH", r"C:\Program Files\GDAL\gdal.dll"
    )
    GEOS_LIBRARY_PATH = os.getenv(
        "GEOS_LIBRARY_PATH", r"C:\Program Files\GDAL\geos_c.dll"
    )
else:
    if os.getenv("GDAL_LIBRARY_PATH"):
        GDAL_LIBRARY_PATH = os.getenv("GDAL_LIBRARY_PATH")
    if os.getenv("GEOS_LIBRARY_PATH"):
        GEOS_LIBRARY_PATH = os.getenv("GEOS_LIBRARY_PATH")

# =========================
# BASIC CONFIG
# =========================
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if h.strip()
]
if "*" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("*")


# =========================
# INSTALLED APPS
# =========================
INSTALLED_APPS = [
    # Django default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # GIS (PostGIS)
    'django.contrib.gis',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_beat',
    'rest_framework_simplejwt',
    "corsheaders",

    # Local apps
    'apps.accounts.apps.AccountsConfig',
    'apps.departments',
    'apps.grievances',
    'apps.dashboard',
    'apps.feedback',
    'apps.notifications',
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # MUST BE FIRST
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# =========================
# DATABASE
# Prefer DATABASE_URL (Supabase / cloud). Fall back to discrete DB_* vars (local).
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            engine="django.contrib.gis.db.backends.postgis",
            conn_max_age=600,
            ssl_require=os.getenv("DB_SSL_REQUIRE", "True") == "True",
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': os.getenv("DB_NAME", "smart_grievance"),
            'USER': os.getenv("DB_USER", "postgres"),
            'PASSWORD': os.getenv("DB_PASSWORD", "super123"),
            'HOST': os.getenv("DB_HOST", "localhost"),
            'PORT': os.getenv("DB_PORT", "5433"),
        }
    }

# =========================
# AUTH USER MODEL
# =========================
AUTH_USER_MODEL = 'accounts.User'

# =========================
# PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# REST FRAMEWORK + JWT
# =========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=3000),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# =========================
# LANGUAGE & TIME
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# =========================
# STATIC & MEDIA
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# REDIS + CELERY
# =========================
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Free-tier friendly: run tasks in-process when Redis/Celery worker is unavailable
CELERY_TASK_ALWAYS_EAGER = os.getenv("CELERY_TASK_ALWAYS_EAGER", "False") == "True"
CELERY_TASK_EAGER_PROPAGATES = True

# =========================
# CELERY BEAT
# =========================
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# =========================
# CORS / CSRF
# =========================
# Comma-separated origins, e.g.
# FRONTEND_ORIGINS=http://localhost:5173,https://your-app.vercel.app
_frontend_origins = [
    o.strip()
    for o in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if o.strip()
]

CORS_ALLOWED_ORIGINS = _frontend_origins
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    o for o in _frontend_origins if o.startswith("https://") or o.startswith("http://")
]

# Also trust the public backend URL if set (for admin / forms)
_backend_public = os.getenv("BACKEND_PUBLIC_URL", "").strip()
if _backend_public and _backend_public not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(_backend_public)

# =========================
# EMAIL
# =========================
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "noreply@localhost")
