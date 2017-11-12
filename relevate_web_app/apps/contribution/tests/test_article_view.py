from django.test import TestCase, Client
from ..models.article_model import Article
from ..models.topic_model import Topics
from ...utility_testing_methods import ProfileFactory, ArticleFactory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ...profiles.modules.contributor_util import user_can_contribute
from ..forms.article_forms import *
import os
from .test_files.test_variables import ARTICLE_MASSIVE_WORDS_TEXTS

user_profile = ProfileFactory()
#test files
home_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
test_file_dir = os.path.join(home_dir, 'tests/test_files')
test_article_image = os.path.join(test_file_dir, 'article_test_image.jpg')
test_non_pic_file = os.path.join(test_file_dir, 'test_non_pic_file.docx')


def test_topics_ids(queried):
	"""
	Test Topic item given a querylist from topics table
	:param queried: the list of topics query items
	:return:
	"""
	topic_id = []
	print(type(queried))
	for each_topic in queried:
		print(each_topic)
		topic_id.append(each_topic.id)
	return topic_id


class ArticleTestCase(TestCase):
	"""
		Article Unit Test Class
	"""
	def setUp(self):
		"""
		Sets up the requires for the testing of the article
		:return:
		"""
		user = user_profile.create_user(email='adviser@email.com', first_name='Adviser',
				last_name='McAdviserFace')
		self.user_prof = user_profile.create_user_profile(user=user)
		Topics.objects.create(name='getting drafted', description='healthing drafting')
		Topics.objects.create(name='getting secured', description='healthing desont matter')
		Topics.objects.create(name='getting smart', description='healthing so what')
		Topics.objects.create(name='getting there', description='healthing works')
		self.topics = Topics.objects.all()

	def test_non_contributor_redirected(self):
		"""
		Test to see if a non contributor is redirected to the appropiate page
		:return:
		"""
		client = Client()
		self.assertEqual(self.user_prof.user.username, 'adviser@email.com')
		logged_in = client.login(username=self.user_prof.user.username, password='password')
		response = client.get('/article_create/')
		self.assertTrue(logged_in, True)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/')

	def test_article_form_correct_input(self):
		"""
		Test to see if the correct form  input redirects user to the success page
		:return:
		"""
		client = Client()
		contributor = user_profile.create_contributor_profile(user_profile=self.user_prof, user=self.user_prof.user)
		logged_in = client.login(username=contributor.user_profile.user.username, password='password')
		response = client.get('/article_create/', follow=True)
		self.assertTrue(logged_in, True)
		self.assertEqual(user_can_contribute(contributor.user_profile.user), contributor)
		self.assertEqual(response.status_code, 200)
		query_topic = Topics.objects.all()[0:2]
		with open(test_article_image, 'rb') as the_image:
			response = client.post('/article_create/', data={'title':'testing non user',
													'content':"I was suppose to do this",
													'image':the_image,
													'topic_choices': test_topics_ids(query_topic),
													}, follow=True)
		red_path, red_code = response.redirect_chain[0]
		self.assertEqual(red_path, '/all_posts/')
		self.assertEqual(red_code, 302)

	def test_article_form_no_input_file(self):
		"""
		Test to see if user's failure to upload the required files is handled correctly
		:return:
		"""
		client = Client()
		contributor = user_profile.create_contributor_profile(user_profile=self.user_prof, user=self.user_prof.user)
		logged_in = client.login(username=contributor.user_profile.user.username, password='password')
		response = client.get('/article_create/', follow=True)
		self.assertTrue(logged_in, True)
		self.assertEqual(user_can_contribute(contributor.user_profile.user), contributor)
		self.assertEqual(response.status_code, 200)
		query_topic = Topics.objects.all()[0:2]
		with open(test_non_pic_file, 'rb') as the_image:
			response = client.post('/article_create/', data={'title':'okay what is ',
													'content':"I was suppose to do this",
													'image':the_image,
													'topic_choices': test_topics_ids(query_topic),
													}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn('For this field:', str(response.content))

	def test_valid_update_form(self):
		"""
		Test to see if article update works correctly with appropiate inputs
		:return:
		"""
		client = Client()
		article_fac = ArticleFactory()
		contributor = user_profile.create_contributor_profile(user_profile=self.user_prof, user=self.user_prof.user)
		logged_in = client.login(username=contributor.user_profile.user.username, password='password')
		self.assertTrue(logged_in, True)
		post = article_fac.create_post(contributor, image=test_article_image)
		response = client.get('/articles_update/'+str(post.slug)+'/')
		self.assertEqual(response.status_code, 200)
		query_topic = self.topics[1:3]
		with open(test_article_image, 'rb') as the_image:
			response = client.post('/articles_update/'+str(post.slug)+'/', data={'title':'okay what is',
												'content':"I was suppose to do this",
												'image':the_image,
												'topic_choices': test_topics_ids(query_topic),
												'isPublished':False
												}, follow=True)

		red_path, red_code = response.redirect_chain[0]
		self.assertEqual(red_path, '/all_posts/')
		self.assertEqual(red_code, 302)
		new_post = article_fac.get_post_object(post.slug)
		self.assertEqual(new_post.article.content, "I was suppose to do this")
		self.assertEqual(new_post.article.title, "okay what is")
		for each_item in query_topic:
			self.assertIn(each_item, new_post.article.article_topics.all())

	def test_invalid_updated_form(self):
		"""
		Test to see if article update form responded approipately to invalid form input
		:return:
		"""
		client = Client()
		article_fac = ArticleFactory()
		contributor = user_profile.create_contributor_profile(user_profile=self.user_prof, user=self.user_prof.user)
		logged_in = client.login(username=contributor.user_profile.user.username, password='password')
		self.assertTrue(logged_in, True)
		post = article_fac.create_post(contributor, image=test_article_image)
		response = client.get('/articles_update/'+str(post.slug)+'/')
		self.assertEqual(response.status_code, 200)
		query_topic = self.topics[1:3]
		with open(test_article_image, 'rb') as the_image:
			response = client.post('/articles_update/'+str(post.slug)+'/', data={'title':ARTICLE_MASSIVE_WORDS_TEXTS,
												'content':ARTICLE_MASSIVE_WORDS_TEXTS,
												'image':the_image,
												'topic_choices': test_topics_ids(query_topic),
												'isPublished':False
												}, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertIn('For this field:', str(response.content))



