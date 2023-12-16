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

    def save(self, *args, **kwargs):
        # Check if upvote or downvote is None, and set them to 0
        if self.upvote is None:
            self.upvote = 0
        if self.downvote is None:
            self.downvote = 0

        super(Review, self).save(*args, **kwargs)

class ReviewCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    checkedUpvote = models.BooleanField(default=False, unique=True)
    checkedDownvote = models.BooleanField(default=False, unique=True)

    def save(self, *args, **kwargs):
        # Ensure that only one ReviewCheck object exists for each user and review combination
        self.__class__.objects.filter(user=self.user, review=self.review).exclude(pk=self.pk).delete()
        super(ReviewCheck, self).save(*args, **kwargs)