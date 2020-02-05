from django.contrib import admin
from myprofile.models import Profile, Site, BookMark

admin.site.register(Profile)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['profile', 'link']

@admin.register(BookMark)
class BookMarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
