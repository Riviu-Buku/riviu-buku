from homepage.views import show_homepage
from django.urls import path

app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage')
]