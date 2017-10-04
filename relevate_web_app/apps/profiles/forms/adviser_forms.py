from django import forms

class AdviserCreateForm(forms.Form):
	
	number_of_advisees = forms.IntegerField(label="Number of Mentees", widget=forms.TextInput(attrs={'class': 'uk-input'}), required=True)
	reason = forms.CharField(label="Reason For Being a Mentor", 
							widget=forms.Textarea(attrs={'placeholder': 'Why do you want to be a mentor?',
											'class': 'uk-input', 'style':'overflow:scroll;resize:none;'}), required=True)
	accept_terms = forms.BooleanField(label="Terms and Conditions", widget=forms.CheckboxInput(attrs={'class': 'uk-checkbox'}), required=True)