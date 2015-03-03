from django.db import models
from django.utils.safestring import mark_safe


class Config(models.Model):
    flickr_username = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100, verbose_name="API key")
    secret = models.CharField(
        max_length=100,
        help_text=mark_safe(
            'You can get these from '
            '<a href="https://www.flickr.com/services/apps/create/apply/">'
            'here</a>'
        )
    )
    max_cache_size = models.PositiveIntegerField(
        verbose_name="Maximum disk space to use for local photo cache (MB)",
        help_text="The cache prevents re-fetching of photos, so helps reduce bandwidth usage",
        default=5000000, # 5 GB
    )

