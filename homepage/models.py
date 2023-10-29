from django.db import models
from django.contrib.auth.models import User
from review.models import Review

# Create your models here.

class Book(models.Model):
    title = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)

    language = models.CharField(max_length=100, null=True, blank=True)
    genres = models.JSONField(null=True, blank=True)
    characters = models.JSONField(null=True, blank=True)
    edition = models.CharField(max_length=100, null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)

    publisher = models.CharField(max_length=100, null=True, blank=True)
    awards = models.JSONField(null=True, blank=True)
    numRatings = models.IntegerField(null=True, blank=True)
    numLikes = models.IntegerField(null=True, blank=True)
    coverImg = models.URLField(null=True, blank=True)
    review = models.ManyToManyField(Review)

    liked_by_users = models.ManyToManyField(User, related_name="liked_books", blank=True)
    
    def __str__(self):
        return self.title
    
class FavoriteBook(models.Model):
    title = models.TextField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title