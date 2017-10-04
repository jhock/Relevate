from django.db import models


class Infographic(models.Model):
	'''
	+-----------+--------------------------------------------------------------------+
	| Property  | Use                                                                |
	+===========+====================================================================+
	| title     | The title of the infographic                                       |
	+-----------+--------------------------------------------------------------------+
	| image     | The actual infographic image                                       |
	+-----------+--------------------------------------------------------------------+
	| topics    | The topics associated with the infographic                         |
	+-----------+--------------------------------------------------------------------+
	| is_image  | **Depricated**                                                     |
	+-----------+--------------------------------------------------------------------+
	| thumbnail | The cropped portion of the infographic used to display in the feed |
	+-----------+--------------------------------------------------------------------+
	| blurb     | The description of the infographic                                 |
	+-----------+--------------------------------------------------------------------+
	A type of Post that contains an infographic and no text besides the descriptive blurb.
	'''
	class Meta:
		db_table = 'infographics'

	title = models.TextField(max_length=1000)
	image = models.FileField(upload_to='article_infographic/', null=True, blank=True)
	topics = models.ManyToManyField('Topics')
	is_image = models.BooleanField(default=True)
	thumbnail = models.ImageField(upload_to='article_infographic/thumbnails/', max_length=250, default=None, null=True)
	blurb = models.CharField(max_length=150, null=False, blank=False, default=None)

	def __str__(self):
		return self.title

