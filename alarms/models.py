from django.db import models


class Alarm(models.Model):
    message = models.CharField(max_length=100)
