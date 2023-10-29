from django.urls import path
from myprofile.views import *

app_name = 'myprofile'

urlpatterns = [
    path('', show_profile, name='show_profile'),
    path('complete/', complete_profile, name='complete_profile'),
    path('edit/', update_profile, name='update_profile'),
    path('update-bio/', update_bio, name='update_bio'),
    path('toggle-unlike-book/<int:book_id>/', toggle_unlike_book, name='toggle_unlike_book'),
]