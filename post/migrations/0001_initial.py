# Generated by Django 2.2.9 on 2020-03-05 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import post.utils
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('대외활동', '대외활동'), ('공모전', '공모전'), ('스터디', '스터디'), ('인턴', '인턴'), ('강연', '강연'), ('기타', '기타')], max_length=5, verbose_name='카테고리')),
                ('title', models.CharField(max_length=100, verbose_name='제목')),
                ('contents', models.TextField(blank=True, null=True, verbose_name='내용')),
                ('reference', models.URLField(blank=True, null=True, verbose_name='관련 URL')),
                ('start_date', models.DateField(verbose_name='시작 날짜')),
                ('end_date', models.DateField(verbose_name='종료 날짜')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=post.utils.date_upload_to, verbose_name='대표 이미지')),
                ('score', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='추천도')),
                ('tags', taggit.managers.TaggableManager(help_text='콤마(,)로 태그를 분리해주세요.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_post', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
