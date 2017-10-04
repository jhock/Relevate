from django.test import Client, TestCase
from ...utility_testing_methods import ProfileFactory
from ..models.contributor_model import DeniedContributors, PendingContributors
from datetime import datetime as dt

pf = ProfileFactory()

class TestContributorCreateView(TestCase):

	def setUp(self):
		pass

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestContributorUpdateView(TestCase):

	def setUp(self):
		pass

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestContributorProfileView(TestCase):

	def setUp(self):
		pass

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestPublicContributorProfileView(TestCase):

	def setUp(self):
		pass

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestContributorListView(TestCase):

	def setUp(self):
		first_user = pf.create_user(email='first@email.com', first_name='First',
				last_name='McFirstFace')
		second_user = pf.create_user(email='second@email.com', first_name='Second',
				last_name='McSecondFace')
		contrib_one = pf.create_contributor_profile(user=first_user)
		contrib_two = pf.create_contributor_profile(user=second_user)

	def test_contrib_list(self):
		c = Client()
		response = c.get('/profile/contributors/')
		
		self.assertEqual(response.status_code, 200)

		c1 = response.context['contributors'][0]
		c2 = response.context['contributors'][1]

		self.assertEqual(str(c1), "First McFirstFace")
		self.assertEqual(str(c2), "Second McSecondFace")

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestDeniedContributorListView(TestCase):

	def setUp(self):
		contrib_user = pf.create_user(email='contrib@email.com', first_name="Contrib",
				last_name='McContribFace')
		contrib = pf.create_contributor_profile(user=contrib_user)
		DeniedContributors.objects.create(contributor=contrib, 
				reason='Cause I said so.', date_denied=dt.utcnow())

		staff_user = pf.create_user(email='staff@email.com', tempname="Staff", is_staff=True)
		non_staff = pf.create_user(email='nonstaff@email.com', tempname="NonStaff")

		pf.create_user_profile(user=staff_user)
		pf.create_user_profile(user=non_staff)

	def test_non_staff_access(self):
		c = Client()

		logged_in = c.login(username='nonstaff@email.com', password='password')
		self.assertTrue(logged_in, "User could not be logged in")

		response = c.get('/profile/denied_contributors/')
		
		self.assertRedirects(response, "/")

	def test_staff_access(self):
		c = Client()

		logged_in = c.login(username='staff@email.com', password='password')
		self.assertTrue(logged_in, "User could not be logged in")

		response = c.get('/profile/denied_contributors/')
		
		c1 = response.context['contributors'][0].contributor

		self.assertEqual(str(c1), "Contrib McContribFace")


# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-

class TestContributorApproveView(TestCase):

	def setUp(self):
		staff = pf.create_user(email='staff@email.com', tempname="Staff", is_staff=True)
		non_staff = pf.create_user(email='nonstaff@email.com', tempname='NonStaff')

		staff_prof = pf.create_user_profile(user=staff)
		non_staff_prof = pf.create_user_profile(user=non_staff)

		contrib_user = pf.create_user(email='contrib@email.com', tempname='Contrib')
		contrib = pf.create_contributor_profile(user=contrib_user)
		PendingContributors.objects.create(contributor=contrib)


	def test_non_staff_acess(self):
		c = Client()

		logged_in = c.login(username='nonstaff@email.com', password='password')
		self.assertTrue(logged_in, "User could not be logged in")

		response = c.get('/profile/contributors_approve/')

		self.assertRedirects(response, '/')

	def test_staff_access(self):
		c = Client()

		logged_in = c.login(username='staff@email.com', password='password')
		self.assertTrue(logged_in, "User could not be logged in")

		response = c.get('/profile/contributors_approve/')

		c1 = response.context['pending_contributors'][0].contributor

		self.assertEqual(str(c1), "Contrib McContribFace")

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-















