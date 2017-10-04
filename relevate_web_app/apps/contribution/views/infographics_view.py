from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from braces.views import LoginRequiredMixin
from ..forms.infographics_form import ArticleInfographicsCreate, ArticleInfographicUpdateForm
from ...profiles.models.user_models import UserProfile
from ..models.topic_model import Topics
from ..models.infographic_model import Infographic
from ..models.post_model import Post, PendingPost
from ...profiles.modules.contributor_util import user_can_contribute, has_adviser
from datetime import datetime
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from ..modules.infographic_util import get_infographic_crop
from ..modules.post_util import is_image_file, display_error
from django.template.defaultfilters import slugify
from django.conf import settings
import os


class InfographicCreateView(LoginRequiredMixin, View):
	'''
	Views for creating a new infographic
	'''

	def get(self, request):
		'''
		Gets the form for creating a new infographic
		'''
		form = ArticleInfographicsCreate()
		tag_names = Topics.objects.all().order_by('name')
		user_prof = UserProfile.objects.get(user=request.user)
		return render(request, 'article_infographics_create.html',
			{
				'form':form,
				'user_prof': user_prof,
				'tag_names': tag_names,
				'first_name':request.user.first_name,
				'last_name':request.user.last_name

			})

	def post(self, request):
		'''
		Actually creates the new infographic

		Also crops the top 300 pixels off the infographic and 
		saves it as the thumbnail
		'''
		form = ArticleInfographicsCreate(request.POST, request.FILES)
		user_prof = UserProfile.objects.get(user=request.user)
		tag_names = Topics.objects.all().order_by('name')
		if form.is_valid():
			content = form.cleaned_data.get('contents')
			title = form.cleaned_data['title']
			topics = form.cleaned_data.get('topic_choices')
			blurb = form.cleaned_data.get('blurb')
			contributor_profile = user_can_contribute(request.user)
			if contributor_profile:
				infographic = Infographic(
						title=title,
						image=content,
						blurb = blurb,
						is_image=True,
					)
				infographic.save()
				createdDate = datetime.utcnow()
				name = title + str(createdDate)
				thumb_name = slugify(name) + '.png'
				t = get_infographic_crop(content, thumb_name)
				if not (os.environ['DJANGO_SETTINGS_MODULE'] == 'settings.local'):
					infographic.thumbnail.name = settings.MEDIA_URL + 'media/article_infographic/thumbnails/' + thumb_name
				else:
					infographic.thumbnail.name = settings.MEDIA_URL + '/article_infographic/thumbnails/' + thumb_name
				infographic.save()
				post = Post(
						contributor= contributor_profile,
						is_infographic = True,
						infographic = infographic,
					)
				post.save()
				if (request.POST.get('hidden-publish-checkbox') == "on"):
					if (contributor_profile.has_adviser):
						pending_post = PendingPost(post=post, adviser=contributor_profile.advisers_profile)
						pending_post.save()
						post.is_pending_adviser = True
						messages.success(request, "Infographic Will be Published as Soon as your Adviser Confirms It!")
					else:
						post.publishDate = datetime.utcnow()
						post.isPublished = True
						messages.success(request, "Infographic Was Successfully Published!")
				else:
					messages.success(request, "Infographic Was Successfully Created!")
				for each_topic in topics:
					infographic.topics.add(each_topic)
				infographic.save()
				post.save()
				return HttpResponseRedirect(reverse_lazy('contribution:all_posts'))
			else:
				messages.warning(request, 'Need to be a contributor to post!')
				return HttpResponseRedirect(reverse_lazy("contribution:home"))
		display_error(form, request)
		return render(request, 'article_infographics_create.html', 
									{
										'form':form,
										'user_prof':user_prof, 
										'tag_names':tag_names,
										'first_name':request.user.first_name,
										'last_name':request.user.last_name
									})


