# STANDARD LIB
import json
import logging
import re
import StringIO
import urllib2

# LIBRARIES
from django.conf import settings
from django.core.files.base import File
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date as date_filter
from django.db import models

# FLOTO
from floto.constants import ALBUM_TITLE_TRUNCATIONS, PHOTO_TITLES_TO_IGNORE


class Album(models.Model):
    id = models.PositiveIntegerField(primary_key=True)  # prevent it being an AutoField
    title = models.CharField(max_length=255)
    ignore = models.BooleanField(
        default=False,
        help_text="Ignore this album for display purposes? E.g. for the 'Auto upload' album."
    )

    @property
    def title_display(self):
        title = self.title
        for regex in ALBUM_TITLE_TRUNCATIONS:
            title = re.sub(regex, u"", title)
        return title


class Photo(models.Model):
    id = models.PositiveIntegerField(primary_key=True) # prevent it being an AutoField
    title = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    rotation = models.PositiveIntegerField(default=0)
    url = models.URLField()
    date_taken = models.DateTimeField(blank=True, null=True)
    location = models.TextField(blank=True)
    albums = models.ManyToManyField(Album)
    cached_image = models.FileField(upload_to=settings.IMAGES_DIR, null=True)

    def cache_image(self, refresh=False):
        if self.cached_image and not refresh:
            logging.info("Not re-caching image %s as we already have it", self.pk)
            return
        image = urllib2.urlopen(self.url)
        name = "%s.jpg" % self.pk
        data = File(StringIO.StringIO(image.read()))
        self.cached_image.save(name, data)

    @property
    def serving_url(self):
        return reverse("image_proxy", kwargs={"photo_id": self.pk})

    @property
    def content_type(self):
        # Take a guess at the content type. Flicr doesn't seem to provide it when it serves the image.
        ext = self.url.rsplit('.', 1)[-1].lower()
        if ext in ('jpg', 'jpeg', 'png', 'gif', 'tiff'):
            return "image/%s" % ext
        return ""

    @property
    def location_display(self):
        """ Take the JSON of the location information and return a nicely formatted string
            describing the location.
        """
        location = json.loads(self.location)
        parts = ['country', 'city', 'neighborhood']
        result = u""
        for part in parts:
            part_string = location.get(part)
            if part_string:
                result += u"%s, " % part_string
        result.rstrip(u", ")
        return result

    @property
    def title_display(self):
        title = self.title
        for regex in PHOTO_TITLES_TO_IGNORE:
            if re.match(regex, title):
                return u""
        return title

    @property
    def primary_album_display(self):
        """ Get the display title of the first/most significat album this photo belongs to. """
        album = self.albums.filter(ignore=False).first()
        return album.title_display if album else u""

    @property
    def date_taken_display(self):
        # Python's standard strftime doesn't do the English ordinal suffix stuff, hence this
        if not self.date_taken:
            return u""
        return date_filter(self.date_taken, "dS N Y")

