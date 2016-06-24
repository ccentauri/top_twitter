from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core import validators

from material import *


class App(models.Model):
    id = models.IntegerField(primary_key=True,
                             unique=True,
                             editable=False,
                             auto_created=True,
                             db_index=True)

    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    description = models.TextField(default='')
    article = models.TextField(default='')

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,
                                          null=True,
                                          default=timezone.now)

    link_source = models.CharField(max_length=200,
                                   default='',
                                   validators=[validators.URLValidator()])
    link_apk = models.CharField(max_length=200,
                                default='',
                                validators=[validators.URLValidator()])

    preview_image = models.ImageField(upload_to='uploads/images/previews/',
                                      default='',
                                      help_text='Preview image. Only 1600x800 allowed')

    icon = models.ImageField(upload_to='uploads/images/icons/',
                             default='',
                             help_text='Small icon')

    # TODO create ColorPicker widget
    color_primary = models.CharField(max_length=7, default='#000000')
    color_secondary = models.CharField(max_length=7, default='#000000')

    def publish(self):
        self.published_date = timezone.now
        self.save()

    def __str__(self):
        return self.title


class Screenshot(models.Model):
    file = models.ImageField(upload_to='uploads/images/screenshots')
    page = models.ForeignKey('App')
