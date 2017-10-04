from django.test import Client, TestCase
from ...utility_testing_methods import ProfileFactory
from ..models.adviser_model import DeniedAdvisers
from datetime import datetime as dt

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

















