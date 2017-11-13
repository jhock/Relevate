from django.shortcuts import render
from ..forms.authentication_forms import RegistrationForm, LoginForm, ConfirmationForm
from ..forms.authentication_forms import PasswordChangeForm, PasswordResetRequestForm, SetPasswordForm, UpdateUserForm
from ...profiles.models.user_models import User, UserProfile
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from ...profiles.models.confirmation_model import Confirmation
from braces.views import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.views.generic import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.template import *
from ...contribution.models.topic_model import Topics
from ...contribution.modules.post_util import display_error

from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect, QueryDict
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView


class RegisterUserView(View):
	"""
	Returns the form to be filled out when registering, the 'RegistrationForm``.
	If the user is already authenticated, it redirects them
	to the home view.
	"""
	def get(self, request):
		if request.user.is_authenticated():
			return HttpResponseRedirect(reverse('contribution:home'))
		return render(request, 'registration.html', {'form': RegistrationForm()}, RequestContext(request, locals()))

	"""
	If the form is valid, a ``User`` object is created as well as a ``PendingAdvisers``
	object. The ``User`` begins with ``confirmed`` set to false until they are confirmed as a user.

	Once ``User`` object is created, and ``EmailMessage`` is created to provide the user ``user_email``
	with a unique ``confirmation_code``

	If the form is not valid, the form errors are rendered on the page in the form of
	messages, and the form is redisplayed.
	"""
	def post(self, request):
		form = RegistrationForm(request.POST)
		if form.is_valid():
			auto_confirm = True #Flag for autoconfirm for beta testing, when set to True, autoconfirm
			#Get user data from form
			password = form.cleaned_data['password1']
			email = form.cleaned_data['email']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			#Create a new user
			user = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name)
			#Activate and save user
			user.is_active = True
			user.save()
			user_profile = UserProfile(user=user)
			user_profile.save()
			for each_topic in form.cleaned_data.get('area_of_expertise'):
				user_profile.topics_preferences.add(each_topic)
			#If autoconfirm set for testing, a confirmation email will not be sent, user redirected to home.
			if auto_confirm:
				user_profile.confirmed = True
				user_profile.save()
				messages.success(request, 'Your account has been created!')
				login(request, user)
				return HttpResponseRedirect(reverse('profile:user_contributor_question'))
			else:
				#save user profile, and create a confirmation code.
				user_profile.save()
				code = User.objects.make_random_password(length=6, allowed_chars='0123456789')
				confirmation_code = code + str(user_profile.user.id)
				confirmation_model = Confirmation.objects.create(user_profile=user_profile, confirmation_code=confirmation_code)
				#Setting up confirmation email.
				user_name = first_name + last_name
				user_email = email
				template = get_template('confirmation_email_content.html')
				context = Context({'userName': user_name,
				 'email': email,
				 'magic_link': 'myrelevate.com/%s/%s' % (email, code)})
				content = template.render(context)
				email_message = EmailMessage('Confirm Your Account with MyRelevate', content + confirmation_code, 'relevate@outlook.com', [user_email], headers={'Reply-To': 'relevate@outlook.com'})
				email_message.content_subtype = "html"
				try:
					email_message.send()
				except:
					messages.error(request, 'Email could not be sent')
				#confirmation email sent.
				messages.success(request, 'Your account has been created! Check your email to complete confirmation.')
				login(request, user)
				return HttpResponseRedirect(reverse('profile:confirmation'))
			#Error for account creation. (To Do: specific errors)
		messages.error(request, 'Your account could not be created, please try again.')
		return render(request, 'registration.html', {'form': RegistrationForm()}, RequestContext(request, locals()))


class DeactivatedAccountView(View):
	"""
	In Progress
	"""

	def get(self, request):
		return render(request, 'deactivated_account.html')


