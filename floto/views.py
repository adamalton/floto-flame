# LIBRARIES
from django.shortcuts import render, redirect

# FLOTO
from floto.forms import ConfigForm
from floto.models import Config


def home(request):
    if not Config.objects.exists():
        # No settings yet, just redirect to the config page
        return redirect("config")
    return render(request, "floto/home.html", {})


def frame(request):
    return render(request, "floto/frame.html", {})


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


def image_proxy(request, img_id):
    raise NotImplementedError()
