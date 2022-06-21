from django.contrib import admin
from Movie.models import *

# Register your models here.

admin.site.register(Movie)
admin.site.register(Rating)