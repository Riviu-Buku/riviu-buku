from django.urls import path
from upload_buku.views import *

app_name = 'upload_buku'

urlpatterns = [
    path('', upload_buku, name='upload_buku'),
    path('create-flutter/', create_book_flutter, name='create_book_flutter')
]