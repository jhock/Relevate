from ..models.adviser_model import Adviser
from ..models.contributor_model import ContributorProfile

def get_adviser_profile(user_prof):
	contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
	adviser = Adviser.objects.get(contributor_profile=contrib_prof)
	return adviser