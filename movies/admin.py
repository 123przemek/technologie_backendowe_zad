from django.contrib import admin
from movies.models import Actor, Movie, Country, Oscar

# Register your models here.

admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Country)
admin.site.register(Oscar)
