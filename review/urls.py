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
    path('increase-upvote/<int:item_id>/', increase_upvote_ajax, name='increase_upvote_ajax'),
    path('decrease-upvote/<int:item_id>/', decrease_upvote_ajax, name='decrease_upvote_ajax'),
    path('increase-downvote/<int:item_id>/', increase_downvote_ajax, name='increase_downvote_ajax'),
    path('decrease-downvote/<int:item_id>/', decrease_downvote_ajax, name='decrease_downvote_ajax'),
    path('delete-review/<int:item_id>/', delete_review, name='delete_review'),
    
]