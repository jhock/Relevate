
from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage as storage
from io import BytesIO
import boto
from base64 import b64decode
import os



def get_infographic_crop(content, thumb_name):
	"""
	Crop infographic, upload to S3 or local, and return the name
	of the cropped image file.
	
	:param content: Image to open
	:param thumb_name: The slugified name to be used for the thumbnail
	
	:return: The possibly modified thumbnail name
	"""
	img = Image.open(content)
	width, height = img.size
	if (height > 300):
		img = img.crop((0, 0, width, 300))
		# if (len(thumb_name) >= 168):
		# 	thumb_name = thumb_name[:167]
	memFile = BytesIO()
	ext = content.content_type.upper().split("/")[1]
	img.save(memFile, format=ext)

	if not (os.environ['DJANGO_SETTINGS_MODULE'] == 'settings.local'):
		conn  = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
		bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME, validate=False)
		k = bucket.new_key('media/article_infographic/thumbnails/' + thumb_name)
		k.set_contents_from_string(memFile.getvalue())
		k.set_acl("public-read")
		memFile.close()
	else:
		img.save(settings.MEDIA_ROOT + "/article_infographic/thumbnails/"  + thumb_name)
	return thumb_name