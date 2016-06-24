import twitter
from django.conf import settings
from django.db import IntegrityError
from twitter.error import TwitterError
from django.shortcuts import render
from django.template import RequestContext
import logging
from dateutil.parser import parse

from top_twitter.models import Tweet, HashTag, UserMention, Url, User


def post_list(request):
    # # Create instance of Twitter API
    # api = twitter.Api(settings.CONSUMER_KEY,
    #                   settings.CONSUMER_SECRET,
    #                   settings.ACCESS_TOKEN_KEY,
    #                   settings.ACCESS_TOKEN_SECRET)
    #
    # # Try to get top hashtags.
    # # Catching TwitterError ('Rate limit exceeded', etc)
    # try:
    #     trends = api.GetTrendsWoeid(woeid=1)
    # except TwitterError:
    #     logging.error(TwitterError.message)
    #     trends = []
    #
    # # Create list of tweets
    # tweets = []
    # error = False
    #
    # # Check if we have any hashtags in list
    # if trends:
    #     # Get only first 10 top-hashtags and delete rest
    #     del trends[9:len(trends) - 1]
    #
    #     # Find the latest tweets for hashtag
    #     for trend in trends:
    #         # Try to get tweets.
    #         # Catching TwitterError ('Rate limit exceeded', etc)
    #         try:
    #             tweets.append(
    #                 api.GetSearch(result_type='popular', term=trend.query, count=settings.TWEETS_LOADING_NUMBER))
    #         except TwitterError:
    #             error = True
    # else:
    #     # If trends list is empty - error was occurred
    #     error = True

    return render(request,
                  'top_twitter/post_list.html',
                  {
                      'tweets': Tweet.objects.all(),
                      'trends': [],
                      'error': False
                  },
                  RequestContext(request))


def popular_hashtag(request):
    api = twitter.Api(consumer_key='Hc2uDuKnrBYD8fzkhFw8THOzr',
                      consumer_secret='ypWJFvpRSNbdAPqXp8me137SuUitTV0xkTC5EWiozYpv2QjM25',
                      access_token_key='707631903608868869-jvTlyWZChllWMzGOWEsyF0PFrVtLQrI',
                      access_token_secret='hFqKoa54LF470kSRmzbxnmSkz4SlKBuZlbYfCumDEmLDf')
    hashtags = api.GetTrendsWoeid(woeid=1)
    return render(request, 'top_twitter/popular_hashtag.html', {'hashtags': hashtags},
                  RequestContext(request))


def add(request):
    # Create instance of Twitter API
    api = twitter.Api(settings.CONSUMER_KEY,
                      settings.CONSUMER_SECRET,
                      settings.ACCESS_TOKEN_KEY,
                      settings.ACCESS_TOKEN_SECRET)

    # Try to get top hashtags.
    # Catching TwitterError ('Rate limit exceeded', etc)
    try:
        trends = api.GetTrendsWoeid(woeid=1)
    except TwitterError:
        logging.error(TwitterError.message)
        trends = []

    # Create list of tweets
    tweets = []
    error = False

    # Check if we have any hashtags in list
    if trends:
        # Get only first 10 top-hashtags and delete rest
        del trends[9:len(trends) - 1]

        # Find the latest tweets for hashtag
        for trend in trends:
            # Try to get tweets.
            # Catching TwitterError ('Rate limit exceeded', etc)
            try:
                tweets.extend(
                    api.GetSearch(result_type='popular', term=trend.query, count=settings.TWEETS_LOADING_NUMBER))
            except TwitterError:
                error = True
    else:
        # If trends list is empty - error was occurred
        error = True

    # Adding new tweets in database
    for tweet in tweets:
        try:
            tweet_db_entry = Tweet.objects.create(
                created_at=parse(tweet.created_at).strftime("%Y-%m-%d %H:%M:%S"),
                favorite_count=tweet.favorite_count,
                id=tweet.id,
                id_str=tweet.id_str,
                lang=tweet.lang,
                retweet_count=tweet.retweet_count,
                source=tweet.source,
                text=tweet.text,
            )

            for hashtag in tweet.hashtags:
                tweet_db_entry.hashtag_set.add(
                    HashTag.objects.create(
                        tweet=tweet_db_entry,

                        text=hashtag.text
                    ))

            for url in tweet.urls:
                tweet_db_entry.url_set.add(
                    Url.objects.create(
                        tweet=tweet_db_entry,

                        url=url.url,
                        expanded_url=url.expanded_url
                    ))

            tweet_db_entry.user = User.objects.create(
                tweet=tweet_db_entry,

                created_at=parse(tweet.user.created_at).strftime("%Y-%m-%d %H:%M:%S"),
                description=tweet.user.description,
                favourites_count=tweet.user.favourites_count,
                followers_count=tweet.user.followers_count,
                friends_count=tweet.user.friends_count,
                geo_enabled=tweet.user.geo_enabled,
                id=tweet.user.id,
                lang=tweet.user.lang,
                listed_count=tweet.user.listed_count,
                location=tweet.user.location,
                name=tweet.user.name,
                profile_background_color=tweet.user.profile_background_color,
                profile_background_image_url=tweet.user.profile_background_image_url,
                profile_background_tile=tweet.user.profile_background_tile,
                profile_banner_url=tweet.user.profile_banner_url,
                profile_image_url=tweet.user.profile_image_url,
                profile_link_color=tweet.user.profile_link_color,
                profile_sidebar_fill_color=tweet.user.profile_sidebar_fill_color,
                profile_text_color=tweet.user.profile_text_color,
                screen_name=tweet.user.screen_name,
                statuses_count=tweet.user.statuses_count,
                time_zone=tweet.user.time_zone,
                url=tweet.user.url,
                utc_offset=tweet.user.utc_offset,
                verified=tweet.user.verified
            )

            for usermention in tweet.user_mentions:
                tweet_db_entry.usermention_set.add(
                    UserMention.objects.create(
                        tweet=tweet_db_entry,

                        id=usermention.id,
                        name=usermention.name,
                        screen_name=usermention.screen_name
                    ))

                tweet_db_entry.save()
        except IntegrityError:
            continue

    return render(request,
                  'top_twitter/twitter_add.html',
                  {
                      'tweets': Tweet.objects.all(),
                      'error': error
                  },
                  RequestContext(request))
