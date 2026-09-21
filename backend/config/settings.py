"""
Django settings for SHP Restaurant Management System backend.
"""

from pathlib import Path
from datetime import timedelta
import os
import sys
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps folder to sys.path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'shp-restro-insecure-dev-secret-key-change-in-prod-2026')

DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('true', '1', 't')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

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
TIME_ZONE = 'UTC'
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
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# SimpleJWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost(:[0-9]+)?$",
    r"^http://127.0.0.1(:[0-9]+)?$",
    r"^https:\/\/.*\.shptechnology\.online$",
]

# Channels Layer configuration (In-memory for development, configurable for Redis)
REDIS_URL = os.getenv('REDIS_URL')
if REDIS_URL:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [REDIS_URL],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer'
        }
    }

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
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "SHP Restro Admin",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "SHP Restaurant OS",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "SHP Restro",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome to SHP Restaurant Management System",
    # Copyright on the footer
    "copyright": "SHP Technology Ltd",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": ["orders.Order", "customers.Customer", "menu.MenuItem"],
    # Field name on user model that contains avatar ImageField/URLField/CharField or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Open API Docs", "url": "/api/docs/", "new_window": True},
        {"name": "Live Frontend", "url": "http://localhost:5173", "new_window": True},
    ],
    #############
    # Side Menu #
    #############
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    # Icons for apps/models
    "icons": {
        "authentication.User": "fas fa-user-shield",
        "restaurants.Restaurant": "fas fa-store-alt",
        "restaurants.Outlet": "fas fa-utensils",
        "menu.Category": "fas fa-layer-group",
        "menu.MenuItem": "fas fa-pizza-slice",
        "tables.Table": "fas fa-chair",
        "orders.Order": "fas fa-receipt",
        "orders.OrderItem": "fas fa-hamburger",
        "reservations.TableReservation": "fas fa-calendar-check",
        "reservations.PartyBooking": "fas fa-glass-cheers",
        "customers.Customer": "fas fa-users",
        "promotions.Offer": "fas fa-percent",
    },
    # Default icon for parent apps
    "default_icon_parents": "fas fa-chevron-circle-right",
    # Default icon for child models
    "default_icon_children": "fas fa-circle",
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-warning",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

