from django.urls import path
from upload_buku.views import *

app_name = 'upload_buku'

urlpatterns = [
    path('', show_upload, name='show_upload')
]