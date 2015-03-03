from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'floto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'floto.views.home', name='home'),
    url(r'^frame/$', 'floto.views.frame', name='frame'),
    url(r'^config/$', 'floto.views.config', name='config'),
    url(r'^flickr-oauth-callback/$', 'floto.views.flickr_oauth_callback', name='flickr_oauth_callback'),
    url(r'^image-proxy/$', 'floto.views.image_proxy', name='image_proxy'),
)
