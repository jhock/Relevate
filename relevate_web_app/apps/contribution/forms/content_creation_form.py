from django import forms
from ..models.topic_model import Topics
from ..modules.post_util import validate_file, validate_content_creation_file
from PIL import Image
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.fields import RichTextFormField

class ContentCreateForm(forms.Form):
	"""
	Create Article Form
	"""

	# List of types of content creation for sorting in the template
	TYPE_OF_CONTENT = (
		('Infographics', 'Infographics'),
		('Blogs', 'Blogs'),
		('Videos', 'Videos'),
		('Articles and Books', 'Articles and Books'),
		('Social Media', 'Social Media'),
		('Podcasts', 'Podcasts'),
		('Interviews & Press Releases', 'Interviews & Press Releases'),
		('Community Talks & Events', 'Community Talks & Events')
	)
	# list of identifiers used to separate content creation posts by experience.
	LEVEL_OF_EXPERIENCE = (
		('Getting Started', 'Getting Started'),
		('Expanding Your Reach', 'Expanding Your Reach'),
		('Troubleshooting', 'Troubleshooting'),
		('Advanced Techniques', 'Advanced Techniques')
	)


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
	content = RichTextFormField(config_name='advanced_toolbar', max_length=10000, label='Post Content', required=False)
	blurb = forms.CharField(max_length=400, label='Short Description of Post',
						widget=forms.Textarea(attrs={'placeholder': 'Insert description Here',
													 'class': 'uk-textarea', 'rows':'5'}),  required=True)
	content_file =  forms.FileField(label='Upload Post Information in File Form (accepted: PDF, Word document)', required=False, validators=[validate_content_creation_file],
								widget=forms.FileInput(attrs={'accept': '.doc,.docx,.pdf,.mp4,.webm'}))
	references = forms.CharField(max_length=3000, label='Post References (if any)',
					widget=forms.Textarea(), required=False)
	type = forms.CharField(label='Post Category', required=True, widget=forms.Select(choices=TYPE_OF_CONTENT))
	level = forms.CharField(label='Level of Reader Experience', required=True, widget=forms.Select(choices=LEVEL_OF_EXPERIENCE))
	#True is public_scholarship, False is content_creation
	public_scholarship_or_content_creation = forms.BooleanField(required=False)

	#fields for cropping images
	x = forms.FloatField(required=True, error_messages={'required': 'Please crop the image before uploading.'})
	y = forms.FloatField(required=True, error_messages={'required': 'Please crop the image before uploading.'})
	width = forms.FloatField(required=True, error_messages={'required': 'Please crop the image before uploading.'})
	height = forms.FloatField(required=True, error_messages={'required': 'Please crop the image before uploading.'})

class CkEditorForm(forms.Form):
    content = RichTextFormField()
