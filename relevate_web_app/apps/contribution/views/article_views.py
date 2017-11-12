from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View, FormView
from ..models.article_model import Article
from ..forms.article_forms import *
from braces.views import LoginRequiredMixin
from django.contrib import messages
from ...profiles.modules.contributor_util import user_can_contribute, has_adviser
from ..modules.post_util import add_to_pending_post
from datetime import datetime
from ..models.topic_model import Topics
from django.core.exceptions import ObjectDoesNotExist
from ...profiles.models.user_models import UserProfile
from ...profiles.models.contributor_model import ContributorProfile
import json
from ..models.post_model import Post, PendingPost
from ..modules.post_util import display_error, is_image_file
from django.conf import settings
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import os.path
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

class NewPostView(View):

	def get(self, request):
		"""
        Displays the about page containing the team members and
        contact info
        """
		if request.user.is_authenticated:
			user_prof = UserProfile.objects.get(user=request.user)
			if (user_prof.is_contributor):
				return render(request, "new_post.html", {'user_prof': user_prof,})
			else:
				return render(request, "home.html")
		else:
			return render(request, "home.html")


class ArticleCreateView(LoginRequiredMixin, FormView):
	"""
		A class that represents the a new article creation page.
	"""


	def get(self, request, *args, **kwargs):
		"""

		The get request to view the article
		
		:return: an http response showing the article form for creating new article

		"""
		user_prof = UserProfile.objects.get(user=request.user)
		form = ArticleCreateForm()
		tag_names = Topics.objects.all().order_by('name')
		if not user_can_contribute(request.user):
			return HttpResponseRedirect(reverse("contribution:home"))
		return render(request, 'article_create.html', 
			{
				'form':form,
				'user_prof': user_prof,
				'tag_names':tag_names,
				'first_name':request.user.first_name,
				'last_name':request.user.last_name
			})

	def post(self, request, *args, **kwargs):
		"""
			The post request for creating a new article
			
			:return: an http response that redirects to a new page if article creation is successful
		"""
		user_prof = UserProfile.objects.get(user=request.user)
		contrib_prof = user_can_contribute(request.user)
		form = ArticleCreateForm(request.POST, request.FILES)
		if form.is_valid():
			title = form.cleaned_data['title']
			content = form.cleaned_data.get('content')
			topics = form.cleaned_data.get('topic_choices')
			x = form.cleaned_data.get('x')
			y = form.cleaned_data.get('y')
			w = form.cleaned_data.get('width')
			h = form.cleaned_data.get('height')
			image = form.cleaned_data.get('image')
			url_image = form.cleaned_data.get('url_image')
			blurb = form.cleaned_data.get('blurb')
			references = form.cleaned_data.get('references')
			contributor_profile = user_can_contribute(request.user)
			if contributor_profile:
				new_article = Article(
						title=title, 
						content=content,
						image = image,
						blurb = blurb,
						references = references
					)
				new_article.save()
				#If user inputs image file instead of url
				if image:
					#Gets the original image to be cropped
					photo = Image.open(form.cleaned_data.get('image'))
					#Cropps the image using values x,y,w,and h from the form
					cropped_image = photo.crop((x, y, w + x, h + y))
					#Splits the file name and the extension
					filename, file_extension = os.path.splitext(os.path.basename(urlparse(new_article.image.url).path))
					cropped_image.save(settings.BASE_DIR+"/media/articles/images/"+filename+file_extension)
					new_article.image = "articles/images/"+filename+file_extension
				#If user inputs url instead of image file
				elif url_image:
					img_temp = NamedTemporaryFile(delete=True)
					img_temp.write(urlopen(url_image).read())
					img_temp.flush()
					new_article.image.save(url_image, File(img_temp))
				new_article.save()

				post = Post(
						contributor= contributor_profile,
						is_article = True,
						article = new_article,
					)
				post.save()
				if (request.POST.get('hidden-publish-checkbox') == "on"):
					if (contrib_prof.has_adviser):
						pending_post = PendingPost(post=post, adviser=contrib_prof.advisers_profile)
						pending_post.save()
						post.is_pending_adviser = True
						messages.success(request, "Article Will be Published as Soon as your Adviser Confirms It!")
					else:
						post.publishDate = datetime.utcnow()
						post.isPublished = True
						messages.success(request, "Article Was Successfully Published!")
				else:
					messages.success(request, "Article Was Successfully Created!")

				for each_topic in topics:
					new_article.article_topics.add(each_topic)
				new_article.save()
				post.save()
				print ("Article went through")
				return HttpResponseRedirect(reverse_lazy('contribution:all_posts'))
			else:
				return HttpResponseRedirect(reverse_lazy("contribution:home"))
		else:
			print("Invalid")
			display_error(form, request)
			return render(request, 'article_create.html', 
				{
					'form':form,
					'user_prof':user_prof,
					'tag_names': Topics.objects.all().order_by('name'),
					'first_name':request.user.first_name,
					'last_name':request.user.last_name
				})


class ArticleRemoveView(LoginRequiredMixin, View):

	"""
		An class representing an Ajax request for deleting an article
	"""

	def post(self, request):
		"""
		The function that the jquery AJAX request calls
		"""
		response = {}
		try:
			post = Post.objects.get(slug=str(request.POST.get('slug')))
			post.is_deleted = True
			post.save()
			response["deleted"] = True
		except (AttributeError, ValueError, KeyError):
			response["deleted"] = False
		return HttpResponse(json.dumps(response))


