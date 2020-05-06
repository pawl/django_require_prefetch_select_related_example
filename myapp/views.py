from django.http import HttpResponse

from . import models


def index(request):
    for playlist in models.Playlist.objects.eager_load_sorted_songs().all():
        for song in playlist.sorted_songs:
            print(song.artist.name)

    return HttpResponse('success', status=200)
