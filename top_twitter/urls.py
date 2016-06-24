from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^tags/', views.popular_hashtag, name='popular_hashtag'),

    # Remove before deploying!
    url(r'^angular/', views.angular, name='angular'),
]