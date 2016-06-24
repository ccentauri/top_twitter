from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^tags/', views.popular_hashtag, name='popular_hashtag'),
    url(r'^statistics/', views.statistics, name='statistics'),

    # Remove before deploying!
    url(r'^add/', views.add, name='add'),
]
