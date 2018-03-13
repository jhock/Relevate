from django import forms
from django.template import Context
from ..modules.contributor_util import get_states, get_countries
from ..models.adviser_model import Adviser
from ...contribution.models.topic_model import Topics
from ..models.contributor_model import Degree
from ...components.templatetags.select_tags import Select

class AdviserModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s (%s)" % (obj.__str__(), obj.contributor_profile.user_profile.user.username)
	def validate(self, val):
		pass

class SelectWidget(forms.TextInput):
    def __init__(self, options, label, placeholder, *args, **kwargs):
        super(SelectWidget, self).__init__(*args, **kwargs)
        self.options = options
        self.label = label
        self.placeholder = placeholder

    def render(self, name, value, attrs=None):
        text_html = super(SelectWidget, self).render(name, value, attrs=attrs)
        placeholder_prop = 'placeholder="' + self.placeholder + '"'
        return Select(None, self.label, None, text_html, [placeholder_prop], self.options).render(Context())


class ContributorForm(forms.Form):
	# Changed to false to prevent update page from throwing a fit
	cv = forms.FileField(
		label='Upload CV (must be a .pdf)', 
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
		widget=forms.TextInput(attrs={'class': 'uk-input'}),
		required=True
	)

	city = forms.CharField(
		label="City", 
		widget=forms.TextInput(attrs={'class': 'uk-input'}),
		required=True
	)

	state = forms.ChoiceField(
		label="State", 
		choices=get_states(), 
		widget=forms.Select(attrs={'class': 'uk-select'}),
		required=True
	)

	country = forms.ChoiceField(
		label="Country", 
		choices=get_countries(), 
		widget=forms.Select(attrs={'class': 'uk-select'}),
		required=True
	)

	zipcode = forms.CharField(
		label="Zip Code", 
		max_length=5, 
		widget=forms.TextInput(attrs={'class': 'uk-input'}), 
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
				'placeholder': 'Website URL',
				'class': 'uk-input uk-form-width-large'
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
		widget=forms.CheckboxSelectMultiple(
			attrs={
				'class': 'expertise-checkbox'
			}
		), 
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