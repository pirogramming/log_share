# Generated by Django 2.2.9 on 2020-02-07 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='프로필사진')),
                ('department', models.CharField(max_length=100, verbose_name='소속')),
                ('description', models.TextField(blank=True, max_length=200, null=True, verbose_name='한줄소개')),
                ('interested_tag', models.CharField(blank=True, max_length=255, null=True, verbose_name='관심태그')),
                ('naver', models.URLField(blank=True, null=True, verbose_name='네이버 URL')),
                ('daum', models.URLField(blank=True, null=True, verbose_name='다음 URL')),
                ('github', models.URLField(blank=True, null=True, verbose_name='깃 URL')),
                ('other_url', models.URLField(blank=True, null=True, verbose_name='기타 URL')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]