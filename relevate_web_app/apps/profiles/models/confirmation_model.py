from __future__ import unicode_literals
from django.db import models
from .user_models import UserProfile

class Confirmation(models.Model):

    class Meta:
        db_table = u'confirmation'

    user_profile = models.ForeignKey(UserProfile)
    confirmation_code = models.IntegerField(max_length=255, null=False, blank=False)