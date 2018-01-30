from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from ...contribution.models import Topics

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	confirmed = models.BooleanField(default=False)
	is_adviser = models.BooleanField(default=False)
	is_contributor = models.BooleanField(default=False)
	topics_preferences = models.ManyToManyField('contribution.Topics', blank=True)
	#user_avatar = models.ImageField(upload_to='user_profiles/user_avatar', null=True, blank=True)



	def __unicode__(self):
		return self.user.username

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name

	class Meta:
		db_table = "myrelevate_userprofile"
