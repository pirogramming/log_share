# Generated by Django 2.2.9 on 2020-02-11 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20200207_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contents',
            field=models.TextField(blank=True, null=True, verbose_name='내용'),
        ),
    ]
