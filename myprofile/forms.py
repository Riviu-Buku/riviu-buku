from django.forms import ModelForm
from myprofile.models import ProfileUser
from django import forms

class ProfileForm(ModelForm):
    AVATAR_CHOICES = (
        ('avatar-default.jpeg', 'Default'),
        ('avatar1.jpeg', 'Avatar 1'),
        ('avatar2.jpeg', 'Avatar 2'),
        ('avatar3.jpeg', 'Avatar 3'),
        ('avatar4.jpeg', 'Avatar 4'),
        ('avatar5.jpeg', 'Avatar 5'),
        ('avatar6.jpeg', 'Avatar 6'),
        ('avatar7.jpeg', 'Avatar 7'),
    )
    avatar = forms.ChoiceField(choices=AVATAR_CHOICES, required=False)
    class Meta:
        model = ProfileUser
        fields = ["name", "avatar", "email", "handphone", "bio", "address"]

class UpdateProfileForm(ModelForm):
    class Meta:
        model = ProfileUser
        fields = ["name", "avatar", "email", "handphone", "bio", "address"]
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)