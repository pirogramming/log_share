from django.contrib import admin

from group_management.models import CustomGroup, GroupRequest

admin.site.register(CustomGroup)
admin.site.register(GroupRequest)
