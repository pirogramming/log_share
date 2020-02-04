from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    search_fields = ['title']


from django.contrib import admin

# Register your models here.
