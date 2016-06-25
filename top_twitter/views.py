import itertools
import operator

import twitter
from django.conf import settings
from django.contrib.auth.decorators import login_required
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
                      'tweets': Tweet.objects.all().order_by('-created_at'),
                      'trends': [],
                      'error': False
                  },
                  RequestContext(request))


def popular_hashtag(request):
    # Create instance of Twitter API
    api = twitter.Api(settings.CONSUMER_KEY,
                      settings.CONSUMER_SECRET,
                      settings.ACCESS_TOKEN_KEY,
                      settings.ACCESS_TOKEN_SECRET)

    hashtags = api.GetTrendsWoeid(woeid=1)

    return render(request,
                  'top_twitter/popular_hashtag.html',
                  {
                      'hashtags': hashtags
                  },
                  RequestContext(request))


def add_tweets(hashtag_number, tweets_number):
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

    logging.info(len(trends))
    # Get only first 10 top-hashtags and delete rest
    del trends[int(hashtag_number):len(trends) - 1]

    for trend in trends:
        # Try to get tweets.
        new_tweets = api.GetSearch(result_type='popular', term=trend.query, count=int(tweets_number))
        tweets.extend(new_tweets)

    # Adding new tweets in database
    for tweet in tweets:
        if tweet.user.profile_banner_url == '' and tweet.user.profile_background_color == '':
            continue
        try:
            tweet_db_entry = Tweet.objects.create(
                # Don't forget to parse date
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

                # Don't forget to parse date
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

                # Save entry to database
                tweet_db_entry.save()
        except IntegrityError:
            # Tweet id duplicated or something like that. Don't mind, continue loop
            continue


def delete_tweets_all():
    Tweet.objects.all().delete()


@login_required
def statistics(request):
    def most_common_element(search_list):
        try:
            # get an iterable of (item, iterable) pairs
            SL = sorted((x, i) for i, x in enumerate(search_list))
            # print 'SL:', SL
            groups = itertools.groupby(SL, key=operator.itemgetter(0))

            # auxiliary function to get "quality" for an item
            def _auxfun(g):
                item, iterable = g
                count = 0
                min_index = len(search_list)
                for _, where in iterable:
                    count += 1
                    min_index = min(min_index, where)
                # print 'item %r, count %r, minind %r' % (item, count, min_index)
                return count, -min_index

            # pick the highest-count/earliest item
            return max(groups, key=_auxfun)[0]
        except ValueError:
            return 'hashtag'

    # Create hashtag list
    hashtag_set = []

    # Collect all hashtags
    for tweet in Tweet.objects.all():
        for tweet_hashtag in tweet.hashtag_set.all():
            hashtag_set.append(tweet_hashtag.text)

    # Find the most common hashtag
    popular_hashtag = most_common_element(hashtag_set)

    # Check is user wants to add more tweets
    if request.method == 'POST':
        if request.POST.get('hashtag_number'):
            add_tweets(request.POST.get('hashtag_number'), request.POST.get('tweets_number'))

    # Check is user wants to delete tweets
    if request.method == 'POST':
        if request.POST.get('action') == 'delete_all':
            delete_tweets_all()

    return render(request,
                  'top_twitter/statistics.html',
                  {
                      'tweets': Tweet.objects.all().order_by('-created_at'),
                      'popular_hashtag': popular_hashtag,
                      'added_successful': True
                  },
                  RequestContext(request))
