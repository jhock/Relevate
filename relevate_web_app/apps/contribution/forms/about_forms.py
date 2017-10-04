from django import forms
from ..modules.post_util import validate_file

class AboutFunderForm(forms.Form):
    CHOICES = [('funder', 'funder'),
               ('adviser', 'adviser'),
               ('architect', 'architect'),
               ('engineer', 'engineer')]

    name = forms.CharField(label='Funder Name', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Funder or Adviser Name'}))
    content = forms.CharField(max_length=1500, widget=forms.Textarea(attrs={'placeholder': 'Enter Funder or Adviser Description.',
											'style': 'font-size: 16px; width: 100%;'}))
    image = forms.ImageField(label="Upload a picture for the Funder or Adviser", required=False, validators=[validate_file],
                             widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}))
    #Field to determine if person is a funder or advisor
    funder_or_adviser = forms.ChoiceField(label='Select if person is a Funder or Adviser',widget=forms.RadioSelect(), required=True, choices=CHOICES)

    #Fields used in image cropping
    x = forms.FloatField(required=False)
    y = forms.FloatField(required=False)
    width = forms.FloatField(required=False)
    height = forms.FloatField(required=False)