from django.conf import settings
from django.db.models.signals import post_save
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(null=True, verbose_name='프로필사진')
    department = models.CharField(max_length=100, verbose_name='소속')
    description = models.TextField(max_length=200, null=True, verbose_name='한줄소개')

    # site = # NULL=True
    def __str__(self):
        return str(self.user) + ' profile'


class Site(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='site')
    link = models.URLField(verbose_name='대표 URL')

    def __str__(self):
        return self.link


# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True)
#     website_url = models.URLField(blank=True)

def on_post_save_for_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user)


post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)
