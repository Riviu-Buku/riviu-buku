from django.urls import path
from homepage.views import *

app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage'),
    path('get_books', get_books, name='get_books')
]