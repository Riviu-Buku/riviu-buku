from django.urls import path
from album.views import *

app_name = 'album'

urlpatterns = [
    path('', show_album, name='show_album'),
    path('create_album/', create_album, name='create_album'),
]