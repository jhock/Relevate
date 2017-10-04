from django.db import models


class Topics(models.Model):
	class Meta:
		db_table = 'topics'
	name = models.CharField(max_length=100, null=False, blank=False)
	description = models.CharField(max_length=255, null=False, blank=False)

	def __str__(self):
		return self.name

