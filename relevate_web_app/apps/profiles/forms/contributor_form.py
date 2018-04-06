from django import forms
from django.template import Context
from ..modules.contributor_util import get_states, get_countries
from ..models.adviser_model import Adviser
from ...contribution.models.topic_model import Topics
from ..models.contributor_model import Degree
from ...components.templatetags.select_tags import Select

import pdb

class AdviserModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s (%s)" % (obj.__str__(), obj.contributor_profile.user_profile.user.username)
	def validate(self, val):
		pass

class SelectWidget(forms.TextInput):
    def __init__(self, options, label, placeholder, editable='True', default_value="", *args, **kwargs):
        super(SelectWidget, self).__init__(*args, **kwargs)
        self.options = options
        self.label = label
        self.placeholder = placeholder
        self.editable = editable
        self.default_value = default_value

    def render(self, name, value, attrs=None):
    		text_html = super(SelectWidget, self).render(name, value, attrs=attrs)
    		props = ['placeholder="' + self.placeholder + '"', 'value="' + self.default_value + '"']

    		return Select(None, self.label, None, text_html, props, self.options, self.editable).render(Context())

class ContributorForm(forms.Form):
	# Changed to false to prevent update page from throwing a fit
	cv = forms.FileField(
		label='Upload your CV (PDF)', 
		required=False, 
		widget=forms.FileInput(attrs={'accept': '.pdf'})
	)
	
	adviser = AdviserModelChoiceField(
		label="Select Your Adviser", 
		queryset=Adviser.objects.filter(is_available=True), 
		widget=forms.Select(attrs={'class': 'uk-select'}), 
		empty_label="No Mentor"
	)

	address = forms.CharField(
		label="Professional Address", 
		widget=forms.TextInput(attrs={'placeholder': 'Enter your address'}),
		required=True
	)

	city = forms.CharField(
		label="City", 
		widget=forms.TextInput(attrs={'placeholder': 'Enter your city'}),
		required=True
	)

	state = forms.CharField(widget=SelectWidget(
		options=[state[0] for state in get_states()], 
		label='State', 
		placeholder='Choose your state'
	))

	country = forms.CharField(widget=SelectWidget(
		options=[country[1] for country in get_countries()], 
		label='Country', 
		default_value='United States',
		placeholder='Choose your country'
	))

	zipcode = forms.CharField(
		label="Zip Code", 
		max_length=5,
		widget=forms.TextInput(attrs={'placeholder': 'Zip Code'}), 
		required=True
	)
	
	# @US_TODO: Turn this into a choices field for recommendation system etc
	program = forms.CharField(
		label="Program", 
		required=False,
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Ex. Psychology',
			}
		)
	)

	institution = forms.CharField(
		label="Institution",
		required=False,
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Ex. Kansas State'
			}
		)
	)

	website_url = forms.URLField(
		label="Website", 
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Website URL'
			}
		), 
		required=False
	)

	biography = forms.CharField(
		max_length=2999, 
		widget=forms.Textarea(
			attrs={
				'placeholder': 'Write a brief biography about yourself.',
				'style': 'font-size: 16px; width: 100%; overflow:scroll;resize:none;'
			}
		)
	)

	degree = forms.CharField(widget=SelectWidget(
			options=[degree for degree in Degree.objects.all().values_list('name', flat=True)], 
			label='Level of Study', 
			placeholder='Enter your level of study'
	))

	area_of_expertise = forms.ModelMultipleChoiceField(
		label="Area of Expertise Relevant to Romantic Relationships", 
		queryset=Topics.objects.all(),
		widget=forms.CheckboxSelectMultiple(),
		required=True
	)

	interests = forms.CharField(
		label="Professional Interests, Experience, and Expertise",  
		widget=forms.Textarea(
			attrs={
				'style':'overflow:scroll;resize:none;'
			}
		), 
		required=False
	)

	# Changed to false to prevent update page from throwing a fit
	avatar = forms.ImageField(
		label="Upload your profile picture", 
		required=False,
		widget=forms.FileInput(
			attrs={
				'accept': '.png,.jpg,.jpeg'
			}
		)
	)

	accept_terms = forms.BooleanField(
		widget=forms.CheckboxInput(attrs={'class': 'uk-checkbox'})
	)

	certification = forms.CharField(
		label="Certifications",
		required=False,
		widget=forms.TextInput(attrs={'placeholder': 'Enter a certification'})
	)

	organizational_affiliation = forms.CharField()


	# widget = forms.TextInput(attrs={'placeholder': 'Organizational Affiliation ex:NCFR',
	# 								'class': 'uk-search-field uk-input uk-form-width-large'})

	#fields for cropping images
	x = forms.FloatField(required=False)
	y = forms.FloatField(required=False)
	width = forms.FloatField(required=False)
	height = forms.FloatField(required=False)

	def __init__(self, *args, **kwargs):
		_organization_list = kwargs.pop('data_list', None)
		super(ContributorForm, self).__init__(*args, **kwargs)

		self.fields['organizational_affiliation'].widget = SelectWidget(
			options=[org for org in _organization_list], 
			label='Organizational Affiliations', 
			placeholder='Ex. NCFR'
		)