from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify


class Post(models.Model):

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
	A Post that is the main content for the site. It links to three different types of Posts: Articles, Links, and
	Infographics. The reason we used this format of a Post connected to an Article, Link, or Infographic is because
	this makes it much easier to manage and display content.
	"""

	class Meta:
		db_table = 'posts'

	contributor = models.ForeignKey('profiles.ContributorProfile', on_delete=models.CASCADE, blank=True, null=True)

	article = models.ForeignKey('contribution.Article', null=True)
	is_article = models.BooleanField(default=False)
	link = models.ForeignKey('contribution.Link', null=True)
	is_link = models.BooleanField(default=False)
	infographic = models.ForeignKey('contribution.Infographic', null=True)
	is_infographic = models.BooleanField(default=False)

	isPublished = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)
	is_pending_adviser = models.BooleanField(default=False)

	slug = models.SlugField(default=None, max_length=100)

	likes = models.IntegerField(default=0, verbose_name="post likes")
	views = models.IntegerField(default=0, verbose_name="post views")

	createdDate = models.DateTimeField(default=datetime.utcnow)
	publishedDate = models.DateTimeField(null=True, blank=True)
	updatedDate = models.DateTimeField(default=datetime.utcnow)

	def save(self, *args, **kwargs):
		'''
		custom save that creates a unique slug based on the date created.
		:param args:
		:param kwargs:
		:return:
		'''
		if not self.slug:
			title = self.getTitle()
			slug_val = title + str(self.createdDate)
			self.slug = slugify(slug_val)
		super(Post, self).save(*args, **kwargs)

	def getTitle(self):
		'''
		:return: The title of the article, link, or infographic.
		'''
		if (self.is_article):
			return self.article.title
		elif (self.is_link):
			return self.link.title
		elif (self.is_infographic):
			return self.infographic.title
		else:
			raise ValueError("Post isn't of type {Article, Link, Infographic}")

	def __str__(self):
		return self.getTitle()


class PendingPost(models.Model):
	'''
	A temporary, linking model for posts that are waiting to be approved by an adviser.
	'''
	class Meta:
		db_table = 'pendingpost'

	post = models.ForeignKey('Post', null=True)
	adviser = models.ForeignKey('profiles.Adviser', null=True)


