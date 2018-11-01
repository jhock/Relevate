from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField
from ...profiles.models import User
from django.contrib.auth import authenticate
from ...contribution.models import Topics

class UpdateUserForm(forms.Form):
	"""
	Allows user to update their name and email, checks for all other emails besides their own.
	"""
	first_name = forms.CharField(label='First Name', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'uk-input'}))
	last_name = forms.CharField(label='Last Name', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'uk-input'}))
	email = forms.EmailField(label='Email', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'uk-input'}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'uk-input'}),
							   required=False)
	password2 = forms.CharField(label='Verify Password', widget=forms.PasswordInput(attrs={'class':'uk-input'}), required=False)
	area_of_expertise = forms.ModelMultipleChoiceField(label="Area of Expertise Relevant to Romantic Relationships",
								queryset=Topics.objects.all(),
								widget=forms.CheckboxSelectMultiple(attrs={'class': 'expertise-checkbox'}), required=False)

	#TODO: make a clean_mail to check for any other email besides their own.

	def clean(self):
		"""
		Verifies that the values entered into the password fields match
		NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
		"""
		cleaned_data = super(UpdateUserForm, self).clean()
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
		self.cleaned_data['first_name'] = self.cleaned_data['first_name'].capitalize()
		self.cleaned_data['last_name'] = self.cleaned_data['last_name'].capitalize()
		return self.cleaned_data

class RegistrationForm(forms.Form):

	"""
	Registration form, allows users to create accounts.
	"""
	first_name = forms.CharField(label='First Name', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your first Name'}))
	last_name = forms.CharField(label='Last Name', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your last Name'}))
	email = forms.EmailField(label='Email', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter a strong password'}),
							   required=True)
	password2 = forms.CharField(label='Verify Password', widget=forms.PasswordInput(attrs={'placeholder': "Re-enter the password"}), required=True)
	area_of_expertise = forms.ModelMultipleChoiceField(label="Area of Expertise Relevant to Romantic Relationships",
								queryset=Topics.objects.all(),
								widget=forms.CheckboxSelectMultiple(attrs={'class': 'expertise-checkbox'}), required=False)

	def clean_email(self):
		cleaned_data = super(RegistrationForm, self).clean()
		email = self.cleaned_data['email']
		try:
			email_value = User.objects.get(email=email)
			msg = "Sorry, this email is already in use."
			print("email already in use")
			self.add_error('email', msg)
		except User.DoesNotExist:
			return email

	def clean(self):
		"""
		Verifies that the values entered into the password fields match
		NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
		"""
		cleaned_data = super(RegistrationForm, self).clean()
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
		self.cleaned_data['first_name'] = self.cleaned_data['first_name'].capitalize()
		self.cleaned_data['last_name'] = self.cleaned_data['last_name'].capitalize()
		return self.cleaned_data


class LoginForm(forms.Form):
	my_default_errors = {
		'invalid': 'Make sure email and password are correct'
	}
	username = forms.CharField(label='Username', max_length=100, required=True,
			widget=forms.TextInput(attrs={'class': 'uk-input uk-form-width-large'}),)
	password = forms.CharField(label='Password', error_messages=my_default_errors,
			widget=forms.PasswordInput(attrs={'class': 'uk-input uk-form-width-large'}))

	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']


class PasswordChangeForm(forms.Form):
	password = forms.CharField(label='New Password', 
								widget=forms.PasswordInput(attrs={'class': 'uk-input'}),
								required=True)
	verify_password = forms.CharField(label='Verify New Password', 
								widget=forms.PasswordInput(attrs={'class': 'uk-input'}), 
								required=True)

	def clean(self):
		cleaned_data = super(PasswordChangeForm, self).clean()
		user_password = self.cleaned_data.get('password')
		user_verify_password = self.cleaned_data.get('verify_password')

		if user_password and user_verify_password:
			if user_password != user_verify_password:
				msg = "Passwords does not match"
				self.add_error('password', msg)
		return cleaned_data

class SetPasswordForm(forms.Form):
	"""
	A form that lets a user change set their password without entering the old
	password
	"""
	error_messages = {
		'password_mismatch': ("The two password fields didn't match."),
		}
	new_password1 = forms.CharField(label=("New password"),
									widget=forms.PasswordInput)
	new_password2 = forms.CharField(label=("New password confirmation"),
									widget=forms.PasswordInput)

	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 and password2:
			if password1 != password2:
				raise forms.ValidationError(
					self.error_messages['password_mismatch'],
					code='password_mismatch',
					)
		return password2

class PasswordResetRequestForm(forms.Form):
	email = forms.CharField(label=("Email"), max_length=254)

#TO Do: resend confirmation code if forgotten
class ConfirmationForm(forms.Form):
	confirmation_code = forms.CharField(label='Confirmation Code', required=True, widget=forms.TextInput(attrs={'placeholder': 'Confirmation Code'}))


