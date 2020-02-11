# Generated by Django 2.2.9 on 2020-02-11 06:24

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
            name='CustomGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=50, unique=True, verbose_name='그룹명')),
                ('group_category', models.CharField(choices=[('art', '문화/예술/공연'), ('volunteer', '봉사/사회활동'), ('scholarship', '학술/교양'), ('startup', '창업/취업'), ('language', '어학'), ('physical', '체육'), ('play', '친목'), ('etc', '기타')], default='etc', max_length=50, verbose_name='카테고리')),
                ('notes', models.TextField(blank=True, verbose_name='그룹설명')),
                ('is_searchable', models.BooleanField(verbose_name='검색허용')),
                ('access_code', models.CharField(blank=True, max_length=50, verbose_name='그룹검색코드')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_manage_groups', to=settings.AUTH_USER_MODEL, verbose_name='그룹장')),
                ('members', models.ManyToManyField(related_name='user_groups', to=settings.AUTH_USER_MODEL, verbose_name='그룹멤버')),
            ],
            options={
                'verbose_name_plural': 'groups',
                'ordering': ['group_name'],
            },
        ),
        migrations.CreateModel(
            name='GroupRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group_management.CustomGroup')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('group', 'sender')},
            },
        ),
    ]
