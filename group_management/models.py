from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.db import models


class CustomGroup(Group):
    # todo: group 관리자 정하기
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
    category = models.CharField(max_length=50, default='etc', choices=categories, verbose_name='카테고리')
    notes = models.TextField(blank=True, verbose_name='그룹설명')
    is_searchable = models.BooleanField(verbose_name='검색허용')

    class Meta:
        verbose_name_plural = "groups"
        ordering = ['name']

    def __str__(self):
        return self.name


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