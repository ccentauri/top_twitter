from django.contrib import admin
from top_twitter.models import Tweet, User


@admin.register(Tweet)
class Admin(admin.ModelAdmin):
    def user(self):
        return '<p>%s</p>' % (self.user.name,)

    user.allow_tags = True

    list_display = ('id', 'created_at', 'text', user)
    ordering = ('-created_at',)
