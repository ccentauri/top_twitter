from django.db import models


class Post(models.Model):
    id = models.IntegerField(primary_key=True,
                             unique=True,
                             editable=False,
                             auto_created=True,
                             db_index=True)

    author_name = models.CharField(max_length=100, default='@')
    author_link = models.CharField(max_length=100, default='@')
    author_image = models.URLField(max_length=200, default='')
    date = models.DateTimeField()
    message = models.TextField()
