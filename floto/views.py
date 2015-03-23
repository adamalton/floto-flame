# STANDARD LIB
import logging

# LIBRARIES
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
import flickr_api

# FLOTO
from floto.http import JsonResponse
from floto.models import Photo
from floto import utils

PHOTO_TAGS = "photoframe"

AUTH_CACHE_KEY = "flickr_api_auth_object"
AUTH_FILENAME = "flickr_api_auth.txt"
flickr_api.set_keys(api_key=settings.FLICKR_API_KEY, api_secret = settings.FLICKR_API_SECRET)


def start_oauth(request):
    auth = flickr_api.auth.AuthHandler(callback=utils.get_oauth_callback_url(request))
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


def trigger_photo_list_refresh(request):
    """ Fetches the list of photos from Flickr and makes sure that we have a Photo object for each
        one.
    """
    flickr_api.set_auth_handler(AUTH_FILENAME)
    photos = []
    page = 1
    pages = 1
    while page <= pages:
        result = flickr_api.Photo.search(tags=PHOTO_TAGS, user_id="me", page=page)
        photos += [p for p in result]
        pages = result.info.pages
        page += 1

    def _get_photo_values(photo):
        # On the raspberry Pi this seems to sometimes die, hence it's wrapped in a retriable func
        return dict(
            url=photo.getPhotoFile(),
            rotation=photo.rotation,
            title=photo['title']
        )

    for photo in photos:
        defaults = utils.do_with_retry(_get_photo_values, photo)
        Photo.objects.update_or_create(pk=photo['id'], defaults=defaults)
    return HttpResponse("Photo list refreshed")


def get_photo_list(request):
    photos = Photo.objects.order_by('?')
    data = []
    for photo in photos:
        data.append(dict(
            id=photo.pk,
            title=photo.title,
            timestamp=photo.timestamp,
            rotation=photo.rotation,
            serving_url=photo.serving_url,
        ))
    return JsonResponse(data)


def frame(request):
    """ The main view which is actually used to display the photos. """
    return render(request, "floto/frame.html", {})


def image_proxy(request, photo_id):
    """ A view which serves the image file (jpeg) for a photo, either from our local storage or
        by fetching it from Flickr (and putting it in local storage in the process).
    """
    photo = get_object_or_404(Photo, pk=photo_id)
    if not photo.cached_image:
        photo.cache_image()
    image_data = photo.cached_image.read()
    return HttpResponse(image_data, content_type=photo.content_type)
