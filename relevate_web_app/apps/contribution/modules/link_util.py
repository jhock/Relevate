# from PIL import Image
# from selenium.webdriver.remote.remote_connection import LOGGER
# import os
# from django.conf import settings
# from django.core.files.storage import default_storage as storage
# from io import BytesIO
# import boto
# from base64 import b64decode

## def get_link_screenshot(link, name):
## 	"""
## 	**UNUSED**
#	
## 	Get the screen shot of the link
#	
## 	:param link: The link Url
## 	:param name: Name of the Caputure Url
## 	"""
## 	# logging.ERROR = 40
## 	LOGGER.setLevel(40)
## 	driver = webdriver.PhantomJS(service_args=["--webdriver-loglevel=NONE"])
## 	driver.set_window_size(1200, 760) # set the window size that you need 
## 	driver.get(link)

## 	# Get it as a bytes array so we don't have to save and load
## 	# the file, it just stays in memory only until it's put on
## 	# S3
## 	src_base64 = driver.get_screenshot_as_base64()
## 	src_png = b64decode(src_base64)
## 	img = Image.open(BytesIO(src_png))
## 	img = img.crop((0, 0, 1200, 300))
## 	memFile = BytesIO()
## 	img.save(memFile, format="PNG")

## 	# Since the local settings file wont have AWS_ACCESSS_KEY stuff,
## 	# if you get an attribute error then you're probably on a local machine
## 	# so just save it like normal
## 	try:
## 		conn  = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
## 		bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME, validate=False)
## 		k = bucket.new_key('media/links/images/' + name)
## 		k.set_contents_from_string(memFile.getvalue())
## 		k.set_acl("public-read")
## 		memFile.close()
## 	except AttributeError:
## 		img.save(settings.MEDIA_ROOT + '/links/images/' + name)

