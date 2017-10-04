from .profiles.models.adviser_model import Adviser
from .profiles.models.contributor_model import ContributorProfile, Address, Degree
from .profiles.models.user_models import UserProfile
from django.contrib.auth.models import User
from .contribution.models.topic_model import Topics
from .contribution.models.article_model import Article
from .contribution.models.post_model import Post
from datetime import datetime as dt
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ObjectDoesNotExist

class ProfileFactory(object):

	def __init__(self):
		pass

	# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	def create_user(self, email="test@email.com", password='password', first_name='Testy', 
			last_name='McTestFace', is_staff=False, tempname=None):
		if(tempname != None):
			first_name = tempname
			last_name = "Mc"+first_name+"Face"
		user = User.objects.create_user(email=email, username=email, password=password, 
			first_name=first_name, last_name=last_name, is_staff=is_staff)
		# user.save()
		return user

	# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	def create_user_profile(self, user=None, confirmed=True, is_adviser=False,
			is_contributor=False):
		if(user == None):
			user = self.create_user()
		user_prof = UserProfile.objects.create(user=user, confirmed=confirmed,
			is_adviser=is_adviser, is_contributor=is_contributor)
		# user_prof.save()

		return user_prof

	# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	def create_contributor_profile(self, user=None, user_profile=None, website_url=None, cv=None, 
			biography_text="No.", degree=None, institution="Kansas State University", 
			program="Computer Science", address=None, interests=None, avatar=None,
			accept_terms=True, expertise_topics=None, has_adviser=False, 
			adviser_profile=None, is_approved=True, date_joined=None, 
			is_adviser_passthrough=False):
		
		if(user_profile == None):
			user_profile = self.create_user_profile(user=user, 
				is_contributor=True, is_adviser=is_adviser_passthrough)
		if (degree == None):
			degree = Degree.objects.create(abbreviation="PhD", name='Doctor of Philosophy')
		if (address == None):
			address = Address.objects.create(street_address="123 Butts Dr.",
					city="Farts", state="North Carolina", zipcode="12345",
					country="USA")
		if (expertise_topics == None):
			expertise_topics = Topics.objects.create(name='Commitment',
				description="The role of commitment in romantic relationships and how to navigate it")
		if (date_joined == None):
			date_joined = dt.utcnow()

		contrib_prof = ContributorProfile.objects.create(user_profile=user_profile,
			website_url=website_url, cv=cv, biography_text=biography_text,
			degree=degree, institution=institution, address=address,
			interests=interests, avatar=avatar, accept_terms=accept_terms, 
			has_adviser=has_adviser,
			advisers_profile=adviser_profile, is_approved=is_approved, 
			date_joined=date_joined)
		# contrib_prof.save()
		contrib_prof.expertise_topics.add(expertise_topics)
		# contrib_prof.save()

		return contrib_prof

	# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	def create_adviser(self, user=None, contributor_profile=None, accept_terms=True, 
			max_num_advisees=5, is_active=True, is_available=True,
			description="No."):
		
		if (contributor_profile == None):
			contributor_profile = self.create_contributor_profile(user=user, is_adviser_passthrough=True)
		adviser_prof = Adviser.objects.create(contributor_profile=contributor_profile,
				accept_terms=accept_terms, max_num_advisees=max_num_advisees,
				is_active=is_active, is_available=is_available,
				description=description)
		# adviser_prof.save()

		return adviser_prof

	# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	'''
		Abbreviations for the following methods are shorthand for the following
		create_contributor_profile_needs_adviser_(True/False)_has_adviser_(True/False)
	'''

	def create_contributor_profile_NAT_HAT(self, adviser_user, student_user):
		degree = Degree.objects.create(abbreviation="SU", name="Student-Undergraduate")
		# degree.save()
		adviser = self.create_adviser(user=adviser_user)
		student = self.create_contributor_profile(user=student_user, degree=degree, 
				has_adviser=True, advisers_profile=adviser)

		# adviser.save()
		# student.save()

		return student

	# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	def create_contributor_profile_NAT_HAF(self, student_user):
		degree = Degree.objects.create(abbreviation="SU", name="Student-Undergraduate")
		# degree.save()
		student = self.create_contributor_profile(user=student_user, degree=degree)

		# student.save()
		return student

	# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	def create_contributor_profile_NAF_HAT(self, adviser_user, other_user):
		adviser = self.create_adviser(user=adviser_user)
		# adviser.save()
		other = self.create_contributor_profile(user=other_user, has_adviser=True, 
				advisers_profile=adviser)
		# other.save()
		return student

	# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

	def create_contributor_profile_NAF_HAF(self, other_user):
		other = self.create_contributor_profile(user=other_user)
		# other.save()

		return other

	# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


class ArticleFactory(object):

	def __init__(self):
		self.topics = Topics.objects.all()[0:2]

	def create_article(self, article_topics=None, image=None, title="testing fac title", content="fake content"):
		if article_topics is None:
			article_topics = self.topics
		image_file = SimpleUploadedFile(name=image, content=open(image, 'rb').read(),
												content_type='image/jpg')
		article = Article.objects.create(image=image_file, title=title, content=content)
		for item in article_topics:
			article.article_topics.add(item)
		return article

	def create_post(self, contributor_profile, article=None, image=None):
		if article is None:
			article = self.create_article(image=image)
		post = Post.objects.create(contributor=contributor_profile, is_article=True, article=article)
		return post

	def get_post_object(self, slug, article=None):
		if article:
			try:
				post = Post.objects.get(article=article)
			except ObjectDoesNotExist:
				post = None
		else:
			post = Post.objects.get(slug=slug)
		return post























