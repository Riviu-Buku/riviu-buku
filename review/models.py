from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    reply = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    description = models.TextField()