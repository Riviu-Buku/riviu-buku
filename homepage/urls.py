from django.urls import path
from homepage.views import *

app_name = 'homepage'

urlpatterns = [
    path('', show_homepage, name='show_homepage'),
    path('get_books', get_books, name='get_books'),
    path('get_books_by_id/<int:id>/', get_books_by_id, name='get_books_by_id'),
    path('create-fav-book-ajax/', add_book_ajax, name='add_book_ajax'),
    path('xml/', show_xml, name='show_xml'), 
    path('json/', show_json, name='show_json'), 
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'), 
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
]