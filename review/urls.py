from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns = [
    # path('', show_review, name='show_review'),
    path('<int:id>/', show_review, name='show_review'),
    path('write-review/', write_review, name='write_review')
]