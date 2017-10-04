from django.test import Client, TestCase
from ...utility_testing_methods import ProfileFactory

pf = ProfileFactory()


class TestHomeView(TestCase):

	def setUp(self):
		simple_user = pf.create_user(email='simple@email.com', first_name='Simple',
				last_name='McSimpleFace')
		contrib_user = pf.create_user(email='contrib@email.com', first_name='Contrib',
				last_name='McContribFace')
		self.simple = pf.create_user_profile(user=simple_user)
		self.contrib = pf.create_contributor_profile(user=contrib_user)

	def test_home_not_logged_in(self):
		c = Client()
		response = c.get('/')

		self.assertEqual(response.status_code, 200, "Didn't return a 200 status code.")
		with self.assertRaises(KeyError):
			response.context['user_prof']
		with self.assertRaises(KeyError):
			response.context['contrib_prof']

	def test_home_user_logged_in(self):
		c = Client()
		logged_in = c.login(username=self.simple.user.username, password='password')

		self.assertTrue(logged_in, 'User couldn\'t be logged in.')

		response = c.get('/')

		self.assertEqual(response.status_code, 200, "Didn't return a 200 status code.")
		self.assertEqual(response.context['user_prof'].user, self.simple.user)
		with self.assertRaises(KeyError):
			response.context['contrib_prof']

	def test_home_contrib_logged_in(self):
		c = Client()

		logged_in = c.login(username=self.contrib.user_profile.user.username, password='password')

		self.assertTrue(logged_in, 'User couldn\'t be logged in.')

		response = c.get('/')

		self.assertEqual(response.status_code, 200, "Didn't return a 200 status code.")
		self.assertEqual(response.context['user_prof'].user, self.contrib.user_profile.user)
		self.assertEqual(response.context['contrib_prof'].user_profile.user, self.contrib.user_profile.user)

# =-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class TestAboutView(TestCase):

	def setUp(self):
		simple_user = pf.create_user(email='simple@email.com', first_name='Simple',
				last_name='McSimpleFace')
		contrib_user = pf.create_user(email='contrib@email.com', first_name='Contrib',
				last_name='McContribFace')
		self.simple = pf.create_user_profile(user=simple_user)
		self.contrib = pf.create_contributor_profile(user=contrib_user)

	def test_about_not_logged_in(self):
		c = Client()
		response = c.get('/about/')

		self.assertEqual(response.status_code, 200, "Didn't return a 200 status code.")
		with self.assertRaises(KeyError):
			response.context['user_prof']
		with self.assertRaises(KeyError):
			response.context['contrib_prof']

	def test_about_user_logged_in(self):
		c = Client()
		logged_in = c.login(username=self.simple.user.username, password='password')

		self.assertTrue(logged_in, 'User couldn\'t be logged in.')

		response = c.get('/about/')

		self.assertEqual(response.status_code, 200, "Didn't return a 200 status code.")
		self.assertEqual(response.context['user_prof'].user, self.simple.user)
		with self.assertRaises(KeyError):
			response.context['contrib_prof']

	def test_about_contrib_logged_in(self):
		c = Client()

		logged_in = c.login(username=self.contrib.user_profile.user.username, password='password')

		self.assertTrue(logged_in, 'User couldn\'t be logged in.')

		response = c.get('/about/')

		self.assertEqual(response.status_code, 200, "Didn't return a 200 status code.")
		self.assertEqual(response.context['user_prof'].user, self.contrib.user_profile.user)
		self.assertEqual(response.context['contrib_prof'].user_profile.user, self.contrib.user_profile.user)












