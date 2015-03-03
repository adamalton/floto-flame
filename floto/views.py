# STANDARD LIB
import logging

# LIBRARIES
from django.shortcuts import render, redirect, get_object_or_404

# FLOTO
from floto.forms import ConfigForm
from floto.models import Config
from floto.utils import (
    get_flicker_api_instance,
    get_oauth_auth_url,
    get_object_or_none,
    has_valid_oauth_token,
    store_oauth_token,
)


def home(request):
    config = get_object_or_none(Config)
    if not config:
        # No settings yet, just redirect to the config page
        return redirect("config")
    # else...
    flickr = get_flicker_api_instance(config)
    if has_valid_oauth_token(flickr):
        context = dict(
            have_valid_oauth_token=True,
        )
    else:
        context = dict(
            have_valid_oauth_token=False,
            oauth_url=get_oauth_auth_url(flickr, request),
        )
    return render(request, "floto/home.html", context)


def frame(request):
    config = get_object_or_none(Config)
    if not config:
        return redirect('config')
    flickr = get_flicker_api_instance(config)
    if not has_valid_oauth_token(flickr):
        return redirect('home')
    response = flickr.photos.search(
        user_id=config.flickr_username,
        tags=config.tags_to_show
    )
    import pdb; pdb.set_trace()
    context = dict(
        photos=response['photos']['photo']
    )
    return render(request, "floto/frame.html", context)


def config(request):
    config, created = Config.objects.get_or_create()
    if request.method == "POST":
        form = ConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ConfigForm(instance=config)
    context = dict(form=form)
    return render(request, "floto/config.html", context)


def flickr_oauth_callback(request):
    logging.info('We got a callback from Flickr, store the token')
    token = request.GET['oauth_token']
    store_oauth_token(token)
    logging.info('Saved new oauth token')
    return redirect('home')


def image_proxy(request, img_id):
    raise NotImplementedError()


