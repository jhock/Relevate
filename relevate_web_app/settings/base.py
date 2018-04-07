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


ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.relevate.com']
LOGIN_REDIRECT_URL = 'contribution:home'

# Application definition

INSTALLED_APPS = [
	'apps.profiles',
	'apps.contribution',
	'apps.components',
	'apps.styleguide',
	'apps.api',
	'compressor',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'templatetag_handlebars',
	'storages',
	'rest_framework',
	'ckeditor',
	'ckeditor_uploader'

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
			'libraries':{
				'button_tags': 'apps.components.templatetags.button_tags',
				'checkbox_tags': 'apps.components.templatetags.checkbox_tags',
				'file_input_tags': 'apps.components.templatetags.file_input_tags',
        'dropdown_menu_tags': 'apps.components.templatetags.dropdown_menu_tags',
       	'icon_tags': 'apps.components.templatetags.icon_tags',
       	'progress_tags': 'apps.components.templatetags.progress_tags',
        'select_tags': 'apps.components.templatetags.select_tags',
        'text_area_tags': 'apps.components.templatetags.text_area_tags',
        'text_input_tags': 'apps.components.templatetags.text_input_tags',
        'component_assets': 'apps.components.templatetags.component_assets',
        'example_tags': 'apps.styleguide.templatetags.example_tags'
			}
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
STATIC_ROOT = (os.path.join(BASE_DIR,'static_assets'))
COMPRESS_ROOT = (os.path.join(BASE_DIR, 'static/__cache__'))

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
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

# The following lines are settings for django-ckeditor. See their documentation page for more info.
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

# Configuration for django-ckeditor. Here is where you control everything for django-ckeditor, including the toolbar,
# style, size, options, file upload url, and extra plugins. Plugins must be added to /static/ckeditor/plugins, and to
# 'extraPlugins' to appear on the editor.
CKEDITOR_CONFIGS = {
	#To change the default toolbar, go to /static/js/ckeditor_basic_config.js. Yes, it only works that way.
	#Toolbars set here can only be used for ckeditor form fields, default django form fields must be replaced in the
	#template or assocated js file.
    'default': {
        'toolbar': 'Basic',
    },
	#The advanced toolbar, mainly used for content with image upload
	'advanced_toolbar': {
		'skin': 'moono',
		# 'skin': 'office2013',
		'toolbar': 'Custom',
		'toolbar_Custom': [
			{'name': 'clipboard', 'items': ['Undo', 'Redo', 'PasteFromWord']},
			{'name': 'styles', 'items': ['Styles', 'Format']},
			{'name': 'basicstyles',
			 'items': ['Bold', 'Italic', 'Underline', 'RemoveFormat']},
			{'name': 'paragraph',
			 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
					   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'Blockquote']},
			{'name': 'document', 'items': ['Preview', '-', 'Templates']},
			{'name': 'links', 'items': ['Link', 'Unlink']},
			{'name': 'insert',
			 'items': ['Image']},
			{'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
			{'name': 'about', 'items': ['About']},
			{'name': 'editing', 'items': ['Scayt']},
		],
		# 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
		# 'height': 291,
		# 'width': '100%',
		# 'filebrowserWindowHeight': 725,
		# 'filebrowserWindowWidth': 940,
		# 'toolbarCanCollapse': True,
		'tabSpaces': 4,
		'extraPlugins': ','.join([
			'uploadimage',  # the upload image feature,
			'uploadwidget',
			'image2',
 'about', 'clipboard',  'colordialog',  'dialog', 'div',
 'filetools', 'find', 'flash', 'format', 'forms', 'iframe', 'image', 'justify', 'language',
'lineutils', 'link', 'magicline', 'menubutton', 'notification', 'notificationaggregator',
'pagebreak', 'pastefromword', 'preview', 'scayt', 'showblocks', 'smiley',
 'specialchar', 'stylescombo', 'table', 'templates', 'undo',
 'widget', 'maximize', 'removeformat', 'blockquote'
		]),
		"removePlugins": "stylesheetparser",
		'imageUploadUrl' : '/ckeditor/',
		'filebrowserUploadUrl' : '/ckeditor/upload/',
	}
}

# I wasn't sure where to put this, so I'm open/hopeful we can move it to a 
# location that makes more sense

# this allows Django template tags to span multiple lines.
import re
from django.template import base
base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)

