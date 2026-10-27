"""
Django settings for SHP Restaurant Management System backend.
"""

from pathlib import Path
from datetime import timedelta
import os
import sys
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from backend/.env first, then root .env if present
load_dotenv(BASE_DIR / '.env')
load_dotenv(BASE_DIR.parent / '.env')

# Add apps folder to sys.path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 't')

_INSECURE_DEV_SECRET = 'shp-restro-insecure-dev-secret-key-change-in-prod-2026'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', _INSECURE_DEV_SECRET if DEBUG else '')
if not SECRET_KEY:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(
        'DJANGO_SECRET_KEY must be set in the environment when DJANGO_DEBUG is off.'
    )

ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    'DJANGO_ALLOWED_HOSTS', '*'
).split(',') if h.strip()]

INSTALLED_APPS = [
    'daphne',  # Must be before django.contrib.staticfiles for ASGI
    'jazzmin',  # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party packages
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_spectacular',
    'channels',

    # Internal project apps
    'apps.authentication',
    'apps.restaurants',
    'apps.menu',
    'apps.tables',
    'apps.orders',
    'apps.reservations',
    'apps.customers',
    'apps.promotions',
    'apps.analytics',
    'apps.notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
ASGI_APPLICATION = 'config.asgi.application'

DATABASE_URL = os.getenv('DATABASE_URL', '')
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600),
        }
    except ImportError:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            'DATABASE_URL is set but dj-database-url is not installed. '
            'Run: pip install dj-database-url'
        )
else:
    # SQLite is for local development only — set DATABASE_URL (Postgres) in production.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'authentication.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('DJANGO_TIME_ZONE', 'Asia/Kolkata')
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # Secure by default: every endpoint requires authentication unless a view
    # explicitly opts into public access (see IsAuthenticatedOrReadOnly / AllowAny overrides).
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/min',
        'user': '1000/min',
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# SimpleJWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_MINUTES', '60'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_REFRESH_DAYS', '1'))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS Settings
# Never allow all origins together with credentials in production. Default to an
# allowlist; only enable the wildcard explicitly (dev) via env.
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False').lower() in ('true', '1', 't')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost(:[0-9]+)?$",
    r"^http://127.0.0.1(:[0-9]+)?$",
    r"^https:\/\/.*\.shptechnology\.online$",
]
_extra_cors = os.getenv('CORS_ALLOWED_ORIGINS', '')
CORS_ALLOWED_ORIGINS = [o.strip() for o in _extra_cors.split(',') if o.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()]

# Channels Layer & Redis Cache configuration
_TESTING = 'test' in sys.argv
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
if _TESTING:
    # Tests run without external services.
    CHANNEL_LAYERS = {'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
elif REDIS_URL:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [REDIS_URL],
            },
        },
    }
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer'
        }
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# Razorpay Payment Gateway Configuration (no insecure fallbacks — must be set in env)
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')
RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET', '')

# ==============================================================================
# PRODUCTION SECURITY (active whenever DEBUG is off)
# ==============================================================================
if not DEBUG:
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() in ('true', '1', 't')
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# Static files: WhiteNoise for compressed, hashed serving in production (optional dep).
try:
    import whitenoise  # noqa: F401
    MIDDLEWARE.insert(
        MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1,
        'whitenoise.middleware.WhiteNoiseMiddleware',
    )
    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
    }
except ImportError:
    pass

# DRF Spectacular OpenAPI documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'SHP Restaurant Management API',
    'DESCRIPTION': 'RESTful API & WebSockets for POS, Kitchen KDS, Table & Party Booking and Online Delivery',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ==============================================================================
# JAZZMIN THEME CONFIGURATION
# ==============================================================================
JAZZMIN_SETTINGS = {
    # Title & Branding
    "site_title": "SHP Restro Admin",
    "site_header": "SHP Restro",
    "site_brand": "SHP Restaurant OS",
    "site_logo": "img/logo.png",
    "site_icon": "img/favicon.png",
    "login_logo": "img/logo.png",
    "welcome_sign": "Welcome to SHP Restaurant Operating System",
    "copyright": "SHP Technology Ltd",
    
    # Global search model configuration
    "search_model": ["orders.Order", "customers.Customer", "menu.MenuItem", "reservations.TableReservation"],
    
    # Top navigation links
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "API Docs", "url": "/api/docs/", "new_window": True},
        {"name": "Live POS & Web", "url": "http://localhost:5173", "new_window": True},
    ],
    
    # Sidebar navigation & Layout (Clean, non-cluttered structure)
    "show_sidebar": True,
    "navigation_expanded": False,
    "order_with_respect_to": [
        "orders",
        "reservations",
        "tables",
        "menu",
        "customers",
        "promotions",
        "restaurants",
        "authentication",
    ],
    
    # Icons for Models
    "icons": {
        "authentication.User": "fas fa-user-shield",
        "restaurants.Restaurant": "fas fa-store-alt",
        "menu.Category": "fas fa-layer-group",
        "menu.MenuItem": "fas fa-utensils",
        "tables.RestaurantTable": "fas fa-chair",
        "orders.Order": "fas fa-receipt",
        "orders.OrderItem": "fas fa-hamburger",
        "reservations.TableReservation": "fas fa-calendar-check",
        "reservations.PartyBooking": "fas fa-glass-cheers",
        "customers.Customer": "fas fa-users",
        "promotions.Offer": "fas fa-tags",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-dot-circle",
    
    # Form experience
    "changeform_format": "horizontal_tabs",
    "related_modal_active": True,
    "custom_css": "css/admin-custom.css",
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "default_theme_mode": "auto",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}



