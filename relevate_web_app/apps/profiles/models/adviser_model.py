from __future__ import unicode_literals
from django.db import models


class Adviser(models.Model):
	"""
	+--------------------------+-------------------------------------------------------------------------+
	|      Property            |                                   Use                                   |
	+==========================+=========================================================================+
	| contributor_profile      | The ``ContributorProfile`` instance that corresponds to this adviser    |
	+--------------------------+-------------------------------------------------------------------------+
	| accept_terms             | Whether the adviser has check the "Accept Terms" box in the application |
	+--------------------------+-------------------------------------------------------------------------+
	| max_num_advisees         | The maximum number of people the adviser is willing to take on          |
	+--------------------------+-------------------------------------------------------------------------+
	| is_active                | Whether the adviser has been approved by the staff                      |
	+--------------------------+-------------------------------------------------------------------------+
	| is_available             | Whether the adviser is currently able to take on more advisees          |
	+--------------------------+-------------------------------------------------------------------------+
	| description              | The self written description of why they want to be an adviser.         |
	+--------------------------+-------------------------------------------------------------------------+
	"""

	class Meta:
		db_table = 'advisers'

	contributor_profile = models.ForeignKey('ContributorProfile')
	accept_terms = models.BooleanField(default=False)
	max_num_advisees = models.IntegerField(default=False, null=True)
	is_active = models.BooleanField(default=False)
	is_available = models.BooleanField(default=False, verbose_name="Checks if adviser can take on more students")
	description = models.TextField(null=False, blank=False)

	def __str__(self):
		"""
		Returns the first and last name of the user profile associated with this adviser
		"""
		return (self.contributor_profile.user_profile.user.first_name + " " + 
			self.contributor_profile.user_profile.user.last_name)


class PendingAdvisers(models.Model):
	"""
	+----------+--------------------------------------------------+
	| Property |                       Use                        |
	+==========+==================================================+
	| adviser  | The ``Adviser`` instance that is pending review. |
	+----------+--------------------------------------------------+

	"""
	class Meta:
		db_table = 'pending_advisers'
	adviser = models.ForeignKey('Adviser')


class DeniedAdvisers(models.Model):
	"""
	+-------------+--------------------------------------------------+
	|  Property   |                       Use                        |
	+-------------+--------------------------------------------------+
	| adviser     | The ``Adviser`` instance that is pending review. |
	+-------------+--------------------------------------------------+
	| reason      | The reason the adviser was denied                |
	+-------------+--------------------------------------------------+
	| date_denied | The date which a staff member denied them        |
	+-------------+--------------------------------------------------+
	"""
	class Meta:
		db_table = 'denied_advisers'

	adviser = models.ForeignKey('Adviser')
	reason = models.TextField(null=False, blank=False)
	date_denied = models.DateTimeField(null=True, blank=False)

	def __str__(self):
		"""
		Returns the first and last name of the user profile associated with this adviser
		"""
		return (self.adviser.contributor_profile.user_profile.user.first_name + " " + 
			self.adviser.contributor_profile.user_profile.user.last_name)

