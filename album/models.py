from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from homepage.models import Book

# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    description = models.CharField(max_length=256)
    cover_image = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Save the album first to generate an id
        super().save(*args, **kwargs)

        # Then check if there are any books in the album
        if self.books.exists():
            # If there are books, set the cover image to the cover image of the first book
            self.cover_image = self.books.first().coverImg
            # Save the album again to update the cover image
            super().save(*args, **kwargs)