from django.urls import path
from album.views import *

app_name = 'album'

urlpatterns = [
    path('', show_albums, name='show_albums'),
    path('create-album/', create_album, name='create_album'),
    path('search-books/', search_books, name='search_books'),
    path('albums/<slug:slug>/', show_album, name='show_album')
]