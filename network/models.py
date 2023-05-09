from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime

class User(AbstractUser):
    follower_users = models.ManyToManyField("self",blank=True, symmetrical= False, related_name="follower")
    following_users = models.ManyToManyField("self",blank=True, symmetrical= False, related_name="following")

    def __str__(self):
        return f"{self.username}"
    


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="creator")
    content = models.CharField(max_length=128, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    
    def __str__(self):
        return f"{self.creator}: {self.content}"
    
    
