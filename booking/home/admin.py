from django.contrib import admin

# Register your models here.
from home.models import Movie, Showtime, Booking

[admin.site.register(model) for model in [Movie, Showtime, Booking]]