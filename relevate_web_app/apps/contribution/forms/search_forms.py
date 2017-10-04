from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Search for Post'}))