from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    reply = models.IntegerField(null=True, blank=True)
    upvote = models.IntegerField(null=True, blank=True)
    downvote = models.IntegerField(null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)