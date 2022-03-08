from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Blog(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=32, null=True)
    title = models.CharField(max_length=32, unique=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
