from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns = [
    # path('', show_review, name='show_review'),
    path('<int:id>/', show_review, name='show_review'),
    path('write-review/', write_review, name='write_review'),
    path('create-review-ajax/<int:id>/', add_review_ajax, name='add_review_ajax'),
    path('get-review/<int:id>/', get_review_json, name='get_review_json'),
    path('get-review-user/<int:id>/', get_review_by_user_json, name='get_review_by_user_json'),
]