class ArticleUpdateView(LoginRequiredMixin, View):
	"""
	A class representing the  page for updating an individual article
	"""

	def get(self, request, slug):
		"""
		The get function that get the article edit page

		:param slug: the unique url for each article
		
		:return: the page for viewing the article
		"""
		user_prof = UserProfile.objects.get(user=request.user)
		try:
			post = Post.objects.get(slug=str(slug), is_deleted=False)
			article = post.article
			list_of_topics = []
			already_sel = []
			for top in article.article_topics.all():
				list_of_topics.append(top.id)
				already_sel.append(top)
			rest = Topics.objects.all().order_by('name')

			form = ArticleUpdateForm(
				initial={
					'title':article.title,
					'content':article.content,
					'topic_choices':list_of_topics,
					'isPublished':post.isPublished,
					'image': article.image,
					'blurb': article.blurb,
					'references': article.references
			})
			return render(request, 'article_update.html', 
					{
						'form':form, 
						'article':article,
						'user_prof': user_prof,
						'post':post,
						'already_sel':already_sel,
						'tag_names': rest,
						'first_name':request.user.first_name,
						'last_name':request.user.last_name
					})
		except ObjectDoesNotExist:
			return HttpResponseRedirect(reverse('contribution:all_posts'))

	def post(self, request, slug):
		"""
		This function create a post request to reflect the edits on the page
			
		:param slug: the unique url for each article
		
		:return: returns an http response that redirects to users list of articles upon successful completion of edit
		"""
		user_prof = UserProfile.objects.get(user=request.user)
		contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
		list_of_topics = []
		post = Post.objects.get(slug=slug, is_deleted=False)
		article = post.article
		article_topics = article.article_topics.all()
		tag_names = Topics.objects.all().order_by('name')
		already_sel = []
		for top in article_topics:
			list_of_topics.append(top.id)
			already_sel.append(top)
		form = ArticleUpdateForm(request.POST, request.FILES)
		if form.is_valid():
			article.title = form.cleaned_data.get("title")
			article.content = form.cleaned_data.get("content")
			article.references = form.cleaned_data.get('references')
			image = form.cleaned_data.get("image")

			x = form.cleaned_data.get('x')
			y = form.cleaned_data.get('y')
			w = form.cleaned_data.get('width')
			h = form.cleaned_data.get('height')

			blurb = form.cleaned_data.get('blurb')
			article.blurb = blurb

			# If user inputs image file instead of url
			if image:
				article.image = image
				# Gets the original image to be cropped
				photo = Image.open(image)
				# Crops the image using values x,y,w,and h from the form
				cropped_image = photo.crop((x, y, w + x, h + y))
				# Splits the file name and the extension
				filename, file_extension = os.path.splitext(os.path.basename(urlparse(image.name).path))
				cropped_image.save(settings.BASE_DIR + "/media/articles/images/" + filename + file_extension)
				article.image = "articles/images/" + filename + file_extension
			article.save()
			post.updateDate = datetime.utcnow()
			for each_topic in list_of_topics:
				try:
					article.article_topics.remove(each_topic)
				except ObjectDoesNotExist:
					pass
			for each_topic in form.cleaned_data.get("topic_choices"):
				article.article_topics.add(each_topic)
			if (request.POST.get('hidden-publish-checkbox') == "on"):
				if (contrib_prof.has_adviser):
					pending_post = PendingPost(post=post, adviser=contrib_prof.advisers_profile)
					pending_post.save()
					post.is_pending_adviser = True
					messages.success(request, "Article Will be Published as Soon as your Adviser Confirms It!")

				else:
					post.publishDate = datetime.utcnow()
					post.isPublished = True
					messages.success(request, "Article Was Successfully Published!")
			else:

				messages.success(request, "Article Was Successfully Updated!")
			article.save()
			post.save()

			return HttpResponseRedirect(reverse_lazy("contribution:article_view", kwargs={'slug':slug}))
		display_error(form, request)
		return render(request, 'article_update.html', 
				{
					'form':form, 
					'article':article,
					'user_prof': user_prof,
					'post':post,
					'tag_names':tag_names,
					'already_sel':already_sel,
					'first_name':request.user.first_name,
					'last_name':request.user.last_name
				})


class ArticleIndividualView(LoginRequiredMixin, View):
	"""
		Class for view individual articles
	"""

	def get(self, request, slug):
		"""
		The get request for the view

		:param slug: this is a unique url identifier for each article

		"""
		user_prof = UserProfile.objects.get(user=request.user)
		try:
			post = Post.objects.get(slug=str(slug), is_deleted=False)
			article = post.article
			contributor = user_can_contribute(request.user)
			is_user_article = False
			if user_prof.is_contributor == True:
				if contributor.id is post.contributor.id or user_prof.user.email == "relevate@outlook.com":
					is_user_article = True
			else:
				post.views = post.views + 1
				post.save()
			return render(request, 'article_view.html', 
				{
					'article':article, 
					'is_user_article':is_user_article, 
					'user_prof':user_prof,
					'post': post,
					'first_name':request.user.first_name,
					'last_name':request.user.last_name
				})
		except ObjectDoesNotExist:
			return HttpResponseRedirect(reverse('contribution:all_posts'))

	def post(self, request, slug):
		"""
		The post request to make changes to the individual article

		:param slug: the unique url identifier

		"""
		user_prof = UserProfile.objects.get(user=request.user)
		try:
			post = Post.objects.get(slug=str(slug), is_deleted=False)
			article = post.article
			if request.POST.get('change_publish_true'):
				post.isPublished = True
			elif request.POST.get('change_publish_false'):
				post.isPublished = False
			post.save()
			return render(request, 'article_view.html', 
				{
					'article':article, 
					'is_user_article':True, 
					'user_prof':user_prof,
					'post': post,
					'first_name':request.user.first_name,
					'last_name':request.user.last_name
				})
		except ObjectDoesNotExist:
			pass
		return HttpResponseRedirect(reverse('contribution:all_posts'))
