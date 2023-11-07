from pathlib import Path
import datetime
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))
APPS_DIR = BASE_DIR / "app"

DEBUG = env.bool("DJANGO_DEBUG", True)

SECRET_KEY = 'django-freddiers-secret-key-dnasjkdn%^313()dsadsa//$$%$#'

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
AUTH_GROUP_MODEL = None
AUTH_PERMISSION_MODEL = None
AUTH_USER_MODEL = 'authentication.User'

# Application definition

DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    ]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_yasg',
]

LOCAL_APPS = [
    'app.authentication',
    'app.core',
    'app.loans',
    'app.accounting',
]
    
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
APPEND_SLASH = True

db_name = env.str('DB_NAME', 'drums')
db_user = env.str('DB_USER', 'cifu')
db_password = env.str('DB_PASSWORD', 'febreroDe13')
db_host = env.str('DB_HOST', 'general-testing-ldin.caio4cdm27ia.us-east-1.rds.amazonaws.com')
db_port = env.str('DB_PORT', '5432')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': db_port,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'
#DEFAULT_FILE_STORAGE set to local

try:
    DEFAULT_FILE_STORAGE=env("DEFAULT_FILE_STORAGE")
except:
    pass

AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", "123")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", "123")
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME", "123")
AWS_REGION_NAME = env.str("AWS_REGION_NAME", "123")
AWS_QUERYSTRING_AUTH = False

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
SIMPLE_JWT = {
    'SIGNING_KEY': 'django-freddiers-secret-key-dnasjkdn%^313()dsadsa//$$%$#',
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(hours=24),
    "AUDIENCE": "https://freddierbusiness.com",
    "ISSUER": "https://freddierbusiness.com",
    "SUBJECT": "web/app user auth",
}
BLACKLIST_APP = {
    'ROTATE_REFRESH_TOKENS': True,
    'CHECK_BLACKLIST': True,
    'ALWAYS_BLACKLIST': True,
}
SILENCED_SYSTEM_CHECKS = ['models.W042', 'urls.W002']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'