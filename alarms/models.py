from django.contrib.auth.models import User
from django.db import models


class Alarm(models.Model):
    receiver = models.ForeignKey(User, max_length=50, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
