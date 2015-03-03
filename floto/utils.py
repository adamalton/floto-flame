# LIBRARIES
from django.core.cache import cache
from django.core.urlresolvers import reverse
import flickrapi

# FLOTO
from floto.models import Config

OAUTH_TOKEN_CACHE_KEY = 'oauth_token'


def get_flicker_api_instance(config=None):
    """ Get an instance of flickrapi.FlickrAPI based on the Config object in the DB. """
    if not config:
        config = Config.objects.get()
    token = cache.get(OAUTH_TOKEN_CACHE_KEY)
    flickr = flickrapi.FlickrAPI(
        config.api_key,
        config.secret,
        # username=config.flickr_username,
        format='parsed-json',
        token=token,
        store_token=False,
    )
    return flickr


def has_valid_oauth_token(flickr):
    """ Does the given FlickrAPI instance have a valid oauth token? """
    try:
        status = flickr.auth_checkToken()
        if status['stat'] == u"ok":
            return True
    except flickrapi.FlickrError:
        pass
    return False


def get_oauth_auth_url(flickr, request):
    """ Given an instance of the FlickrAPI (which presumably doesn't have a valid oauth token)
        return the URL for the user to authorise with.
    """
    callback_url = reverse("flickr_oauth_callback")
    protocol = "https" if request.is_secure() else "http"
    host = request.get_host()
    callback_url = "%s://%s%s" % (protocol, host, callback_url)
    flickr.get_request_token(oauth_callback=callback_url)
    return flickr.auth_url()


def store_oauth_token(token_str):
    """ Given a string representation of an oauth token, convert it for the Flicr API
        for the user defined in the Config, and store it in the cache.
    """
    config = Config.objects.get()
    # flickr = get_flicker_api_instance()
    # import pdb; pdb.set_trace()
    token = flickrapi.auth.FlickrAccessToken(
        unicode(token_str), config.secret,
        flickrapi.auth.FlickrAccessToken.levels[0], # read
    )
    # token = flickr.get_token(token_str)
    cache.set(OAUTH_TOKEN_CACHE_KEY, token)


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
