from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# secrets.json
secret_file = os.path.join(BASE_DIR, 'secrets.json') 

with open(secret_file) as f:
    secrets = json.loads(f.read())

# def get_secret(setting):
#     try:
#         return secrets[setting]
#     except KeyError:
#         error_msg = "Set the {} environment variable".format(setting)
#         raise ImproperlyConfigured(error_msg)

def get_env_variable(var_name):
  try:
    return secrets[var_name]
  except KeyError:
    error_msg = 'Set the {} environment variable'.format(var_name)
    raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_variable("SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'corsheaders',
    
    # my app
    'bookieum',
    'kakao',
    'google',
    'naver',
    'logout',
    'main',
    'mypage',
    'survey',
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", 
    "http://bookieum-bucket.s3-website.ap-northeast-2.amazonaws.com"
]
CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'bookieum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'bookieum.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable("MYSQL_NAME"),
        'USER': get_env_variable("MYSQL_USER"),
        'PASSWORD': get_env_variable("MYSQL_PASSWORD"),
        'HOST': get_env_variable("MYSQL_HOST"),
        'PORT': get_env_variable("MYSQL_PORT"),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'statics')
STATIC_URL = '/assets/'
STATICFILES_DIRS =(os.path.join(BASE_DIR, 'static'),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 세션 설정
# SESSION_COOKIE_AGE = 3600
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_COOKIE_SAMESITE = 'Lax' 