from django.contrib import admin
from myprofile.models import Profile, Site, Post, BookMark

admin.site.register(Profile)
admin.site.register(Site)
admin.site.register(Post)
admin.site.register(BookMark)