from __future__ import unicode_literals
from django.db import models


class Universities(models.Model):
	name_of_university = models.CharField(max_length=250, null=False, blank=False)

