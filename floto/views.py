# LIBRARIES
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import flickr_api

# FLOTO
from floto.models import Photo
from floto.utils import (
    get_oauth_callback_url,
)

AUTH_CACHE_KEY = "flickr_api_auth_object"
AUTH_FILENAME = "flickr_api_auth.txt"
flickr_api.set_keys(api_key=settings.FLICKR_API_KEY, api_secret = settings.FLICKR_API_SECRET)


def start_oauth(request):
    auth = flickr_api.auth.AuthHandler(callback=get_oauth_callback_url(request))
    url = auth.get_authorization_url("read")
    cache.set(AUTH_CACHE_KEY, auth)
    return HttpResponseRedirect(url)


def oauth_callback(request):
    auth = cache.get(AUTH_CACHE_KEY)
    auth.set_verifier(request.GET['oauth_verifier'])
    #TODO: the request also contains 'oauth_token' - why do we not use/need that?
    flickr_api.set_auth_handler(auth) # My god it's not thread safe
    auth.save(AUTH_FILENAME)
    return redirect("frame")


def frame(request):
    flickr_api.set_auth_handler(AUTH_FILENAME)
    user = flickr_api.test.login()
    photos = user.getPhotos()
    import pdb; pdb.set_trace()
    # photos[0].save('photo.jpg')
    for photo in photos:
        url = photo.getPhotoFile()
        rotation = photo['rotation']
        Photo.objects.get_or_create(pk=photo['id'], url=url, rotation=rotation)
        p = Photo.objects.get_or
    photos = [p.getPhotoFile() for p in photos]
    context = dict(
        photos=photos,
    )
    return render(request, "floto/frame.html", context)


def image_proxy(request, img_id):
    raise NotImplementedError()


