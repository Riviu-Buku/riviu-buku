from django.urls import path
from homepage.views import *

app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage'),
    path('get_books', get_books, name='get_books'),
    path('get_books_by_id/<int:id>/', get_books_by_id, name='get_books_by_id'),
    path('create-fav-book-ajax/', add_book_ajax, name='add_book_ajax'),
]