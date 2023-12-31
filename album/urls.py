from django.urls import path
from album.views import *

app_name = 'album'

urlpatterns = [
    path('', show_albums, name='show_albums'),
    path('create-album/', create_album, name='create_album'),
    path('search-books/', search_books, name='search_books'),
    path('albums/<slug:slug>/', show_album, name='show_album'),
    path('edit-album/<slug:slug>/', edit_album, name='edit_album'),
    path('album/<slug:slug>/remove-book/', remove_book_from_album, name='remove_book_from_album'),
    path('delete-album/<slug:slug>/', delete_album, name='delete_album'),
    path('search-albums/', search_albums, name='search_album'),
    path('json/', get_album_json, name='get_album_json'),
    path('create-album-flutter/', create_album_flutter, name='create_album_flutter'),
    path('edit-album-flutter/<slug:slug>/', edit_album_flutter, name='edit_album_flutter'),
    path('delete-album-flutter/<slug:slug>/', delete_album_flutter, name='delete_album_flutter'),
]