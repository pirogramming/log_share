from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager

from .utils import date_upload_to


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_post')
    categories = (
        ('대외활동', '대외활동'),
        ('공모전', '공모전'),
        ('스터디', '스터디'),
        ('인턴', '인턴'),
        ('강연', '강연'),
        ('기타', '기타'),
    )
    category = models.CharField(choices=categories, verbose_name='카테고리', max_length=5)
    title = models.CharField(max_length=100, verbose_name='제목')
    contents = models.TextField(null=True, blank=True, verbose_name='내용')
    reference = models.URLField(verbose_name='관련 URL', null=True, blank=True)
    start_date = models.DateField(verbose_name='시작 날짜')
    end_date = models.DateField(verbose_name='종료 날짜')
    photo = models.ImageField(upload_to=date_upload_to, verbose_name='대표 이미지', null=True, blank=True)
    tags = TaggableManager()
    SCORE_CHOICES = zip(range(1,6), range(1,6))
    score = models.IntegerField(choices=SCORE_CHOICES, verbose_name='추천도')

    def __str__(self):
        return self.title

    @property
    def is_valid_date(self):
        return self.end_date > self.start_date
