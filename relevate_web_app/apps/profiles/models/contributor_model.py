from django.db import models
from datetime import datetime
from .adviser_model import Adviser
from ...contribution.models.topic_model import Topics
from .user_models import UserProfile


class Degree(models.Model):
	class Meta:
		db_table = 'degree'
	abbreviation = models.CharField(max_length=10, null=False, blank=False)
	name = models.CharField(max_length=50, null=False, blank=False)

	def __str__(self):
		return self.name


class Address(models.Model):

	class Meta:
		db_table = 'address'

	street_address = models.CharField(max_length=255, null=False, blank=True)
	city = models.CharField(max_length=255, null=False, blank=False)
	state = models.CharField(max_length=255, null=False, blank=False)
	zipcode = models.CharField(max_length=5, null=False, blank=False)
	country = models.CharField(max_length=255, null=False, blank=False)


class ContributorProfile(models.Model):

	class Meta:
		db_table = 'contributorprofile'

	user_profile = models.ForeignKey('UserProfile')
	website_url = models.URLField(null=True, blank=True)
	cv = models.FileField(upload_to='user_profiles/cv', null=True, blank=True)
	biography_text = models.TextField(max_length=3000, null=True, blank=True)
	address = models.ForeignKey('Address', null=False, blank=False)
	interests = models.TextField(null=True, blank=True)
	avatar = models.ImageField(upload_to='user_profiles/avatar', null=True, blank=True)
	accept_terms = models.BooleanField(default=False)
	expertise_topics = models.ManyToManyField('contribution.Topics')
	has_adviser = models.BooleanField(default=False)
	advisers_profile = models.ForeignKey('Adviser', null=True, blank=True)
	is_approved = models.BooleanField(default=False)
	date_joined = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.user_profile.user.first_name + " " + self.user_profile.user.last_name


class DeniedContributors(models.Model):
	class Meta:
		db_table = 'denied_contributors'
	contributor = models.ForeignKey(ContributorProfile, null=True, blank=True)
	reason = models.TextField(null=False, blank=False)
	date_denied = models.DateTimeField(null=False, blank=False)


class PendingContributors(models.Model):
	class Meta:
		db_table = 'pending_contributors'
	contributor = models.ForeignKey(ContributorProfile, null=True, blank=True)


class AcademicProfile(models.Model):

	class Meta:
		db_table = 'academicprofile'

	degree = models.ForeignKey('Degree', null=False, blank=False)
	program = models.CharField(max_length=255, null=False, blank=False, verbose_name="i.e department name")
	institution = models.CharField(max_length=255, null=False, blank=False)
	contributor_profile = models.ForeignKey('ContributorProfile', null=False, blank=False)

	def __str__(self):
		return self.contributor_profile.user_profile.user.first_name + \
			   " " + self.contributor_profile.user_profile.user.last_name


class ContributorCertification(models.Model):
	class Meta:
		db_table = 'certificationprofile'

	name_of_certification =  models.TextField(null=True, blank=True)
	contributor_profile = models.ForeignKey('ContributorProfile', null=False, blank=False)

	def __str__(self):
			return self.contributor_profile.user_profile.user.first_name + \
				   " " + self.contributor_profile.user_profile.user.last_name

class OrganizationalAffiliation(models.Model):
	class Meta:
		db_table = 'organizational_affiliation'

	name_of_affiliation = models.TextField(null=True, blank=True)
	contributor_profile = models.ForeignKey('ContributorProfile', null=False, blank=False)

	def __str__(self):
			return self.contributor_profile.user_profile.user.first_name + \
				   " " + self.contributor_profile.user_profile.user.last_name







