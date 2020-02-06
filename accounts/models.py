from django.contrib.auth.models import User
from django.db import models
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill

def user_path(instance, filename): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    from random import choice
    import string # string.ascii_letters : ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s/%s.%s' % (instance.owner.username, pid, extension) # 예 : wayhome/abcdefgs.png

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.TextField(max_length=10)
    department = models.TextField(max_length=100, verbose_name='소속',blank=True)
    description = models.TextField(max_length=200, null=True, verbose_name='한줄소개')
    naver = models.URLField(verbose_name='네이버 URL', null=True, blank=True)
    daum = models.URLField(verbose_name='다음 URL', null=True, blank=True)
    github = models.URLField(verbose_name='깃 URL', null=True, blank=True)
    # photo = models.ImageField(null=True, verbose_name='프로필사진', upload_to=user_path)
    # profile_pic = models.ImageField(upload_to="blog/profile_pic")
    # 저장경로 : MEDIA_ROOT/blog/profile_pic/xxxx.jpg 경로에 저장
    # DB필드 : 'MEDIA_URL/blog/profile_pic/xxxx.jpg' 문자열 저장
    # photo = models.ImageField(blank=True, upload_to="blog/%Y/%m/%d")
    # other_url = models.URLField(verbose_name='기타 URL', null=True, blank=True)
    # description = models.TextField(max_length=200, null=True, verbose_name='한줄소개')


def __str__(self):
    return str(self.user) + ' profile'
# Create your models here.
