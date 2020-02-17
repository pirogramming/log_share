from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class CustomGroup(models.Model):
    categories = (
        ('art', '문화/예술/공연'),
        ('volunteer', '봉사/사회활동'),
        ('scholarship', '학술/교양'),
        ('startup', '창업/취업'),
        ('language', '어학'),
        ('physical', '체육'),
        ('play', '친목'),
        ('etc', '기타'),
    )
    members = models.ManyToManyField(User, verbose_name='그룹멤버', related_name='user_groups', db_table='group_membership')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='그룹장', related_name='user_manage_groups')
    group_name = models.CharField(max_length=50, unique=True, verbose_name='그룹명')
    group_category = models.CharField(max_length=50, default='etc', choices=categories, verbose_name='카테고리')
    notes = models.TextField(blank=True, verbose_name='그룹설명')
    is_searchable = models.BooleanField(verbose_name='검색허용')
    access_code = models.CharField(max_length=50, blank=True, verbose_name='그룹가입코드')

    class Meta:
        verbose_name_plural = "groups"
        ordering = ['group_name']

    def __str__(self):
        return self.group_name


class GroupMembership(models.Model):
    customgroup = models.ForeignKey(CustomGroup, models.DO_NOTHING, related_name='membership')
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'group_membership'
        unique_together = (('customgroup', 'user'),)



class GroupRequest(models.Model):
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{} -> {}".format(self.sender, self.group)

    class Meta:
        unique_together = (
            ('group', 'sender')
        )
