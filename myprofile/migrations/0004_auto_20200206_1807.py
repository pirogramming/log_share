# Generated by Django 2.2.9 on 2020-02-06 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myprofile', '0003_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
