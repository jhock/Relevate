from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from ..models.adviser_model import Adviser, PendingAdvisers, DeniedAdvisers
from ..models.user_models import UserProfile
from ..models.contributor_model import ContributorProfile
from django.views.generic import View
from django.contrib import messages
from braces.views import LoginRequiredMixin
from ..forms.adviser_forms import AdviserCreateForm
from ..modules.adviser_util import get_adviser_profile
from datetime import datetime as dt
from ...contribution.models.post_model import Post, PendingPost
from ...contribution.modules.post_util import display_error


class AdviserListView(View):

	def get(self, request):
		"""
		Get a list of all advisers
		"""
		if (request.user.is_authenticated):
			user_prof = UserProfile.objects.get(user=request.user)
		else:
			user_prof = None
		advisers = Adviser.objects.filter(is_active=True)
		return render(request, "advisers_list.html", {
				'advisers': advisers,
				'user_prof': user_prof
			})


class DeniedAdviserListView(LoginRequiredMixin, View):
	"""
	Contains ``LoginRequiredMixin``
	"""

	def get(self, request):
		"""
		Denied advisers are stored in the DB. This view gets
		a list of them, but only if the user is a staff member. Otherwise,
		it redirects them to the home page.
		"""
		if (request.user.is_staff):
			user_prof = UserProfile.objects.get(user=request.user)
			denials = DeniedAdvisers.objects.all()
			return render(request, "denied_advisers.html",
				{
					'user_prof': user_prof,
					'advisers': denials
				})
		else:
			return HttpResponseRedirect(reverse_lazy("contribution:home"))



class AdviserApproveView(LoginRequiredMixin, View):
	"""
	Contains ``LoginRequiredMixin``
	"""

	def get(self, request):
		"""
		Shows a list of advisers that are waiting to be approved, with 
		options to either approve or deny them. Redirects to home if the user
		isn't a staff member.
		"""
		if (request.user.is_staff):
			user_prof = UserProfile.objects.get(user=request.user)
			pending_adviser_ids = PendingAdvisers.objects.values_list("adviser_id", flat=True)
			advisers = Adviser.objects.filter(id__in=pending_adviser_ids)
			return render(request, "adviser_approve.html", 
				{
					'advisers': list(advisers),
					'user_prof': user_prof
				})
		else:
			return HttpResponseRedirect(reverse_lazy("contribution:home"))



class ApproveButtonView(View):

	def post(self, request):
		"""
		This is an endpoint for an AJAX call, it will pull the ID from
		the data supplied and then mark that adviser as approved by setting ``is_adviser`` on
		the UserProfile to True, as well as setting ``is_active`` on the Adviser object to True.
		Finally, the entry corresponding to this adviser is deleted from the PendingAdvisers
		table.
		"""
		request_id = request.POST.get("id")
		adviser = Adviser.objects.get(id=int(request_id))
		user_prof = adviser.contributor_profile.user_profile
		print("Approving User: " + user_prof.user.first_name + " " + user_prof.user.last_name)
		user_prof.is_adviser = True
		user_prof.save()
		adviser.is_active = True
		adviser.save()
		PendingAdvisers.objects.filter(adviser_id=adviser.id).delete()
		return HttpResponse('')


class DenyButtonView(View):

	def post(self, request):
		"""
		This is an endpoint for an AJAX call, it will pull the ID from
		the data supplied and then mark that adviser as denied by adding them
		to the DeniedAdvisers table.
		"""
		request_id = request.POST.get("id")
		reason = request.POST.get('reason')
		adviser = Adviser.objects.get(id=int(request_id))
		user_prof = adviser.contributor_profile.user_profile
		print("Denying User: " + user_prof.user.first_name + " " + user_prof.user.last_name)
		PendingAdvisers.objects.filter(adviser_id=adviser.id).delete()
		denial = DeniedAdvisers(adviser=adviser,
								date_denied=dt.utcnow(),
								reason=reason)
		denial.save()
		# @US_TODO: Send an email explaining denial
		return HttpResponse('')


class AdviserCreateView(LoginRequiredMixin, View):
	"""
	Contains ``LoginRequiredMixin``
	"""

	def get(self, request):
		"""
		Returns the form to be filled out when applying to be an adviser, the ``AdviserCreateForm``.
		If the user is not already a contributor, it redirects them
		to the home view.
		"""
		user_prof = UserProfile.objects.get(user=request.user)
		if (not user_prof.is_contributor):
			return HttpResponseRedirect(reverse_lazy("contribution:home"))
		form = AdviserCreateForm
		return render(request, 'adviser_create.html',
						{'form':form, 'user_prof': user_prof})

	def post(self, request):
		"""
		If the form is valid, an ``Adviser`` object is created as well as a ``PendingAdvisers``
		object. The ``Adviser`` begins with ``is_active`` set to false until they are approved
		via view`profiles.AdviserApproveView`. 
		
		If the form is not valid, the form errors are rendered on the page in the form of 
		messages, and the form is redisplayed.
		"""
		form = AdviserCreateForm(request.POST)
		user_prof = UserProfile.objects.get(user=request.user)
		contrib_prof = ContributorProfile.objects.get(user_profile=user_prof)
		if (form.is_valid()):
			adviser = Adviser(
					contributor_profile = contrib_prof,
					accept_terms = form.cleaned_data.get('accept_terms'),
					is_active = False,
					is_available = True,
					description = form.cleaned_data.get('reason'),
					max_num_advisees = form.cleaned_data.get('number_of_advisees')
				)
			adviser.save()
			pending_adviser = PendingAdvisers(adviser=adviser)
			pending_adviser.save()
			messages.success(request, 'Your application has been submitted and being reviewed!')
			return HttpResponseRedirect(reverse_lazy('contribution:home'))
		else:
			display_error(form, request)
			return render(request, 'adviser_create.html',
							{
								'form': form, 
								'user_prof': user_prof
							})


