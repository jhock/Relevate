from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime

class AboutPerson(models.Model):

	"""
	+--------------------------+-------------------------------------------------------------------------+
	|      Property            |                                   Use                                   |
	+==========================+=========================================================================+
	| name				       | The name of the person                                                  |
	+--------------------------+-------------------------------------------------------------------------+
	| image                    | An image of the person                                                  |
	+--------------------------+-------------------------------------------------------------------------+
	| content                  | The content about who the person is, how they contribute to Relevate etc|
	+--------------------------+-------------------------------------------------------------------------+
	| slug                     | A unique slug for a person                                              |
	+--------------------------+-------------------------------------------------------------------------+
	| funder or adviser        | An identifier used to place the person is the right section             |
	+--------------------------+-------------------------------------------------------------------------+
	This model is used on the "about.html" page. It is used to create a profile for someone who is an Official Advisor
	or a Funder. It allows the Relevate team and staff to easily add, remove, and edit entries on the "about" section
	of the site, without having to manually edit the HTML every time a new person joins the team.
	"""

	class Meta:
		db_table = 'about_person'

	name = models.TextField(max_length=200)
	image = models.ImageField(upload_to='about_person/image', null=False, blank=False)
	content = models.TextField(max_length=3000)
	funder_or_adviser = models.TextField(max_length=30)
	slug = models.SlugField(default=None, max_length=100)
	createdDate = models.DateTimeField(default=datetime.utcnow)
	position = models.IntegerField()  # The position field

	def save(self, *args, **kwargs):
		model = self.__class__

		if self.position is None:
			# Append
			try:
				last = model.objects.order_by('-position')[0]
				self.position = last.position + 1
			except IndexError:
				# First row
				self.position = 0
		if not self.slug:
			slug_val = self.name + str(self.createdDate)
			self.slug = slugify(slug_val)

		return super(AboutPerson, self).save(*args, **kwargs)

	class Meta:
		ordering = ('position',)

	def __str__(self):
		return self.name

	# def save(self, *args, **kwargs):
	# 	'''
	# 	custom save that creates a unique slug based on the date created.
	# 	:param args:
	# 	:param kwargs:
	# 	:return:
	# 	'''
	# 	if not self.slug:
	# 		slug_val = self.name + str(self.createdDate)
	# 		self.slug = slugify(slug_val)
	# 	super(AboutPerson, self).save(*args, **kwargs)
