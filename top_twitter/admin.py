from django.contrib import admin
from top_twitter.models import Tweet, User, Url


class UserInline(admin.TabularInline):
    model = User
    fields = ('name', 'profile_banner_url', 'profile_image_url', 'profile_background_color')


class UrlInline(admin.TabularInline):
    model = Url
    fields = ('url',)


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

    inlines = (UserInline, UrlInline)
