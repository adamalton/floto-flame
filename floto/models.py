from django.db import models
from django.utils.safestring import mark_safe


class Config(models.Model):
    flickr_username = models.CharField(max_length=100, help_text="E.g. 73509078@N00")
    api_key = models.CharField(max_length=100, verbose_name="API key")
    secret = models.CharField(
        max_length=100,
        help_text=mark_safe(
            'You can get these from '
            '<a href="https://www.flickr.com/services/apps/create/apply/">'
            'here</a>'
        )
    )
    tags_to_show = models.CharField(
        max_length=200,
        help_text="Comma-separated list of tags which mark the photos that you want to show",
    )
    max_cache_size = models.PositiveIntegerField(
        verbose_name="Maximum disk space to use for local photo cache (MB)",
        help_text="The cache prevents re-fetching of photos, so helps reduce bandwidth usage",
        default=5000000, # 5 GB
    )



class Photo(models.Model):
    id = models.PositiveIntegerField(primary_key=True) # prevent it being an AutoField
    rotation = models.SmallPositiveIntegerField()
    url = models.URLField()

