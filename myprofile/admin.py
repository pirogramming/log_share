from django.contrib import admin
from myprofile.models import Profile, Site, BookMark

admin.site.register(Profile)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['link', 'profile']

@admin.register(BookMark)
class BookMarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
