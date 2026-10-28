import os
from pathlib import Path
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# # 1. SECURITY CONFIGURATION (Fetched securely from .env)
# SECRET_KEY = config('SECRET_KEY')
#
# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# 1. SECURITY CONFIGURATION
SECRET_KEY = os.environ.get('SECRET_KEY', config('SECRET_KEY', default='local-dev-key'))
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# 2. CLOUDINARY CONFIGURATION
CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', config('CLOUDINARY_CLOUD_NAME', default=''))
API_KEY = os.environ.get('CLOUDINARY_API_KEY', config('CLOUDINARY_API_KEY', default=''))
API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', config('CLOUDINARY_API_SECRET', default=''))

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET,
    secure=True
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUD_NAME,
    'API_KEY': API_KEY,
    'API_SECRET': API_SECRET,
}



# 1. Keep localhost so your app still runs perfectly fine on your computer
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 2. Automatically detect and add your live Render URL when deployed
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)



#
# # 2. CLOUDINARY CONFIGURATION
# cloudinary.config(
#     cloud_name=config('CLOUDINARY_CLOUD_NAME'),
#     api_key=config('CLOUDINARY_API_KEY'),
#     api_secret=config('CLOUDINARY_API_SECRET'),
#     secure=True
# )
#
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
#     'API_KEY': config('CLOUDINARY_API_KEY'),
#     'API_SECRET': config('CLOUDINARY_API_SECRET'),
# }


# 3. APPLICATION DEFINITION
INSTALLED_APPS = [
    'cloudinary_storage',  # Must be placed before django.contrib.staticfiles
    'shop.apps.ShopConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this exact line
    # ... keep all your other middlewares exactly as they are
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'ourawsomecart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ourawsomecart.wsgi.application'



# 4. DATABASE
# 1. Default local database for your laptop
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 2. Automated switch to Render PostgreSQL when live
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )



# 5. PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# 6. INTERNATIONALIZATION & LOCALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True


# 7. STATIC & MEDIA FILES
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# 8. JAZZCASH PAYMENT GATEWAY (Secured via .env)
JAZZCASH_MERCHANT_ID = config('JAZZCASH_MERCHANT_ID', default='')
JAZZCASH_PASSWORD = config('JAZZCASH_PASSWORD', default='')
JAZZCASH_INTEGRITY_SALT = config('JAZZCASH_INTEGRITY_SALT', default='')

JAZZCASH_URL = "http://127.0.0.1:8000/shop/mock-jazzcash-gateway/"
JAZZCASH_RETURN_URL = "http://127.0.0.1:8000/shop/jazzcash-response/"


# 9. EASYPAISA SANDBOX CREDENTIALS (Secured via .env)
EASYPAISA_STORE_ID = config('EASYPAISA_STORE_ID', default='')
EASYPAISA_USERNAME = config('EASYPAISA_USERNAME', default='')
EASYPAISA_PASSWORD = config('EASYPAISA_PASSWORD', default='')
EASYPAISA_HASH_KEY = config('EASYPAISA_HASH_KEY', default='')

EASYPAISA_URL = "https://easypaystg.easypaisa.com.pk/easypay/Index.jsf"
EASYPAISA_RETURN_URL = "http://127.0.0.1:8000/shop/easypaisa-response/"

# 10. EMAIL CONFIGURATION (Console Backend for local testing)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'