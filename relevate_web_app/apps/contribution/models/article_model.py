from django.db import models


class Article(models.Model):
	"""
	+--------------------------+-------------------------------------------------------------------------+
	|      Property            |                                   Use                                   |
	+==========================+=========================================================================+
	| article_topics           | The topic of the article                                                |
	+--------------------------+-------------------------------------------------------------------------+
	| image                    | A url pointer to the location of the article image                      |
	+--------------------------+-------------------------------------------------------------------------+
	| title                    | Title of the article                                                    |
	+--------------------------+-------------------------------------------------------------------------+
	| content                  | The article content                                                     |
	+--------------------------+-------------------------------------------------------------------------+
	| blurb                    | A short excerpt of the article content                                  |
	+--------------------------+-------------------------------------------------------------------------+
	| references               | A place to list any references used in the article                      |
	+--------------------------+-------------------------------------------------------------------------+
	A type of Post whos main content is text.
	"""
	class Meta:
		db_table = 'article'

	article_topics = models.ManyToManyField('Topics')
	image = models.ImageField(upload_to='articles/images', null=False, blank=False)
	title = models.TextField(max_length=1000)
	content = models.TextField(max_length=5000)
	blurb = models.CharField(max_length=250, default="")
	references = models.TextField(max_length=3000, null=True, blank=True)

	def __str__(self):
		return self.title

