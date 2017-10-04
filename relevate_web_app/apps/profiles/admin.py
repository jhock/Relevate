from django.contrib import admin
from .models.user_models import UserProfile
from .models.contributor_model import ContributorProfile, Degree, PendingContributors, DeniedContributors, \
	AcademicProfile, ContributorCertification
from .models.adviser_model import Adviser, DeniedAdvisers, PendingAdvisers

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ContributorProfile)
admin.site.register(Adviser)
admin.site.register(DeniedAdvisers)
admin.site.register(PendingAdvisers)
admin.site.register(Degree)
admin.site.register(PendingContributors)
admin.site.register(DeniedContributors)
admin.site.register(AcademicProfile)
admin.site.register(ContributorCertification)
