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

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.name)
            unique_slug = original_slug
            num = 1
            while Album.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(original_slug, num)
                num += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)