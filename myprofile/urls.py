from django.urls import path
from myprofile.views import *

app_name = 'myprofile'

urlpatterns = [
    path('', show_profile, name='show_profile'),
]