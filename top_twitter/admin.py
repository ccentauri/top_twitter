from django.contrib import admin
from top_twitter.models import Tweet


@admin.register(Tweet)
class Admin(admin.ModelAdmin):
    # Get related field - User
    def user(self):
        return '<p>%s</p>' % (self.user.name,)

    # Allow HTML
    user.allow_tags = True

    # Filter for display
    list_display = ('created_at', 'text', user)

    # Order by created_at descending
    ordering = ('-created_at',)
