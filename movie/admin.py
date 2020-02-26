from django.contrib import admin
from django.contrib import auth
from movie.models import *
#from .models import Movie, Actor

class MovieAdmin(admin.ModelAdmin):
    list_display = ('movieid', 'title', 'genres', 'rate')


class ActorAdmin(admin.ModelAdmin):
    list_display = ('actorid', 'name')

admin.site.unregister(auth.models.Group)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor, ActorAdmin)
