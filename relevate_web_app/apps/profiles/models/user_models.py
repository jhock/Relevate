from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from .contributor_model import ContributorProfile
from ...contribution.models import Topics

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	confirmed = models.BooleanField(default=False)
	is_adviser = models.BooleanField(default=False)
	is_contributor = models.BooleanField(default=False)
	is_pending_contributor = models.BooleanField(default=False)
	topics_preferences = models.ManyToManyField('contribution.Topics', blank=True)
	#user_avatar = models.ImageField(upload_to='user_profiles/user_avatar', null=True, blank=True)


	def get_associated_contributor(self):
		#returns the contributor profile associated with the user. Mainly used for getting the avatar without having to pass
		#the user's contributor profile to every single page. May be removed and replaced with setting the user_avatar
		#to the contributor.avatar. I'll have to run through the code and see if other information besides the contributor's
		#avatar is needed.
		return ContributorProfile.objects.get(user_profile=self)

	def __unicode__(self):
		#returns the username of the user
		return self.user.username

	def full_name(self):
		#returns the full name of the user
		return self.user.first_name + " " + self.user.last_name

	def __str__(self):
		#returns the full name of the user
		#will remove this soon as it has been replaced by full_name, need to sure it is not needed anywhere before removal
		return self.user.first_name + " " + self.user.last_name

	class Meta:
		db_table = "myrelevate_userprofile"
