from django import forms
from ..models.topic_model import Topics
from ..modules.post_util import validate_file
from PIL import Image


class ArticleCreateForm(forms.Form):
	"""
	Create Article Form
	"""
	title = forms.CharField(label='Title', max_length=1000, required=True, widget=forms.TextInput(
																	attrs=
																	{
																		'placeholder': 'Title',
																		'class': 'uk-input uk-form-width-large'
																	}
																)
						)
	image = forms.ImageField(label="Upload a picture for your article", required=False , validators=[validate_file],
								widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}))
	url_image = forms.CharField(max_length=1000, label='Image From Url',
					widget=forms.TextInput(attrs={'placeholder': 'Paste the Url of the image here',
											'class': 'form-control'}),  required=False)
	content = forms.CharField(max_length=10000, label='Article Content',
					widget=forms.Textarea(attrs={'placeholder': 'Insert Article Here',
											'class': 'form-control'}),  required=True)
	blurb = forms.CharField(max_length=3000, label='Short Description of Article',
						widget=forms.Textarea(attrs={'placeholder': 'Insert Article Here',
													 'class': 'uk-textarea', 'rows':'5'}),  required=True)
	references = forms.CharField(max_length=3000, label='Article References (if any)',
					widget=forms.Textarea(), required=False)
	topic_choices = forms.ModelMultipleChoiceField(label="Tag appropiate choices", queryset=Topics.objects.all(),
		 widget=forms.CheckboxSelectMultiple(attrs={'id':'selected_item', "class":"ui fluid dropdown"}),
                                required=True)

	#fields for cropping images
	x = forms.FloatField(required=False)
	y = forms.FloatField(required=False)
	width = forms.FloatField(required=False)
	height = forms.FloatField(required=False)

	def clean(self):
		cleaned_data = super(ArticleCreateForm, self).clean()
		image = cleaned_data.get("image")
		url_image = cleaned_data.get("url_image")

		if image and url_image:
			# Only do something if both fields are valid so far.
			raise forms.ValidationError(
				"Enter information for either an image or an image Url, not both."
			)
		if not image and not url_image:
			raise  forms.ValidationError(
				"Enter information for either an image upload or an image url."
			)




class ArticleUpdateForm(forms.Form):
	title = forms.CharField(label='Title', max_length=1000, required=True,
			widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'uk-input uk-form-width-large'}))
	image = forms.FileField(label='Upload Infographics', required=False, validators=[validate_file],
								widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}))
	content = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'placeholder': 'Insert Article Here',
											'class': 'form-control'}), required=True)
	topic_choices = forms.ModelMultipleChoiceField(label="Tag appropiate choices",  queryset=Topics.objects.all(),
		 widget=forms.CheckboxSelectMultiple(attrs={'type':'hidden', 'id':'selected_item', "class":"ui fluid dropdown"}),
                                required=True)
	blurb = forms.CharField(max_length=150, label='Short Description of Article',
							widget=forms.Textarea(attrs={'placeholder': 'Insert Article Here',
													'class': 'uk-textarea', 'rows':'5'}),  required=True)
	references = forms.CharField(max_length=3000, label='Article References (if any)',
					widget=forms.Textarea(), required=False)
	is_published = forms.BooleanField(label="Publish Article", required=False)
	#fields for cropping images
	x = forms.FloatField(required=False)
	y = forms.FloatField(required=False)
	width = forms.FloatField(required=False)
	height = forms.FloatField(required=False)





