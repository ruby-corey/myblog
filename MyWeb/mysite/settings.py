
import os
from pathlib import Path
import environ


env = environ.Env()


BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR/ ".env"
if env_path.exists():
    env.read_env(env_path)
else :
    print("错误未找到env文件")



SECRET_KEY = env("DJANGO_SECRET_KEY")


DEBUG = env.bool("DJANGO_DEBUG")
SHOW_GRID = DEBUG

ALLOWED_HOSTS = env.list('PRIVATE_HOST', default=['localhost', '127.0.0.1',])
CSRF_TRUSTED_ORIGINS = ['']


INSTALLED_APPS = [
    
    "MyBlog.apps.MyblogConfig",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "markdownx",
]

MIDDLEWARE = [
    

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'MyBlog.middleware.VisitTrackingMiddleware', #....
    
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "MyBlog.context_processors.sidebar_data",    
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"




DATABASES = {
     "default": env.db(),
}




AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "Zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = False

USE_TZ = True



STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    
    "127.0.0.1",

]

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
