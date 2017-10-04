from django.test import Client, TestCase
from ...utility_testing_methods import ProfileFactory
from ..models.adviser_model import DeniedAdvisers, PendingAdvisers, Adviser
from datetime import datetime as dt
from ...contribution.models.post_model import Post, PendingPost
from ...contribution.models.article_model import Article

pf = ProfileFactory()

class TestAdviserListView(TestCase):

	def setUp(self):
		adviser = pf.create_user(email='adviser@email.com', first_name='Adviser',
				last_name='McAdviserFace')
		self.adviser = pf.create_adviser(user=adviser)
		user = pf.create_user(email='user@email.com', first_name='User', 
				last_name='McUserFace')
		self.user = pf.create_user_profile(user=user)

	def test_adviser_list_user_logged_in(self):
		c = Client()
		logged_in = c.login(username=self.user.user.username, password='password')
		self.assertTrue(logged_in, "User could not be logged in")
		response = c.get('/profile/advisers/')
		
		self.assertEqual(response.status_code, 200, "Response didn't return a 200 status code")
		self.assertEqual(response.context['advisers'][0].__str__(), 'Adviser McAdviserFace', 
				"Adviser isn't passed to view correctly")

	def test_adviser_list_user_not_logged_in(self):
		c = Client()
		response = c.get('/profile/advisers/')
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['advisers'][0].__str__(), 'Adviser McAdviserFace', 
				"Adviser isn't passed to view correctly")

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


