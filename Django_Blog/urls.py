"""Django_Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from Django_Blog import settings
from blog import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(admin.site.urls)),
    url(r'^$', views.post_list, name='post_list'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^apps/(?P<post_id>[0-9]+)/$', views.post_page, name='post_detail'),

    url(r'^twitter/', include('top_twitter.urls')),

    # http://docs.djangoproject.com/en/dev/howto/static-files/
    # This method is inefficient and insecure.
    # Do not use this in a production setting.
    # Use this only for development.
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
]
