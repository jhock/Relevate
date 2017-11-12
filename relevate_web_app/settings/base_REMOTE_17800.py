"""
Django settings for relevate_web_app project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from .access_keys import secret_key, sendgrid_key, sendgrid_user

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key
SENDGRID_KEY = sendgrid_key
SENDGRID_USER = sendgrid_user
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []
LOGIN_REDIRECT_URL = 'contribution:home'

# Application definition

INSTALLED_APPS = [
	'apps.profiles',
	'apps.contribution',
	'apps.api',
	'compressor',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'storages',
	'rest_framework'
	#formset-dependencies
]

REST_FRAMEWORK = {
	'PAGE_SIZE': 10
}



MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'apps.contribution.middleware.mobile_redirect_middleware.DetectMobileBrowser'
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'context_processors.reset_url',
				'context_processors.confirm_url',
				'context_processors.done_url',
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.core.context_processors.request',
# )


EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = SENDGRID_USER
EMAIL_HOST_PASSWORD = SENDGRID_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
STATIC_DIRS = (os.path.join(BASE_DIR, 'static'))
COMPRESS_ROOT = (os.path.join(BASE_DIR, 'static/__cache__'))

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
	'/var/www/static/',
]

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
	('text/x-scss', 'django_libsass.SassCompiler'),
)

LOGIN_URL = "profile:login"
LOGGED_OUT_URL = "profile:logged_out"
