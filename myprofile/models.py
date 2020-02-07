from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from post.models import Post




class Profile(models.Model):
    # (in database) ForeignKey - user,profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=20)
    photo = models.ImageField(null=True, blank=True, verbose_name='프로필사진')
    department = models.CharField(max_length=100, verbose_name='소속')
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name='한줄소개')
    interested_tag = models.CharField(max_length=255, null=True, blank=True, verbose_name='관심태그')
    naver = models.URLField(verbose_name='네이버 URL', null=True, blank=True)
    daum = models.URLField(verbose_name='다음 URL', null=True, blank=True)
    github = models.URLField(verbose_name='깃 URL', null=True, blank=True)
    other_url = models.URLField(verbose_name='기타 URL', null=True, blank=True)

    def __str__(self):
        return str(self.user) + ' profile'



# todo model change - ForeignKey
# 두번째 방법) BookMark 모델 필요없이 Post모델에 user = ManyToMany(User)
class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookmark')
    # 같은 user가 여러개의 bookmark를 가질수 있듯이 같은 post가 여러개의 bookmark를 가질 수 있다
    # 따라서 user-post manytomany 관계의 중재 모델 == bookmark
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmark')

    def __str__(self):
        return self.post.title