class AdviserUpdateView(LoginRequiredMixin, View):
	"""
	Contains ``LoginRequiredMixin``
	"""

	def get(self, request):
		"""
		Gets the adviser object associated with the user and populates a form with
		the information in their profile and renders it to be updated.
		
		If the user is not an adviser, they are redirected to the home page.
		"""
		user_prof = UserProfile.objects.get(user=request.user)
		if (not user_prof.is_adviser):
			return HttpResponseRedirect(reverse_lazy("contribution:home"))
		adviser = get_adviser_profile(user_prof)
		form = AdviserCreateForm({
				'number_of_advisees': adviser.max_num_advisees,
				'reason': adviser.description,
				'accept_terms': adviser.accept_terms
			})
		return render(request, 'adviser_update.html', 
			{'form': form, 'user_prof': user_prof})

	def post(self, request):
		"""
		If the form submitted is valid, the ``Adviser`` object is updated with the new information.
		
		If the form is not valid, the errors are rendedered to the page and the form is repopulated.
		"""
		form = AdviserCreateForm(request.POST)
		user_prof = UserProfile.objects.get(user=request.user)
		if (form.is_valid()):
			adviser = get_adviser_profile(user_prof)
			adviser.max_num_advisees = form.cleaned_data.get('number_of_advisees')
			adviser.description = form.cleaned_data.get('reason')
			adviser.save()
			messages.success(request, 'Your profile has been updated!')
			return HttpResponseRedirect(reverse_lazy('profile:adviser_profile'))
		else:
			display_error(form, request)
			return render(request, 'adviser_update.html',
							{'form': form, 'user_prof': user_prof})


class AdviserProfileView(LoginRequiredMixin, View):
	"""
	Contains ``LoginRequiredMixin``
	"""

	def get(self, request):
		"""
		Gets the ``Adviser`` object associated with a user and displays it.
		
		If the user is not and adviser, they are redirected to the home page.
		"""
		user_prof = UserProfile.objects.get(user=request.user)
		if (not user_prof.is_adviser):
			return HttpResponseRedirect(reverse_lazy("contribution:home"))
		adviser = get_adviser_profile(user_prof)
		return render(request, "adviser_profile.html",
			{
				'user_prof': user_prof,
				'adviser': adviser
			})


class AboutAdviserView(LoginRequiredMixin, View):
	"""
	Contains ``LoginRequiredMixin``
	"""

	def get(self, request):
		"""
		Gets the ``Adviser`` object associated with a user and displays it.

		If the user is not and adviser, they are redirected to the home page.
		"""
		adviser_prof = Adviser.objects.all()
		return render(request, "about.html",
					  {
						  'adviser_prof': adviser_prof
					  })



class AdviserApprovePostView(LoginRequiredMixin, View):
	"""
	Contains ``LoginRequiredMixin``
	"""

	def get(self, request):
		"""
		Retrieves all posts from the ``PendingPost`` table for which the user is 
		listed as an adviser and displays them to the screen to be approved or denied.
		
		If the user is not an adviser, they are redirected home.
		"""
		user_prof = UserProfile.objects.get(user=request.user)
		if (not user_prof.is_adviser):
			return HttpResponseRedirect(reverse_lazy("contribution:home"))
		contrib_prof = ContributorProfile.objects.get(user_profile = user_prof)
		adviser = Adviser.objects.get(contributor_profile = contrib_prof)
		all_posts = PendingPost.objects.filter(adviser=adviser).values_list('post_id', flat=True)
		posts = Post.objects.filter(pk__in=all_posts)
		return render(request, 'adviser_approve_post.html', 
			{
				'user_prof': user_prof,
				'posts': posts
			})


class ApprovePostAjaxView(View):
	'''
	AJAX View
	'''

	def post(self, request):
		"""
		Gets the correct ``Post`` object via the supplied id,
		sets its ``isPublished`` to True and sets its ``is_pendings_adviser`` to False.
		It then removes the ``PendingPost`` entry from the table.
		"""
		request_id = request.POST.get("id")
		post = Post.objects.get(id=request_id)
		post.isPublished = True
		post.is_pending_adviser = False
		post.save()
		PendingPost.objects.get(post_id=request_id).delete()
		return HttpResponse("")


class DenyPostAjaxView(View):
	'''
	AJAX View
	'''

	def post(self, request):
		"""
		Gets the correct ``Post`` object via the id supplied, 
		"""
		request_id = request.POST.get("id")
		reason = request.POST.get('reason')
		# @US_TODO: send email about denied post
		PendingPost.objects.get(post_id=request_id).delete()
		post = Post.objects.get(id=request.POST.get('id'))
		post.is_pending_adviser = False
		post.save()
		return HttpResponse("")











