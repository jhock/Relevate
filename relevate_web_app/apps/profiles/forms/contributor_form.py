from django import forms
from ..modules.contributor_util import get_states, get_countries
from ..models.adviser_model import Adviser
from ...contribution.models.topic_model import Topics
from ..models.contributor_model import Degree


class AdviserModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s (%s)" % (obj.__str__(), obj.contributor_profile.user_profile.user.username)
	def validate(self, val):
		pass

class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs ={'placeholder': 'Organizational Affiliation ex:NCFR','class': 'uk-search-field uk-input uk-form-width-large'}
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)

class ContributorForm(forms.Form):
	# Changed to false to prevent update page from throwing a fit
	cv = forms.FileField(label='Upload CV (must be a .pdf)', required=False, 
							widget=forms.FileInput(attrs={'accept': '.pdf'}))
	adviser = AdviserModelChoiceField(label="Select Your Adviser", queryset=Adviser.objects.filter(is_available=True), 
							widget=forms.Select(attrs={'class': 'uk-select'}), empty_label="No Mentor")
	address = forms.CharField(label="Professional Address", widget=forms.TextInput(attrs={'class': 'uk-input'}),
								required=True)
	city = forms.CharField(label="City", widget=forms.TextInput(attrs={'class': 'uk-input'}), required=True)
	state = forms.ChoiceField(label="State", choices=get_states(), widget=forms.Select(attrs={'class': 'uk-select'}),
								required=True)
	country = forms.ChoiceField(label="Country", choices=get_countries(), widget=forms.Select(attrs={'class': 'uk-select'}),
							  required=True)
	zipcode = forms.CharField(label="Zip Code", max_length=5, widget=forms.TextInput(attrs={'class': 'uk-input'}), required=True)
	# @US_TODO: Turn this into a choices field for recommendation system etc
	program = forms.CharField(label="Program", required=False,
							widget=forms.TextInput(attrs={'placeholder': 'Field of study/specialization', 
								'class': 'uk-input uk-form-width-medium'}))
	institution = forms.CharField(label="Institution",required=False,
								  widget=forms.TextInput(attrs={'placeholder': 'Institution ex:Kansas State University',
												'class': 'uk-search-field uk-input uk-form-width-large'}))
	website_url = forms.URLField(label="Website", widget=forms.TextInput(attrs={'placeholder': 'Website URL', 

												'class': 'uk-input uk-form-width-large'}), required=False)
	biography = forms.CharField(max_length=2999, widget=forms.Textarea(attrs={'placeholder': 'Write a brief biography about yourself.',
											'style': 'font-size: 16px; width: 100%; overflow:scroll;resize:none;'}))

	degree = forms.ModelChoiceField(label="Level of Study", queryset=Degree.objects.all(), 
								widget=forms.Select(attrs={'class': 'uk-select uk-form-width-medium'}), empty_label=None, required=False)
	area_of_expertise = forms.ModelMultipleChoiceField(label="Area of Expertise Relevant to Romantic Relationships", 
								queryset=Topics.objects.all(), 
								widget=forms.CheckboxSelectMultiple(attrs={'class': 'expertise-checkbox'}), required=True)
	interests = forms.CharField(label="Professional Interests, Experience, and Expertise",  widget=forms.Textarea(attrs={'style':'overflow:scroll;resize:none;'}), required=False)
	# Changed to false to prevent update page from throwing a fit
	avatar = forms.ImageField(label="Upload your profile picture", required=False,
							widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}))
	accept_terms = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'uk-checkbox'}))

	certification = forms.CharField(label="Certifications",required=False,
									  widget=forms.TextInput(attrs={'placeholder': 'Enter a certification',
													'class': 'uk-search-field uk-input uk-form-width-large'}))

	organizational_affiliation = forms.CharField(label="Organizational Affiliations", required=False)

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

		# the "name" parameter will allow you to use the same widget more than once in the same
		# form, not setting this parameter differently will cuse all inputs display the
		# same list.
		self.fields['organizational_affiliation'].widget = ListTextWidget(data_list=_organization_list, name='organization-list')