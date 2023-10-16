from django.urls import path
from album.views import *

app_name = 'album'

urlpatterns = [
    path('', show_album, name='show_album'),
]