class InfographicUpdateView(LoginRequiredMixin, View):
	'''
	For updating an infographic that already exists
	'''

	def get(self, request, slug):
		'''
		Gets the article to be updated and populates the form

		:param slug: Unique slug for the infographic
		'''
		already_sel = []
		post = Post.objects.get(slug=slug, is_deleted=False)
		infographic_post = post.infographic
		tag_names = Topics.objects.all().order_by('name')
		for top in infographic_post.topics.all():
				already_sel.append(top)
		form = ArticleInfographicUpdateForm(initial={'title':infographic_post.title,
													 'image':infographic_post.image,
													 'topic_choices':already_sel,
													 'is_published':post.isPublished,
													 'blurb': infographic_post.blurb,
													 })
		user_prof = UserProfile.objects.get(user=request.user)
		return render(request, 'article_infographic_update.html', 
							{
								'form':form,
								'user_prof':user_prof, 
								'tag_names': tag_names,
								'post':post,
								'already_sel': already_sel,
								'first_name':request.user.first_name,
								'last_name':request.user.last_name
							}
						)

	def post(self, request, slug):
		'''
		Actually performs the update of the infographic and recrops the thumbnail

		:param slug: Unique slug for the infographic
		'''
		form = ArticleInfographicUpdateForm(request.POST, request.FILES)
		post_ = Post.objects.get(slug=slug, is_deleted=False)
		infographic_post = post_.infographic
		user_prof = UserProfile.objects.get(user=request.user)
		tag_names = Topics.objects.all().order_by('name')
		if form.is_valid():
			title = form.cleaned_data.get("title")
			content = form.cleaned_data.get("contents")
			blurb = form.cleaned_data.get('blurb')
			if content:
				infographic_post.image = content
				infographic_post.blurb = blurb
				infographic_post.is_image = True
				createdDate = datetime.utcnow()
				name = title + str(createdDate)
				thumb_name = slugify(name) + '.png'
				t = get_infographic_crop(content, thumb_name)
				infographic_post.thumbnail.name = settings.MEDIA_URL + 'media/article_infographic/thumbnails/' + thumb_name
				infographic_post.save()
			is_published = form.cleaned_data.get('is_published')
			infographic_post.title = title
			contributor_profile = user_can_contribute(request.user)
			post_.save()
			if is_published:
				if contributor_profile.has_adviser:
					pending_post = PendingPost(post=post_, adviser=contributor_profile.advisers_profile)
					pending_post.save()
					post_.is_pending_adviser = True
					messages.success(request, "Infographic Will be Published as Soon as your Adviser Confirms It!")
				else:
					post_.isPublished = True
					messages.success(request, "Infographic Article Was Successfully Published!")
			post_.isPublished = is_published
			for each_topic in infographic_post.topics.all():
				try:
					infographic_post.topics.remove(each_topic)
				except ObjectDoesNotExist:
					pass
			for each_topic in form.cleaned_data.get("topic_choices"):
				infographic_post.topics.add(each_topic)
			post_.infographic = infographic_post
			post_.save()
			return HttpResponseRedirect(reverse_lazy("contribution:infographic_view", kwargs={'slug':slug}))
		display_error(form, request)
		return render(request, 'article_infographic_update.html', 
							{
								'form':form,
								'user_prof':user_prof,
								'post':post_,
								'tag_names':tag_names,
								'already_sel': infographic_post.topics.all(),
								'first_name':request.user.first_name,
								'last_name':request.user.last_name
							})


class InfographicsListView(LoginRequiredMixin, View):
	'''
	**DEPRICATED. USED ONLY FOR TESTING**
	'''

	def get(self, request):
		"""
		View to show only Infographic Listings
		"""
		contributor_profile = user_can_contribute(request.user)
		post_list = contributor_profile.post_set.all().filter(is_infographic=True)
		return render(request, 'article_infographics_list.html', {'info_list':post_list.infograhic,
																  'user_prof': contributor_profile.user_profile})


class InfographicView(LoginRequiredMixin, View):

	def get(self, request, slug):
		'''
		Gets the view for viewing an individual infographic.

		:param slug: Unique slug for the infographic
		'''
		post_ = Post.objects.get(slug=slug, is_deleted=False)
		infographic_post = post_.infographic
		user_prof = UserProfile.objects.get(user=request.user)
		contributor = user_can_contribute(request.user)
		is_user_article = False
		if user_prof.is_contributor == True:
			if contributor.id is post_.contributor.id or user_prof.user.email == "relevate@outlook.com":
				is_user_article = True
		else:
			post_.views = post_.views + 1
			post_.save()
		return render(request, 'article_infographic_view.html',
					  {'infographic':infographic_post,
					   'user_prof':user_prof,
					   'post':post_,
					   'is_user_article':is_user_article,
					   'first_name':request.user.first_name,
					   	'last_name':request.user.last_name
					   })

	def post(self, request, slug):
		'''
		For when the unpublish button is pressed, instead of going
		to the edit menu. It unpublishes the infographic

		:param slug: Unique slug for the infographic
		'''
		post_ = Post.objects.get(slug=slug, is_deleted=False)
		infographic_post = post_.infographic
		user_prof = UserProfile.objects.get(user=request.user)
		try:
			if request.POST.get('change_publish_true'):
				post_.isPublished = True
			elif request.POST.get('change_publish_false'):
				post_.isPublished = False
			post_.save()
		except ObjectDoesNotExist:
			pass
		contributor = user_can_contribute(request.user)
		if contributor.id is post_.contributor.id:
			is_user_article = True
		else:
			post_.views = post_.views + 1
			post_.save()
			is_user_article = False
		return render(request, 'article_infographic_view.html',
					  {'infographic':infographic_post,
					   'user_prof':user_prof,
					   'post':post_,
					   'is_user_article':is_user_article,
					   'first_name':request.user.first_name,
					   'last_name':request.user.last_name
					   })



