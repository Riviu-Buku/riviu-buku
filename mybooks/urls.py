from django.urls import path
from mybooks.views import *

app_name = 'mybooks'
urlpatterns = [
    path('', show_main, name='show_main'),
    path('get_books', get_books, name='get_books'),
]
