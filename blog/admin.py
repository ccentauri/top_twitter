from django.contrib import admin
from .models import App, Screenshot


class ScreenshotInline(admin.StackedInline):
    model = Screenshot


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    empty_value_display = '--empty--'
    list_display = ('id', 'title', 'created_date', 'published_date')
    inlines = [ScreenshotInline, ]

    # Display several fields on the same line
    # fields = ('author', 'title', 'text', 'created_date', 'published_date',
    # ('link_preview', 'link_source'), 'link_apk')

    # Display additional groups
    fieldsets = (
        ('Main info', {
            'classes': ('collapse',),
            'fields': (
                'author', 'title', 'description', 'article', 'created_date', 'published_date', )
        }),
        ('Links', {
            'classes': ('collapse',),
            'fields': ('link_source', 'link_apk')
        }),
        ('Images', {
            'classes': ('collapse',),
            'fields': ('preview_image', 'icon')
        }),
        ('Colors', {
            'classes': ('collapse',),
            'fields': (('color_primary', 'color_secondary'),)
        })
    )
