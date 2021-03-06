# STANDARD LIB
from datetime import datetime
import json
import logging
import os

# LIBRARIES
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import flickr_api

# FLOTO
from floto.http import JsonResponse
from floto.models import Photo, Album
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
    if not os.path.exists(os.path.join(settings.BASE_DIR, AUTH_FILENAME)):
        logging.info("%s does not exist", AUTH_FILENAME)
        return redirect("start_oauth")

    flickr_api.set_auth_handler(AUTH_FILENAME)
    photos = []
    page = 1
    pages = 1
    while page <= pages:
        logging.info("Fetching photos from Flickr API, page %s", page)
        result = flickr_api.Photo.search(tags=PHOTO_TAGS, user_id="me", page=page, extras="date_taken")
        photos += [p for p in result]
        pages = result.info.pages
        page += 1

    def _get_photo_values(photo):
        # On the raspberry Pi this seems to sometimes die, hence it's wrapped in a retriable func
        date_taken = photo.datetaken
        date_taken = datetime.strptime(date_taken, '%Y-%m-%d %H:%M:%S')
        # Stop Django complaining about it not being explicitly UTC
        date_taken = timezone.make_aware(date_taken)
        location = photo.get('location', {})
        location = json.dumps(location)

        return dict(
            url=photo.getPhotoFile(),
            rotation=photo.rotation,
            title=photo['title'],
            date_taken=date_taken,
            date_taken_granularity=int(photo.datetakengranularity),
            location=location,
        )

    for photo in photos:
        defaults = utils.do_with_retry(_get_photo_values, photo)
        photo_instance, created = Photo.objects.update_or_create(pk=photo['id'], defaults=defaults)
        logging.info("%s photo %s", ("created" if created else "updated"), photo_instance.pk)
        if created:
            logging.info("Updating album info...")
            _update_album_info(photo_instance, photo)
    return HttpResponse("Photo list refreshed")


def trigger_album_info_refresh(request):
    """ For existing photos, make sure that the `albums` field (and related Album objects) are up
        to date.
    """
    # This doesn't need doing very often, and we might not want to update them *all* at once, as
    # that might block other requests, so just do 100 random ones at a time and we can call it often
    limit = request.GET.get('limit', 100)
    for photo in Photo.objects.order_by('?')[:limit]:
        _update_album_info(photo)


def _update_album_info(photo, api_photo=None):
    """ Given a models.Photo object, and optionally a flickr_api.Photo instance of it, update its
        album info.
    """
    if api_photo is None:
        flickr_api.set_auth_handler(AUTH_FILENAME)
        api_photo = flickr_api.Photo(id=photo.id)
    api_albums = api_photo.getAllContexts()[0]  # It returns a list of [albums, pools]
    albums = []
    for api_album in api_albums:
        album, created = Album.objects.update_or_create(
            id=api_album.id, defaults={"title": api_album.title}
        )
        albums.append(album)
    photo.albums.set(albums)


def get_photo_list(request):
    photos = Photo.objects.order_by('?')
    data = []
    for photo in photos:
        data.append(dict(
            id=photo.pk,
            title=photo.title_display,
            timestamp=photo.timestamp,
            rotation=photo.rotation,
            serving_url=photo.serving_url,
            location=photo.location_display,
            album=photo.primary_album_display,
            date_taken=photo.date_taken_display,
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


def shutdown(request):
    if request.method == "POST":
        # This doesn't seem to shut the computer down IMMEDIATELY, so we can redirect and it will
        # probably manage to render the page before the computer shuts down
        utils.shutdown()
        request.session["shutting_down"] = True
        return HttpResponseRedirect(request.path)
    else:
        shutting_down = request.session.pop("shutting_down", False)
        return render(request, "floto/shutdown.html", {"shutting_down": shutting_down})
