from ...profiles.models.user_models import UserProfile
from ...profiles.models.contributor_model import ContributorProfile
from ..forms.link_forms import LinkCreateForm, LinkUpdateForm
from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from datetime import datetime
from ..models.link_model import Link
from ..models.post_model import Post, PendingPost
from django.template.defaultfilters import slugify
from ..models.topic_model import Topics
from django.contrib import messages
from ..modules.post_util import display_error
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import os.path
from PIL import Image
from django.conf import settings

class LinkCreateView(LoginRequiredMixin, View):
	'''
	Get and post for creating a link.
	'''

	def get(self, request):
		'''
		Returns the blank form for creating a link
		'''
		user_prof = UserProfile.objects.get(user=request.user)
		form = LinkCreateForm()
		tag_names = Topics.objects.all().order_by('name')
		return render(request, 'link_create.html',
			{
				'form' : form,
				'user_prof': user_prof,
				'tag_names': tag_names,
				'first_name':request.user.first_name,
				'last_name':request.user.last_name
			})

	def post(self, request):
		'''
		Checks form validity, then creates a new post object of type
		link.
		'''
		user_prof = UserProfile.objects.get(user=request.user)
		contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
		form = LinkCreateForm(request.POST, request.FILES)
		if form.is_valid():
			createdDate = datetime.utcnow()
			image = form.cleaned_data.get('image')

			#The following is commented out until a design for cropping is decided upon.
			# x = form.cleaned_data.get('x')
			# y = form.cleaned_data.get('y')
			# w = form.cleaned_data.get('width')
			# h = form.cleaned_data.get('height')
			link = Link(
				title = form.cleaned_data.get('title'),
				image = image,
				url = form.cleaned_data.get('link'),
				description = form.cleaned_data.get('blurb')
				)
			link.save()
			if image:
				link.image = image
				# The following is commented out until a design for cropping is decided upon.
				"""
				# Gets the original image to be cropped
				photo = Image.open(form.cleaned_data.get('image'))
				# Cropps the image using values x,y,w,and h from the form
				cropped_image = photo.crop((x, y, w + x, h + y))
				# Splits the file name and the extension
				filename, file_extension = os.path.splitext(
					os.path.basename(urlparse(link.image.url).path))
				cropped_image.save(settings.BASE_DIR + "/media/links/images/" + filename + file_extension)
				link.image = "links/images/" + filename + file_extension
				"""
			topics = form.cleaned_data.get('topic_choices')
			for each_topic in topics:
				link.topics.add(each_topic)
			link.save()
			# @US_TODO: Do the pending adviser logic here
			post = Post(
					contributor = contrib_prof,
					is_link = True,
					link = link,
					createdDate = createdDate,
					updatedDate = createdDate,
				)
			post.save()
			if (request.POST.get('hidden-checkbox') == "on"):
				if (contrib_prof.has_adviser):
					pending_post = PendingPost(post=post, adviser=contrib_prof.advisers_profile)
					post.is_pending_adviser = True
					pending_post.save()
					messages.success(request, "Link will be published as soon as your adviser confirms it!")
				else:
					post.isPublished = True
					post.publishDate = datetime.utcnow()
					messages.success(request, "Link was successfully published!")
			else:
				messages.success(request, "Link was successfully created!")
			post.save()
			return HttpResponseRedirect(reverse_lazy("contribution:all_posts"))
		else:
			tag_names = Topics.objects.all().order_by('name')
			display_error(form, request)
			return render(request, 'link_create.html', 
				{
					'form':form,
					'user_prof':user_prof,
					'tag_names':tag_names,
					'first_name':request.user.first_name,
					'last_name':request.user.last_name
				})


class LinkPreview(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, 'previews/link_preview.html')


class LinkUpdateView(LoginRequiredMixin, View):

	def get(self, request, slug):
		'''
		Populates the form for updating a link

		:param slug: Unique slug for the infographic
		'''
		user_prof = UserProfile.objects.get(user = request.user)
		post = Post.objects.get(slug=slug)
		link = post.link
		topics = link.topics.all()
		topic_list = []
		already_sel = []
		print(link.image.url)
		for t in topics:
			already_sel.append(t)
			topic_list.append( (t.id) )
		form = LinkUpdateForm(
				initial = {
					'title': link.title,
					'blurb': link.description,
					'link': link.url,
					'topic_choices': topic_list,
					'image': link.image
				}
			)
		return render(request, 'link_update.html',
			{
				'user_prof': user_prof,
				'form': form,
				'link': link,
				'post': post,
				'length': len(link.description),
				'tag_names':Topics.objects.all().order_by('name'),
				'already_sel':already_sel,
				'slug':slug,
				'first_name':request.user.first_name,
				'last_name':request.user.last_name
			})

	def post(self, request, slug):
		'''
		Actually updates the link after validating the form

		:param slug: Unique slug for the infographic
		'''
		form = LinkUpdateForm(request.POST, request.FILES)
		user_prof = UserProfile.objects.get(user=request.user)
		contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
		post = Post.objects.get(slug=slug)
		if form.is_valid():
			link = post.link
			link.title = form.cleaned_data.get('title')
			link.description = form.cleaned_data.get('blurb')
			image = form.cleaned_data.get('image')
			# The following is commented out until a design for cropping is decided upon.
			# x = form.cleaned_data.get('x')
			# y = form.cleaned_data.get('y')
			# w = form.cleaned_data.get('width')
			# h = form.cleaned_data.get('height')
			if image:
				print("has image")
				# Gets the original image to be cropped

				try:
					link.image = image
					# The following is commented out until a design for cropping is decided upon.
					"""
					photo = Image.open(image)
					# Cropps the image using values x,y,w,and h from the form
					cropped_image = photo.crop((x, y, w + x, h + y))
					# Splits the file name and the extension
					filename, file_extension = os.path.splitext(
						os.path.basename(urlparse(link.image.url).path))
					cropped_image.save(settings.BASE_DIR + "/media/links/images/" + filename + file_extension)
					link.image = "links/images/" + filename + file_extension
					"""
				except:
					print("there was an error")
			print (link.image.url)
			link.save()
			print (link.image.url)
			post.updatedDate = datetime.utcnow()
			post.save()
			if (request.POST.get('hidden-checkbox') == "on"):
				if (contrib_prof.has_adviser):
					pending_post = PendingPost(post=post, adviser=contrib_prof.advisers_profile)
					post.is_pending_adviser = True
					pending_post.save()
					messages.success(request, "Link will be published as soon as your adviser confirms it!")
				else:
					post.isPublished = True
					post.publishDate = datetime.utcnow()
					messages.success(request, "Link was successfully published!")
			else:
				messages.success(request, "Link was successfully created!")
			curr_topics = link.topics.all()
			new_topics = form.cleaned_data.get('topic_choices')
			# Loop through and remove all the ones that aren't in the
			# new set
			for i in curr_topics:
				if (i not in new_topics):
					link.topics.remove(i)
			# Loop through and add all the ones that weren't
			# in the previous set
			for i in new_topics:
				if (i not in curr_topics):
					link.topics.add(i)
			link.save()
			post.save()
			print (link.image.url)
			return HttpResponseRedirect(reverse_lazy('contribution:all_posts'))
		else:
			display_error(form, request)
			return render(request, 'link_update.html',
				{
					'form':form,
					'user_prof':user_prof,
					'tag_names': Topics.objects.all().order_by('name'),
					'already_sel': post.link.topics.all(),
					'first_name':request.user.first_name,
					'last_name':request.user.last_name
				})






