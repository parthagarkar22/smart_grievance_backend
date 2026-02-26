
from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# =========================
# GDAL / GEOS (Windows GIS)
# =========================
# GDAL_LIBRARY_PATH = r"C:\Program Files\GDAL\gdal.dll"
# GEOS_LIBRARY_PATH = r"C:\Program Files\GDAL\geos_c.dll"

# =========================
# BASIC CONFIG
# =========================
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS =["smart-grievance-system-n2xn.onrender.com", "*"]
# ALLOWED_HOSTS = []


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
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",   # MUST be near top
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
# DATABASE (Local PostgreSQL + PostGIS)
# =========================
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': os.getenv("DB_NAME", "smart_grievance"),
#         'USER': os.getenv("DB_USER", "postgres"),
#         'PASSWORD': os.getenv("DB_PASSWORD", "super123"),
#         'HOST': os.getenv("DB_HOST", "localhost"),
#         'PORT': os.getenv("DB_PORT", "5433"),
#     }
# }

# =========================
# DATABASE (Render PostgreSQL + PostGIS)
# =========================
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': os.getenv("DB_NAME", "smart_grievance_db"),
#         'USER': os.getenv("DB_USER", "smart_grievance_db_user"),
#         'PASSWORD': os.getenv("DB_PASSWORD", "c0YHEHCC0XURvpgtfHApqs859OnBvMMU"),
#         'HOST': os.getenv("DB_HOST", "dpg-d6cllgq4d50c73a6s5t0-a"),
#         'PORT': os.getenv("DB_PORT", "5432"),
#     }
# }

# =========================
# DATABASE (Using dj_database_url)
# =========================
import dj_database_url

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get(
            "DATABASE_URL",
            "postgresql://smart_grievance_db_user:c0YHEHCC0XURvpgtfHApqs859OnBvMMU@dpg-d6cllgq4d50c73a6s5t0-a.singapore-postgres.render.com/smart_grievance_db"
        ),
        engine="django.contrib.gis.db.backends.postgis"
    )
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

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# REDIS + CELERY
# =========================
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# =========================
# CELERY BEAT
# =========================
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# =========================
# EMAIL
# =========================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# =========================
# OPTIONAL OPEN ACCESS MODE
# =========================
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.AllowAny',
#     ),
# }

# =========================
# CORS
# =========================
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
# ]


# CORS_ALLOW_ALL_ORIGINS = True


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://front-end-smart-grievance-system.vercel.app/",
]