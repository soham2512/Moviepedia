from io import BytesIO

import requests
from django.core import files
from django.db import models


class Rating(models.Model):
    source = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)

    def __str__(self):
        return self.source + " - " + self.rating


class Movie(models.Model):
    Title = models.CharField(max_length=200)
    Year = models.CharField(max_length=25, blank=True)
    Rated = models.CharField(max_length=10, blank=True)
    Released = models.CharField(max_length=25, blank=True)
    Runtime = models.CharField(max_length=25, blank=True)
    Genre = models.CharField(max_length=25, blank=True)
    Director = models.CharField(max_length=100, blank=True)
    Writer = models.CharField(max_length=300, blank=True)
    Actors = models.CharField(max_length=25, blank=True)
    Plot = models.CharField(max_length=900, blank=True)
    Language = models.CharField(max_length=300, blank=True)
    Country = models.CharField(max_length=100, blank=True)
    Awards = models.CharField(max_length=250, blank=True)
    Poster = models.ImageField(upload_to='static/movie', blank=True)
    Poster_url = models.URLField(blank=True)
    Ratings = models.ManyToManyField(Rating, blank=True)
    imdbRating = models.CharField(max_length=5, blank=True)
    imdbID = models.CharField(max_length=100, blank=True)
    Type = models.CharField(max_length=10, blank=True)
    totalSeasons = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.Title

    def save(self, *args, **kwargs):
        if self.Poster == '' and self.Poster_url != '':
            resp = requests.get(self.Poster_url)
            pb = BytesIO()
            pb.write(resp.content)
            pb.flush()
            file_name = self.Poster_url.split("/")[-1]
            self.Poster.save(file_name, files.File(pb), save=False)

        return super().save(*args, **kwargs)
