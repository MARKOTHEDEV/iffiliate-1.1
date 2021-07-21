"""
Django settings for iffilate project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$!cckhd%+9+(^vxxksodhq!^pq4&kjcn=e*w0hipcpn(phe@ip'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['689c17057ed5.ngrok.io','localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',


    # local files
    'iffliateLanding_page.apps.IffliatelandingPageConfig',
    'users.apps.UsersConfig',
    'raffleDraw.apps.RaffledrawConfig',



    # third party api
    'rest_framework',
   

    #defualt apps for django all auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',    

    # providers i will need e.g facebook
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iffilate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'template')],
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

WSGI_APPLICATION = 'iffilate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Etc/GMT-8'

USE_I18N = True

USE_L10N = True

USE_TZ = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

"this line of code tell django that hey! when the browser is close tell the user to login again!!"
SESSION_EXPIRE_AT_BROWSER_CLOSE=True

STATIC_URL = '/static/'


MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')


# STATICFILES_DIRS = [
#     BASE_DIR / "static",
#     # Path(BASE_DIR,'iffliateLanding_page','static')
#     os.path.join(BASE_DIR,'iffliateLanding_page','static')
    
# ]

STATIC_ROOT = Path(BASE_DIR,'static')

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

AUTH_USER_MODEL = 'users.User'





PAYSTACK_SECRET_KEY   =  'sk_test_38a62cfc2939b3665f400a7c57bd61b7ab19f3fa'
PAYSTACK_PUBLIC_KEY  = 'pk_test_17925fc67c5b6da3dbef32feab9afccb0d175729'




# this area is django all auth specfic settings
SITE_ID = 1
# google settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            # 'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        }
    }
}

"the line below tells django that ="
" 'Hey any social auth u use use the email to authenticate'"
ACCOUNT_AUTHENTICATION_METHOD = 'email'
"Hey if u using a social auth the data we need the most is an email"
ACCOUNT_EMAIL_REQUIRED = True
"hey am not going to accept duplicate email Let that stick in your head "
ACCOUNT_UNIQUE_EMAIL = True
"NOMARLY django uses username but i wrote a custom user model to use email ass authentication"
# so i set it to none just to override the defualt behaviour
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
"Since my custom model dont need a Username is authenticate so we dont need the username.."
ACCOUNT_USERNAME_REQUIRED = False



"The code below has to do with enabling django to send email to USers"

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['website_email']
EMAIL_HOST_PASSWORD = os.environ['website_email_password']
EMAIL_USE_TLS = True



"ALL MY CALLBACK URL VARIBLES .. THIS ARE THE URL THAT GET CALLED AFTER A PERSON PAYS"
"mainly paystack payment"
RAFFLE_DRAW_PAYMENT_CALLBACK_URL = 'http://localhost:8000/raffle/raffleDraw-callback/'
PAYMENT_FOR_MEMBERSHIP_CALLBACK = 'http://localhost:8000/membership_payment_callback/'




django_heroku.settings(locals())