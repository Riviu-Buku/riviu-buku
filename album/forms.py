from django import forms
from .models import Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'description']  # add other fields if needed

class SimpleForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)