# Generated by Django 2.2.9 on 2020-02-20 04:51

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='콤마(,)로 태그를 분리해주세요.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
