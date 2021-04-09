from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



class User(AbstractUser):
    pass



class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers')




class Post(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length= 300)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default = 0) # number of likes start at 0
