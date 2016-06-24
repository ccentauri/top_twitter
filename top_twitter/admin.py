from django.contrib import admin
from top_twitter.models import Post


@admin.register(Post)
class Admin(admin.ModelAdmin):
    list_display = ('author_name',)
