# THIRD PARTY
from django.conf.urls import url

# FLOTO
from floto import views


urlpatterns = [
    # url(r'^$', 'home', name='home'),
    url(r'^frame/$', views.frame, name='frame'),
    url(r'^get-photo-list/$', views.get_photo_list, name='get_photo_list'),
    url(r'^trigger-photo-list-refresh/$', views.trigger_photo_list_refresh, name='trigger_photo_list_refresh'),
    url(r'^trigger-album-info-refresh/$', views.trigger_album_info_refresh, name='trigger_album_info_refresh'),
    url(r'^image-proxy/(?P<photo_id>\d+)/$', views.image_proxy, name='image_proxy'),
    url(r'^start-oauth/$', views.start_oauth, name='start_oauth'),
    url(r'^oauth-callback/$', views.oauth_callback, name='oauth_callback'),
    url(r'store-current-photo-index/$', views.store_current_photo_index, name='store_current_photo_index'),
    url(r'admin/$', views.admin, name='admin'),
    url(r'shutdown/$', views.shutdown, name='shutdown'),
]
