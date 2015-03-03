from django import forms

# Floto
from floto.models import Config


class ConfigForm(forms.ModelForm):

    class Meta(object):
        model = Config
