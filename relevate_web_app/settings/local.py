from .base import *

DATABASES = {
	'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'relevate_dev_db',
			'USER': 'rel_user',
			'PASSWORD': 'relevate_dev_pass',
		}
}

MEDIA_URL = '/media/'
MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))