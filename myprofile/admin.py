from django.contrib import admin
from myprofile.models import Profile, BookMark

admin.site.register(Profile)



@admin.register(BookMark)
class BookMarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
