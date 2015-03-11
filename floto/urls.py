from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('floto.views',

    # url(r'^$', 'home', name='home'),
    url(r'^frame/$', 'frame', name='frame'),
    url(r'^get-photo-list/$', 'get_photo_list', name='get_photo_list'),
    url(r'^trigger-photo-list-refresh/$', 'trigger_photo_list_refresh', name='trigger_photo_list_refresh'),
    url(r'^image-proxy/(?P<photo_id>\d+)/$', 'image_proxy', name='image_proxy'),
    url(r'^start-oauth/$', 'start_oauth', name='start_oauth'),
    url(r'^oauth-callback/$', 'oauth_callback', name='oauth_callback'),
)
