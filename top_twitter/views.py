import twitter
from django.conf import settings
from twitter.error import TwitterError
from django.shortcuts import render
from django.template import RequestContext
import logging


def post_list(request):
    # Create instance of Twitter API
    api = twitter.Api(settings.CONSUMER_KEY,
                      settings.CONSUMER_SECRET,
                      settings.ACCESS_TOKEN_KEY,
                      settings.ACCESS_TOKEN_SECRET)

    # Try to get top hashtags.
    # Catch TwitterError ('Rate limit exceeded', etc)
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
        # Find the latest tweets for hashtag
        # for trend in trends[0]:
        tweets.extend(api.GetSearch(term=trends[0].query, count=settings.TWEETS_LOADING_NUMBER))
    else:
        error = True

    return render(request,
                  'top_twitter/post_list.html',
                  {'tweets': tweets,
                   'error': error},
                  RequestContext(request))


def popular_hashtag(request):
    api = twitter.Api(consumer_key='Hc2uDuKnrBYD8fzkhFw8THOzr',
                      consumer_secret='ypWJFvpRSNbdAPqXp8me137SuUitTV0xkTC5EWiozYpv2QjM25',
                      access_token_key='707631903608868869-jvTlyWZChllWMzGOWEsyF0PFrVtLQrI',
                      access_token_secret='hFqKoa54LF470kSRmzbxnmSkz4SlKBuZlbYfCumDEmLDf')
    hashtags = api.GetTrendsWoeid(woeid=1)
    return render(request, 'top_twitter/popular_hashtag.html', {'hashtags': hashtags},
                  RequestContext(request))
