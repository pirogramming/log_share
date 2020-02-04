from django.db import models
from django.contrib.auth.models import User


#POST - 추후삭제
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='post')
    categories = (
        ('대외활동', '대외활동'),
        ('동아리', '동아리'),
        ('공모전', '공모전'),
        ('스터디', '스터디'),
        ('인턴', '인턴'),
        ('강연', '강연'),
        ('기타', '기타'),
    )
    category = models.CharField(choices=categories, verbose_name='카테고리', max_length=255)
    title = models.CharField(max_length=100, verbose_name='제목')
    contents = models.TextField(null=True, verbose_name='내용')
    reference = models.URLField(verbose_name='관련 URL', null=True, blank=True)
    start_date = models.DateField(verbose_name='시작 날짜')
    end_date = models.DateField(verbose_name='종료 날짜')
    photo = models.ImageField(verbose_name='대표 이미지', null=True, blank=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(null=True, blank=True, verbose_name='프로필사진')
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


class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmark')
    #자기 자신 post 제외하자!!!!
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='bookmark')

    def __str__(self):
        return self.post.title

