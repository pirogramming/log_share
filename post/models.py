from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='post')
    categories = (
        ('대외활동', '대외활동'),
        ('동아리', '동아리'),
        ('공모전', '공모전'),
        ('스터디', '스터디'),
        ('인턴', '인턴'),
        ('강연', '강연'),
        ('자격증', '자격증'),
        ('기타', '기타'),
    )
    category = models.CharField(choices=categories, verbose_name='카테고리', max_length=255)
    title = models.CharField(max_length=100, verbose_name='제목')
    contents = models.TextField(null=True, verbose_name='내용')
    reference = models.URLField(verbose_name='관련 URL', null=True, blank=True)
    start_date = models.DateField(verbose_name='시작 날짜')
    end_date = models.DateField(verbose_name='종료 날짜')
    photo = models.ImageField(verbose_name='대표 이미지', null=True, blank=True)

    #<<<<<<bookmark 기능>>>>>>
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_user_set')

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.like_user_set.count()
