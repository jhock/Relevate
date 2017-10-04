from datetime import datetime

from django.db import models

class Link(models.Model):
	'''
	+-------------+--------------------------------------+
	| Property    | Use                                  |
	+=============+======================================+
	| topics      | The topics associated with this link |
	+-------------+--------------------------------------+
	| title       | The title of the link                |
	+-------------+--------------------------------------+
	| url         | The url to the link                  |
	+-------------+--------------------------------------+
	| description | The description of the link          |
	+-------------+--------------------------------------+
	| image       | The image associated with the link   |
	+-------------+--------------------------------------+
	A type of post that is used to link to existing content on another site. It is useful because a lot of contributors
	already have work on a personal site or other site that they have created.
	'''
	class Meta:
		db_table = 'links'

	topics = models.ManyToManyField('Topics')
	title = models.CharField(max_length=100)
	url = models.URLField()
	description = models.TextField(max_length=400)
	image = models.ImageField(upload_to='links/images', max_length=150)

	def __str__(self):
		return self.title