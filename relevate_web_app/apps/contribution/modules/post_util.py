from ..models.topic_model import Topics
from ..models.post_model import PendingPost
from ...profiles.models.adviser_model import Adviser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from bs4 import BeautifulSoup
import imghdr
import os
from django.core.exceptions import ValidationError


def is_image_file(file_name):
	"""
	Returns file extenstion type. Were it sees if file extension is an images
	Note: only call this function after form is valid is called on the form.

	:param file_name:

	:return: True if image, returns false if pdf
	"""
	if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
		return True
	else:
		return False


def validate_file(value):
	"""
	Validate file type. Makes sure that it is an image file by checking it's extension
	This is used by django's form for validation. It will eventually include other types of
	valid files we accept from user.

	:param value: the file content
	:return:
	"""
	try:
		ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
		valid_extensions = ['.jpg', '.png', '.jpeg']
		if not ext.lower() in valid_extensions:
			raise ValidationError(u'Unsupported file extension.')
	except AttributeError:
		raise ValidationError(u'Unsupported file extension.')

def validate_content_creation_file(value):
	"""
	Validate file type. Makes sure that it is an image file by checking it's extension
	This is used by django's form for validation. It will eventually include other types of
	valid files we accept from user.

	:param value: the file content
	:return:
	"""
	try:
		ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
		valid_extensions = ['.doc', '.docx', '.pdf', '.mp4', '.webm']
		if not ext.lower() in valid_extensions:
			raise ValidationError(u'Unsupported file extension.')
	except AttributeError:
		raise ValidationError(u'Unsupported file extension.')




def add_to_pending_post(new_post, adviser):
	"""
	Add new Post Item to pending post

	:param new_post: New post object
	:param adviser: The adviser that would eventually approve the post
	:return: This is True is successfully added to advisor's post to aprove, return false is post needs no advisor
	"""
	if ( not new_post.contributor.has_adviser):
		return False

	try:
		# See if the adviser has a pending posts associted
		# with them
		pending_post = PendingPost.objects.get(adviser=adviser)
	except ObjectDoesNotExist:
		# if they don't, create one.
		pending_post = PendingPost(adviser=adviser)
		pending_post.save()
	# add the post to that pending post
	print(pending_post.adviser)
	pending_post.pending_posts.add(new_post)
	return True


def remove_from_pending_post(confirmed_post, is_pending):
	"""
	Remove Post from pending post table

	:param confirmed_post: THe post that is elegible to be viewed by the public
	:param is_pending: A boolean that checks if post has already been removed
	:return: False if already removed from list. True if otherwise
	"""
	adviser = confirmed_post.contributor.adviser_profile
	if (adviser):
		try:
			pending_post = PendingPost.objects.get(adviser=adviser)
			pending_post.pending_post.remove(confirmed_post)
			pending_post.save()
			confirmed_post.is_pending_adviser = is_pending
			confirmed_post.save()
			return True
		except ObjectDoesNotExist:
			# send an email to us that something went wrong,
			pass
	return False


def approve_post(post):
	"""
	Adviser approves user post

	:param post: Post object
	:return: void
	"""
	# send email or something
	if (remove_from_pending_post(post, False)):
		post.isPublished = True
	else:
		# @US_TODO: ERROR, need to do something here
		pass

def deny_post(post):
	"""
	Deny User from making post public
	:param post:
	:return:
	"""
	# send email hurr
	return remove_from_pending_post(post, True)


def display_error(form, request):
	"""
	Desplay form error to the user
	:param form: The form
	:param request: The session request
	:return: void
	"""
	for field, mes in form.errors.items():
		str_item = BeautifulSoup(mes[0], 'html.parser')
		#print (str_item.get_text())
		messages.warning(request, "For this field: %s. %s" % (field, mes[0]))

