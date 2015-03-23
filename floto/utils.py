# LIBRARIES
from django.core.urlresolvers import reverse

# FLOTO
from floto.models import Photo


def get_oauth_callback_url(request):
    """ Get the full URI (including protocol) of our 'flickr_oauth_callback' view. """
    callback_url = reverse("oauth_callback")
    protocol = "https" if request.is_secure() else "http"
    host = request.get_host()
    return "%s://%s%s" % (protocol, host, callback_url)


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def cache_images(limit=None):
    photos = Photo.objects.filter(cached_image=None)
    if limit:
        photos = photos[:limit]
    for photo in photos:
        photo.cache_image()

def do_with_retry(func, *args, **kwargs):
    retries = kwargs.pop('_retries', 5)
    catch = kwargs.pop('_catch', Exception)
    tries = 0
    while tries < retries:
        try:
            return func(*args, **kwargs)
        except catch:
            tries += 1
    raise
