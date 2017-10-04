from django import forms
from ..models.topic_model import Topics
from ..modules.post_util import validate_file

class LinkCreateForm(forms.Form):

	title = forms.CharField(label='Title', max_length=100, required=True, widget=forms.TextInput(
								attrs={'placeholder': 'Title','class':'uk-input uk-form-width-large'}))
	link = forms.CharField(label='Link', max_length=200, required=True, widget=forms.TextInput(
								attrs={'placeholder': 'Link','class':'uk-input uk-form-width-large'}))
	blurb = forms.CharField(label='Short Description of Link', max_length=400, required=True, widget=forms.Textarea(
								attrs={'class': 'uk-textarea uk-form-width-large'}))
	image = forms.ImageField(label="Upload an Image", required=True , validators=[validate_file],
								widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}))

	topic_choices = forms.ModelMultipleChoiceField(label="Topics:", queryset= Topics.objects.all(),
			widget=forms.CheckboxSelectMultiple(), required=True)
	#fields for cropping images
	x = forms.FloatField(required=True)
	y = forms.FloatField(required=False)
	width = forms.FloatField(required=False)
	height = forms.FloatField(required=False)

class LinkUpdateForm(forms.Form):

	title = forms.CharField(label='Title', max_length=100, required=True, widget=forms.TextInput(
								attrs=
									{
										'placeholder': 'Title',
										'class':'uk-input uk-form-width-large'
									}
								)
							)
	link = forms.CharField(label='Link', max_length=200, required=True, widget=forms.TextInput(
								attrs=
									{
										'placeholder': 'Link',
										'class':'uk-input uk-form-width-large'
									}
								)
							)
	blurb = forms.CharField(label='Short Description of Link', max_length=400, required=True, widget=forms.Textarea(
								attrs=
									{
										'class': 'uk-textarea uk-form-width-large'
									}
								)
							)
	image = forms.ImageField(label="Upload an Image", required=False , validators=[validate_file],
								widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}))

	topic_choices = forms.ModelMultipleChoiceField(label="Topics:", queryset= Topics.objects.all(),
			widget=forms.CheckboxSelectMultiple(), required=True)
	#fields for cropping images
	x = forms.FloatField(required=False)
	y = forms.FloatField(required=False)
	width = forms.FloatField(required=False)
	height = forms.FloatField(required=False)
