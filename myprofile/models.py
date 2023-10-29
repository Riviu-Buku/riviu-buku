from django.db import models
from django.contrib.auth.models import User

class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    avatar = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    handphone = models.CharField(max_length=15) 
    bio = models.CharField(max_length=20)  
    address = models.CharField(max_length=255)
