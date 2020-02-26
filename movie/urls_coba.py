from django.conf.urls import patterns, include, url
from . import views
from . import models
from django.contrib import admin

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Movery import settings

#from django.urls import include, path
urlpatterns = [
    url(r'^movie_all/(?P<page>\d*)', views.whole_list, {'model': models.Movie}, name='whole_list'),
    url(r'^actor_all/(?P<page>\d*)', views.whole_list, {'model': models.Actor}, name='whole_list'),
    url(r'^movie_detail/(?P<id>.*)', views.detail, {'model': models.Movie}, name='movie_detail'),
    url(r'^actor_detail/(?P<id>.*)', views.detail, {'model': models.Actor}, name='actor_detail'),
    url(r'^search/(?P<item>.*)/(?P<query_string>.*)/(?P<page>\d*).*', views.search, name='search'),
    url(r'^seen/(?P<movie_id>.*)', views.seen, name='seen'),
    url(r'^add_seen/(?P<movie_id>.*)', views.add_seen, name='seen'),
    url(r'^expect/(?P<movie_id>.*)', views.expect, name='expect'),
    url(r'^add_expect/(?P<movie_id>.*)', views.add_expect, name='expect'),
    url(r'^search_suggest/(?P<query_string>.*)', views.search_suggest, name='search_suggest'),
    url(r'^recommendation/(?P<movie_id>.*)', views.recommendation, name='recommendation'),

    urlpatterns=patterns('')+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns+=staticfiles_urlpatterns()

    #url(r'^admin/', admin.site.urls),
]