class ResetPasswordRequestView(FormView):
	success_url = './'
	form_class = PasswordResetRequestForm
	template_name = 'password_reset_form.html'

	@staticmethod
	def validate_email_address(email):
		try:
			validate_email(email)
			return True
		except ValidationError:
			return False

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			data = form.cleaned_data["email"]
		if self.validate_email_address(data) is True:  # uses the method written above
			'''
			If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
			'''
			associated_users = User.objects.filter(Q(email=data) | Q(username=data))
			if associated_users.exists():
				for user in associated_users:
					c = {
						'email': user.email,
						'domain': request.META['HTTP_HOST'],
						'site_name': 'your site',
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'user': user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					subject_template_name = 'password_reset_subject.txt'

					email_template_name = 'password_reset_email.html'

					subject = loader.render_to_string(subject_template_name, c)

					subject = ''.join(subject.splitlines())
					email = loader.render_to_string(email_template_name, c)
					send_mail(subject, email, 'relevate@outlook.com', [user.email], fail_silently=False)
				result = self.form_valid(form)
				messages.success(request,								 'An email has been sent to ' + data + ". Please check its inbox to continue reseting password.")
				return self.form_valid(form)
			messages.error(request, 'No user is associated with this email address')
			return render(request, 'password_reset.html', {'form': PasswordResetRequestForm()})

		else:
			'''
			If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
			'''
			associated_users = User.objects.filter(username=data)
			if associated_users.exists():
				for user in associated_users:
					c = {
						'email': user.email,
						'domain': 'myrelevate.com',
						'site_name': 'example',
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'user': user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					subject_template_name = 'password_reset_subject.txt'
					email_template_name = 'password_reset_email.html'
					subject = loader.render_to_string(subject_template_name, c)

					subject = ''.join(subject.splitlines())
					email = loader.render_to_string(email_template_name, c)
					send_mail(subject, email, 'relevate@outlook.com', [user.email], fail_silently=False)
				result = self.form_valid(form)
				messages.success(request,
								 'Email has been sent to ' + data + "'s email address. Please check its inbox to continue reseting password.")
				return HttpResponseRedirect(reverse(result))
			messages.error(request, 'No user is associated with this email address')
			return render(request, 'password_reset.html', {'form': PasswordResetRequestForm()})


class UserUpdateView(LoginRequiredMixin, View):
	"""
	View for changing account information in progress.
	"""

	def get(self, request):
		'''
        Gets the form for updating a user profile. User can update first name, last name, password, and topics
        '''
		user = request.user
		user_prof = UserProfile.objects.get(user=user)
		topics = user_prof.topics_preferences.all()
		already_sel = []
		for t in topics:
			already_sel.append(t)
		tag_names = Topics.objects.all()
		user_form = UpdateUserForm({
			'first_name': user.first_name,
			'last_name': user.last_name,
			'password1': user.password,
			'password2': user.password,
			'area_of_expertise': already_sel,
		})
		obj = {
			'form': user_form,
			'user_prof': user_prof,
			'already_sel': already_sel,
			'tag_names': tag_names,
		}
		return render(request, 'user_update.html', obj)

	def post(self, request):
		'''
        Performs the update of the user profile after checking the
        validity of the form.
        '''
		user_form = UpdateUserForm(request.POST)
		user_prof = UserProfile.objects.get(user=request.user)
		if user_form.is_valid():
			# Update User name, password
			user_prof.user.first_name = user_form.cleaned_data.get('first_name')
			user_prof.user.last_name = user_form.cleaned_data.get('last_name')
			if user_form.cleaned_data.get('password1'):
				user_prof.user.set_password(user_form.cleaned_data.get('password1'))
			user_prof.user.save()

			curr_topics = user_prof.topics_preferences.all()
			for each_topic in curr_topics:
				try:
					user_prof.topics_preferences.remove(each_topic)
				except ObjectDoesNotExist:
					pass
			for each_topic in user_form.cleaned_data.get('area_of_expertise'):
				user_prof.topics_preferences.add(each_topic)
			user_prof.save()
			messages.success(request, 'Your profile has been updated!')
			return HttpResponseRedirect(reverse('profile:user_update'))
		else:
			display_error(user_form, request)
			topics = user_prof.expertise_topics.all()
			already_sel = []
			for t in topics:
				already_sel.append(t)
			tag_names = Topics.objects.all()
			user_form = UpdateUserForm({
				'first_name': user_prof.user.first_name,
				'last_name': user_prof.user.last_name,
				'password': user_prof.user.password,
				'area_of_expertise': already_sel,
			})
			return render(request, 'user_update.html',
						  {
							'form': user_form,
							'user_prof': user_prof,
							'already_sel': already_sel,
							'tag_names': tag_names,
						  })


class ConfirmationView(LoginRequiredMixin, View):
	"""
	View for confirming an account after creation.
	"""
	def get(self, request):
		return render(request, 'confirmation.html', {'form': ConfirmationForm()})

	"""
	Gets the user associated with a ``Confirmation`` object by checking for a correct
	``confirmation_code`` using ``confirmation_code`` from the form

	If ``confirmation_code`` does not have a matching ``Confirmation`` object, the user is given
	the option to enter in a new code.
	"""
	def post(self, request):
		form = ConfirmationForm(request.POST)
		if form.is_valid():
			#Get confirmation code from form and check to see if correct.
			confirmation_code = form.cleaned_data['confirmation_code']
			confirmation = Confirmation.objects.get(confirmation_code=confirmation_code)
			confirmation.user_profile.confirmed = True
			confirmation.user_profile.save()
			#User confirmed, return to home.
			return HttpResponseRedirect(reverse('contribution:home'))
		#Error for incorrect code, user enters again.
		messages.error(request, 'Code is not correct, please try again.')
		return render(request, 'contribution.html', {'form': ConfirmationForm()})

class UserContributorQuestionView(LoginRequiredMixin, View):

	def get(self, request):
		return render(request, 'user_contributor_question.html')