class TestDeniedAdviserListView(TestCase):

	allow_database_queries = True

	def setUp(self):
		adviser = pf.create_user(email='adviser@email.com', first_name='Adviser',
				last_name='McAdviserFace')
		self.adviser = pf.create_adviser(user=adviser)
		DeniedAdvisers.objects.create(adviser=self.adviser, date_denied=dt.utcnow(),
				reason='For testing purposes')
		staff_user = pf.create_user(email='staff@email.com', is_staff=True)
		non_staff = pf.create_user(email='non_staff@email.com', first_name='NonStaff',
				last_name='McNonStaffFace')
		self.staff_user = pf.create_user_profile(user=staff_user)
		self.non_staff_user = pf.create_user_profile(user = non_staff)

	def test_get_denied_advisers_not_staff(self):
		c = Client()
		logged_in = c.login(username = self.non_staff_user.user.username, password='password')

		self.assertTrue(logged_in, "Couldn't log in user")
		response = c.get('/profile/denied_advisers/')

		self.assertRedirects(response, "/")

	def test_get_denied_advisers_staff(self):
		c = Client()
		logged_in = c.login(username = self.staff_user.user.username, password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/denied_advisers/')

		self.assertEqual(response.status_code, 200, "Didn't return a 200 status code")
		self.assertEqual(response.context['advisers'][0].adviser.__str__(), "Adviser McAdviserFace",
				"The wrong adviser is being displayed")

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestAdiverApproveView(TestCase):

	def setUp(self):
		non_staff_user = pf.create_user(email='nonstaff@email.com', first_name='NonStaff',
				last_name='McNonStaffFace')
		non_staff = pf.create_user_profile(user=non_staff_user)
		adviser_user = pf.create_user(email='adviser@email.com', first_name='Adviser',
				last_name='McAdviserFace')
		adviser = pf.create_adviser(user=adviser_user, is_active=False)
		PendingAdvisers.objects.create(adviser=adviser)
		staff_user = pf.create_user(email='staff@email.com', first_name='Staff',
				last_name='McStaffFace', is_staff=True)
		staff = pf.create_user_profile(user=staff_user)

	def test_non_staff_access(self):
		c = Client()
		logged_in = c.login(username = "nonstaff@email.com", password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/advisers_approve/')

		self.assertRedirects(response, '/')

	def test_staff_access(self):
		c = Client()
		logged_in = c.login(username='staff@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/advisers_approve/')
		self.assertEqual(response.status_code, 200, "Didn't return a 200 status code")

		self.assertEqual(response.context['advisers'][0].__str__(), "Adviser McAdviserFace",
				"The wrong adviser is being displayed")

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestAdviserCreateGetView(TestCase):

	def setUp(self):
		contrib_user = pf.create_user(email='contrib@email.com')
		non_contrib_user = pf.create_user(email='noncontrib@email.com')
		contrib = pf.create_user_profile(user=contrib_user, is_contributor=True)
		non_contrib = pf.create_user_profile(user=non_contrib_user)

	def test_get_non_contrib(self):
		c = Client()
		logged_in = c.login(username='noncontrib@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/advisers_create/')
		self.assertRedirects(response, '/')

	def test_get_contrib(self):
		c = Client()
		logged_in = c.login(username='contrib@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/advisers_create/')

		self.assertEqual(response.status_code, 200, "Didn't return a 200 status code")

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestAdviserCreatePostView(TestCase):

	def setUp(self):
		self.contrib_user = pf.create_user(email='contrib@email.com')
		self.contrib = pf.create_contributor_profile(user=self.contrib_user)

	def test_valid_form(self):
		c = Client()
		logged_in = c.login(username='contrib@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.post('/profile/advisers_create/', {
				'accept_terms': True,
				'reason': 'Cause it sounds neat.',
				'number_of_advisees': 5
			})

		self.assertRedirects(response, '/')

		try:
			adviser_obj = Adviser.objects.get(contributor_profile=self.contrib)
		except Adviser.DoesNotExist:
			self.fail()

		try:
			PendingAdvisers.objects.get(adviser_id=adviser_obj.id)
		except PendingAdvisers.DoesNotExist:
			self.fail()

	def test_invalid_form(self):
		c = Client()
		logged_in = c.login(username='contrib@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.post('/profile/advisers_create/', {
				'accept_terms': True,
				'reason': 'Cause it sounds neat.'
			})
		
		# @US_TODO: Figure out how to make sure it still stays on adviser_create

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestAdviserUpdateGetView(TestCase):

	def setUp(self):
		non_adviser_user = pf.create_user(email='nonadviser@email.com')
		self.non_adviser = pf.create_user_profile(user=non_adviser_user)
		adviser_user = pf.create_user(email='adviser@email.com', first_name='Adviser',
				last_name='McAdviserFace')
		self.adviser = pf.create_adviser(user=adviser_user)

	def test_non_adviser_access(self):
		c = Client()
		logged_in = c.login(username='nonadviser@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/advisers_update/')

		self.assertRedirects(response, '/')

	def test_adviser_access(self):
		c = Client()
		logged_in = c.login(username='adviser@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/advisers_update/')

		form = response.context['form']
		
		self.assertEqual(form['number_of_advisees'].value(), 5)
		self.assertEqual(form['reason'].value(), "No.")

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestAdviserUpdatePostView(TestCase):

	def setUp(self):
		self.adviser = pf.create_adviser()

	def test_post_invalid(self):
		c = Client()
		logged_in = c.login(username='test@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.post('/profile/advisers_update', {
				'accept_terms': True,
				'number_of_advisees': 5
			})

		# @US_TODO: Figure out how to make sure it still stays on adviser_update
	
	def test_post_valid(self):
		c = Client()
		logged_in = c.login(username='test@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.post('/profile/advisers_update/', {
				'accept_terms': True,
				'number_of_advisees': 6,
				'reason': "No."
			})

		self.assertRedirects(response, '/profile/adviser_profile/')

		adviser = Adviser.objects.get(contributor_profile=self.adviser.contributor_profile)

		self.assertEqual(adviser.max_num_advisees, 6)

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestAdviserProfileView(TestCase):

	def setUp(self):
		self.adviser = pf.create_adviser()
		user = pf.create_user(email='nonadviser@email.com')
		self.user = pf.create_user_profile(user=user)

	def test_non_adviser_access(self):
		c = Client()
		logged_in = c.login(username='nonadviser@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/adviser_profile/')
		self.assertRedirects(response, '/')

	def test_adviser_access(self):
		c = Client()
		logged_in = c.login(username='test@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/adviser_profile/')

		adviser = response.context['adviser']
		self.assertEqual(str(adviser), "Testy McTestFace")
		self.assertEqual(adviser.max_num_advisees, 5)
		self.assertEqual(adviser.description, "No.")


# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestAdviserApprovePostView(TestCase):

	def setUp(self):
		self.adviser = pf.create_adviser()
		contrib_user = pf.create_user(email='contrib@email.com')
		self.contrib = pf.create_contributor_profile(user=contrib_user)
		article = Article.objects.create(
				title="My Article Title", 
				content="Don't tell me what to do",
				image = "test-img.png" # @US_TODO: Will mocking an image like this work?
			)
		post = Post.objects.create(
				contributor = self.contrib,
				is_article = True,
				article = article,
				is_pending_adviser = True
			)
		pending_post = PendingPost.objects.create(
				post = post,
				adviser = self.adviser
			)

	def test_adviser_access(self):
		c = Client()
		logged_in = c.login(username='test@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/approve-post/')

		post = response.context['posts'][0]
		
		self.assertEqual(post.article.title, "My Article Title")
		self.assertEqual(post.article.content, "Don't tell me what to do")
		self.assertEqual(post.contributor, self.contrib)

	def test_non_adviser_access(self):
		c = Client()
		logged_in = c.login(username='contrib@email.com', password='password')
		self.assertTrue(logged_in, "Couldn't log in user")

		response = c.get('/profile/approve-post/')

		self.assertRedirects(response, '/')

# @US_TODO: Ajax tests here
# http://ericholscher.com/blog/2009/apr/16/testing-ajax-views-django/
















