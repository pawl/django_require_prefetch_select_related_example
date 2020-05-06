from django.db import models
from django.db.models import Prefetch


class Artist(models.Model):
    name = models.CharField(max_length=100)


class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)


class PlaylistQuerySet(models.QuerySet):
    def eager_load_sorted_songs(self):
        """
        Sorts songs alphabetically by title and ensures all the related objects
        are eager loaded with select_related.

        Also a place to add the select_related/prefetch_related commonly used
        when displaying the items.
        """
        queryset = Song.objects \
            .select_related('artist') \
            .order_by('title')
        return self.prefetch_related(
            Prefetch(
                'songs',
                queryset=queryset,
                to_attr="sorted_songs",
            )
        )


class Playlist(models.Model):
    objects = PlaylistQuerySet.as_manager()

    title = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song)
