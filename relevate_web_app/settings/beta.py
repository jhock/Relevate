from .base import *
from .access_keys import (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
	database_password, database_user )

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'ebdb',
		'USER': database_user,
		'PASSWORD': database_password,
		'HOST': 'aabfsxdo8won4f.czggqranenuo.us-west-2.rds.amazonaws.com',
		'PORT': 3306
	}
}

AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
		'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
		'Cache-Control': 'max-age=94608000',
	}

AWS_STORAGE_BUCKET_NAME = 'relevate-media-bucket'


# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# MEDIAFILES_LOCATION = 'media'
# STATICFILES_LOCATION = 'static'

# STATICFILES_STORAGE = "custom_storages.StaticStorage"
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/" % (AWS_S3_CUSTOM_DOMAIN,)
DEFAULT_FILE_STORAGE = "custom_storages.MediaStorage"


