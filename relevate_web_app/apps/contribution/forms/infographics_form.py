from django import forms
from ..models.topic_model import Topics
from ..modules.post_util import validate_file


class ArticleInfographicsCreate(forms.Form):
	"""
	Create Article Infograhics Form
	"""
	title = forms.CharField(label='Title', max_length=1000, required=True,
							widget=forms.TextInput(attrs={'placeholder': 'Title', 'class':'uk-input uk-width-1-1'}))
	topic_choices = forms.ModelMultipleChoiceField(label="Tag appropiate choices", queryset=Topics.objects.all(),
		 widget=forms.CheckboxSelectMultiple(attrs={'type':'hidden', 'id':'selected_item'}),
                                required=False)
	contents = forms.FileField(label='Upload Infographics', required=True, validators=[validate_file],
								widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}))
	blurb = forms.CharField(label="Short Description of Infographic", max_length=150, required=True,
								widget=forms.Textarea())
	#fields for cropping images
	x = forms.FloatField(required=False)
	y = forms.FloatField(required=False)
	width = forms.FloatField(required=False)
	height = forms.FloatField(required=False)

class ArticleInfographicUpdateForm(forms.Form):
	title = forms.CharField(label='Title', max_length=1000, required=True,
							widget=forms.TextInput(attrs={'placeholder': 'Title', 'class':'uk-input uk-form-width-large'}))
	topic_choices = forms.ModelMultipleChoiceField(label="Tag appropiate choices", queryset=Topics.objects.all(),
		 widget=forms.CheckboxSelectMultiple(attrs={'type':'hidden', 'id':'selected_item', "class":"ui fluid dropdown"}),
                                required=False)
	contents = forms.FileField(label='Upload Infographics', required=False, validators=[validate_file],
								widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}))
	blurb = forms.CharField(label="Short Description of Infographic", max_length=150, required=True,
								widget=forms.Textarea())
	is_published = forms.BooleanField(label="Publish Article", required=False,
								widget=forms.CheckboxInput(attrs={'class': 'uk-checkbox'}))
	#fields for cropping images
	x = forms.FloatField(required=False)
	y = forms.FloatField(required=False)
	width = forms.FloatField(required=False)
	height = forms.FloatField(required=False)

