from django.contrib import admin
from top_twitter.models import Tweet


@admin.register(Tweet)
class Admin(admin.ModelAdmin):
    list_display = ('id',)
