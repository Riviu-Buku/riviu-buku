from django.db import models
from django.contrib.auth.models import User

class ProfileUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    avatar = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    handphone = models.CharField(max_length=15, blank=True) 
    bio = models.CharField(max_length=20, blank=True)  
    address = models.CharField(max_length=255, blank=True)

    def to_dict(self):
        return {
            'user_id': self.user.id,
            'username': self.user.username,
            'name': self.name,
            'avatar': self.avatar,
            'email': self.email,
            'handphone': self.handphone,
            'bio': self.bio,
            'address': self.address,
        }