from django import forms
from ..models.topic_model import Topics
from ..modules.post_util import validate_file, validate_content_creation_file
from PIL import Image
from ..models.content_creation_model import TYPE_OF_CONTENT, LEVEL_OF_EXPERIENCE


class ContentCreateForm(forms.Form):
	"""
	Create Article Form
	"""
	image = forms.ImageField(label="Upload a picture for your post", required=True , validators=[validate_file],
								widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}))
	title = forms.CharField(label='Title', max_length=1000, required=True, widget=forms.TextInput(
																	attrs=
																	{
																		'placeholder': 'Title',
																		'class': 'uk-input uk-form-width-large'
																	}
																)
						)
	content = forms.CharField(max_length=10000, label='Post Content',
					widget=forms.Textarea(attrs={'placeholder': 'Insert Article Here',
											'class': 'form-control'}),  required=False)
	blurb = forms.CharField(max_length=400, label='Short Description of Post',
						widget=forms.Textarea(attrs={'placeholder': 'Insert description Here',
													 'class': 'uk-textarea', 'rows':'5'}),  required=True)
	content_file =  forms.FileField(label='Upload Post Information in File Form (accepted: PDF, Word document)', required=False, validators=[validate_content_creation_file],
								widget=forms.FileInput(attrs={'accept': '.doc,.docx,.pdf,.mp4,.webm'}))
	references = forms.CharField(max_length=3000, label='Post References (if any)',
					widget=forms.Textarea(), required=False)
	type = forms.CharField(label='Post Category', required=True, widget=forms.Select(choices=TYPE_OF_CONTENT))
	level = forms.CharField(label='Level of Reader Experience', required=True, widget=forms.Select(choices=LEVEL_OF_EXPERIENCE))

	#fields for cropping images
	x = forms.FloatField(required=True, error_messages={'required': 'Please crop the image before uploading.'})
	y = forms.FloatField(required=True, error_messages={'required': 'Please crop the image before uploading.'})
	width = forms.FloatField(required=True, error_messages={'required': 'Please crop the image before uploading.'})
	height = forms.FloatField(required=True, error_messages={'required': 'Please crop the image before uploading.'})