from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from post.models import Post




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(null=True, blank=True, verbose_name='프로필사진')
    department = models.CharField(max_length=100, verbose_name='소속')
    description = models.TextField(max_length=200, null=True, verbose_name='한줄소개')
    #관심태그 추가했음
    interested_tag = models.CharField(max_length=255, null=True, blank=True, verbose_name='관심태그')

    def __str__(self):
        return str(self.user) + ' profile'


class Site(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='site')
    link = models.URLField(verbose_name='대표 URL')

    def __str__(self):
        return self.link


class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmark')
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='bookmark')

    def __str__(self):
        return self.post.title

