from django.db import models
from django.contrib.postgres.fields import ArrayField


class Channel(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=500)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'yt_channels'

    def __str__(self):
        return self.name

class Video(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    publishedAt = models.DateTimeField(null=True,blank=True)
    thumbnails = ArrayField(models.URLField(null=True,blank=True),null=True,blank=True)

    class Meta:
        db_table = 'yt_videos'


    def __str__(self):
        return self.title


class ApiKey(models.Model):
    is_exhausted = models.BooleanField(default=False)
    key = models.CharField(max_length=128)
    last_used = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table = 'yt_api_keys'

    def __str__(self):
        return self.key

class Query(models.Model):
    query = models.CharField(max_length=150)
    
    class Meta:
        db_table = 'yt_queries'

    def __str__(self):
        return self.query

