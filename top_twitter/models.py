from django.db import models


class Tweet(models.Model):
    created_at = models.DateTimeField()
    favorite_count = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    id_str = models.CharField(max_length=2000)
    lang = models.CharField(max_length=2000)
    retweet_count = models.IntegerField()
    source = models.TextField()
    text = models.TextField()


class HashTag(models.Model):
    tweet = models.ForeignKey(Tweet)

    text = models.CharField(max_length=2000)


class Url(models.Model):
    tweet = models.ForeignKey(Tweet)

    url = models.CharField(max_length=3000)
    expanded_url = models.CharField(max_length=3000)


class User(models.Model):
    tweet = models.OneToOneField(Tweet, primary_key=True)

    created_at = models.DateTimeField()
    description = models.TextField()
    favourites_count = models.IntegerField()
    followers_count = models.IntegerField()
    friends_count = models.IntegerField()
    geo_enabled = models.BooleanField()
    id = models.IntegerField()
    lang = models.CharField(max_length=3000)
    listed_count = models.IntegerField()
    location = models.CharField(max_length=3000)
    name = models.CharField(max_length=3000)
    profile_background_color = models.CharField(max_length=3000)
    profile_background_image_url = models.CharField(max_length=3000)
    profile_background_tile = models.CharField(max_length=3000)
    profile_banner_url = models.CharField(max_length=3000)
    profile_image_url = models.CharField(max_length=3000)
    profile_link_color = models.CharField(max_length=3000)
    profile_sidebar_fill_color = models.CharField(max_length=3000)
    profile_text_color = models.CharField(max_length=3000)
    screen_name = models.CharField(max_length=3000)
    statuses_count = models.CharField(max_length=3000)
    time_zone = models.CharField(max_length=3000)
    url = models.CharField(max_length=3000)
    utc_offset = models.IntegerField()
    verified = models.BooleanField()


class UserMention(models.Model):
    tweet = models.ForeignKey(Tweet)

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    screen_name = models.CharField(max_length=300)
