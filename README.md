In this repository, I try to figure out the best way to require prefech_related/select_related when fetching a model's related objects. I also want to figure out a good pattern for avoiding duplicated prefetch_related/select_related for multiple places in a codebase that need the related objects eager loaded in the same way.

## Solution

The main idea is to make a custom QuerySet method that does the prefetch_related/select_related and whatever special ways you need to load the related objects. I also use Prefetch's `to_attr` to store the related objects by a different name, so you'll get an error when you try to use it without the eager loading.

The QuerySet:
```python
class PlaylistQuerySet(models.QuerySet):
    def eager_load_sorted_songs(self):
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
```

The View:
```python
for playlist in models.Playlist.objects.eager_load_sorted_songs().all():
    for song in playlist.sorted_songs:
        print(song.artist.name)

for playlist in models.Playlist.objects.all():
    for song in playlist.sorted_songs:
        # Oops, you forgot to use the eager loading method
        # AttributeError: 'Playlist' object has no attribute 'sorted_songs'
        print(song.artist.name)
```

The full example is in this repo.

## Caveats

One issue with doing things this way: it doesn't mix well with code that already has the objects prefetched normally. You'll end up prefetching a 2nd time.

Also, you may end up throwing unexpected fatal exceptions if you don't have test coverage where you implement this.

## Alternatives

* Maybe it's better to do this check only during testing. There's a library called nplusone for that: https://github.com/jmcarp/nplusone
* Or a decorator that checks for prefetching, like these:
    * https://github.com/WhatsMyCut/wmcp-django-api/blob/6bd167830e5c534dd9ed551507e01092f574a66a/apps/general/decorators.py#L22-L28
    * https://github.com/kosz85/django-prefetch-decorator

## Installation

1. Clone this repository and navigate to the directory.
1. Create virtualenv: `virtualenv .venv`
1. Activate the virtualenv: `source .venv/bin/activate`
1. Install dependencies: `pip install -r requirements.txt`
1. Initialize database schema: `python manage.py migrate`
1. Load initial data: `python manage.py loaddata myapp/fixtures/*`

## Usage

Run: `python manage.py runserver`

Visit: http://localhost:8000/
