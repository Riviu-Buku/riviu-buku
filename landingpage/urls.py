from landingpage.views import show_landingpage
from django.urls import path

app_name = 'landingpage'

urlpatterns = [
    path('', show_landingpage, name='show_landingpage')
]