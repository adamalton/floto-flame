# STANDARD LIB
import logging
import StringIO
import urllib2

# LIBRARIES
from django.conf import settings
from django.core.files.base import File
from django.core.urlresolvers import reverse
from django.db import models

# FLOTO
from floto.fields import JSONField


class Album(models.Model):
    id = models.PositiveIntegerField(primary_key=True)  # prevent it being an AutoField
    title = models.CharField(max_length=255)


class Photo(models.Model):
    id = models.PositiveIntegerField(primary_key=True) # prevent it being an AutoField
    title = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    rotation = models.PositiveIntegerField(default=0)
    url = models.URLField()
    date_taken = models.DateTimeField(blank=True, null=True)
    location = JSONField(blank=True, default=dict)
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

