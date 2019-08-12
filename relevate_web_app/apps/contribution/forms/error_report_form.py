from django import forms
from ..modules.post_util import validate_file

class ErrorReportForm(forms.Form):
    Description = forms.CharField(label='Funder Name', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Funder or Adviser Name'}))
    name = forms.CharField(label='Funder Name', max_length=200, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Funder or Adviser Name'}))
    image = forms.ImageField(label="Upload a screenshot of the error.", required=False, validators=[validate_file],
                             widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}))