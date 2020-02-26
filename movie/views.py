from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from movie.models import *
from django.http import HttpResponse
import json
import math
import operator
import random

from movie.initializer import search_cache, search_index


def add_seen(request, movie_id):
    if request.is_ajax():
        history = Seen.objects.filter(movieid_id=movie_id, username=request.user.get_username())
        if len(history) == 0:
            movie = Popularity.objects.get(movieid_id=movie_id)
            weight = movie.weight
            movie.delete()
            new_record = Popularity(movieid_id=movie_id, weight=weight + 3)
            new_record.save()
            new_record = Seen(movieid_id=movie_id, username=request.user.get_username())
            new_record.save()
            return HttpResponse('1')
        else:
            history.delete()
            return HttpResponse('0')


def add_expect(request, movie_id):
    if request.is_ajax():
        history = Expect.objects.filter(movieid_id=movie_id, username=request.user.get_username())
        if len(history) == 0:
            movie = Popularity.objects.get(movieid_id=movie_id)
            weight = movie.weight
            movie.delete()
            new_record = Popularity(movieid_id=movie_id, weight=weight + 3)
            new_record.save()
            new_record = Expect(movieid_id=movie_id, username=request.user.get_username())
            new_record.save()
            return HttpResponse('2')
        else:
            history.delete()
            return HttpResponse('0')


@csrf_protect
def detail(request, model, id):
    items = []
    try:
        if model.get_name() == 'movie' and id != 'None':
            try:
                d = Popularity.objects.get(movieid_id=id)
                weight = d.weight
                d.delete()
                new_record = Popularity(movieid_id=id, weight=weight + 1)
                new_record.save()
            except:
                new_record = Popularity(movieid_id=id, weight=1)
                new_record.save()
            label = 'actor'
            object = model.objects.get(movieid=id)
            records = Act.objects.filter(movieid_id=id)
            if request.user.get_username() != '':
                seen_list = [str(x).split('|')[1] for x in
                             Seen.objects.filter(username=request.user.get_username())]
                expect_list = [str(y).split('|')[1] for y in
                               Expect.objects.filter(username=request.user.get_username())]
                if id in seen_list:
                    object.flag = 1
                if id in expect_list:
                    object.flag = 2
            for query in records:
                for actor in Actor.objects.filter(actorid=query.actorid_id):
                    items.append(actor)
        if model.get_name() == 'actor':
            label = 'movie'
            object = model.objects.get(actorid=id)
            records = Act.objects.filter(actorid_id=id)
            for query in records:
                for movie in Movie.objects.filter(movieid=query.movieid_id):
                    items.append(movie)
    except:
        return render(request, '404.html')
    return render(request, '{}_list.html'.format(label), {'items': items, 'number': len(items), 'object': object})


def whole_list(request, model, page):
    if page is None:
        return render(request, '404.html')
    page = int(page)
    objects = model.objects.all()
    total_page = int(math.ceil(len(objects) / 15))
    if page > total_page:
        return render(request, '404.html')
    last_item_index = 15 * page if page != total_page else len(objects)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - 15 + end_distance
    end_page_num = page + 5 if page > 5 else 15
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    data = {'items': objects[15 * (page - 1):last_item_index], 'current_page': page, 'page_number': total_page,
            'pages': pages}
    return render(request, '{}_list.html'.format(model.get_name()), data)


def search(request, item, query_string, page):
    if item is None or query_string is None or page is None:
        return render(request, '404.html')
    query_string = query_string.replace("%20", " ")
    if item == 'movie':
        result = [search_index.data_in_memory['movie_dict'][movie_id] for movie_id in
                  search_index.search_movie(query_string)]
    elif item == 'actor':
        result = [search_index.data_in_memory['actor_dict'][actor_id] for actor_id in
                  search_index.search_actor(query_string)]
    else:
        return render(request, '404.html')
    page = int(page)
    total_page = int(math.ceil(len(result) / 15))
    if page > total_page and total_page != 0:
        return render(request, '404.html')
    last_item_index = 15 * page if page != total_page else len(result)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - 15 + end_distance
    end_page_num = page + 5 if page > 5 else 15
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    return render(request, item + '_search.html',
                  {'items': result[15 * (page - 1):last_item_index], 'length': len(result),
                   'query_string': query_string, 'current_page': page, 'page_number': total_page, 'pages': pages})


def search_suggest(request, query_string):
    result = search_cache.get(query_string)
    if result is not None:
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    movie_list, actor_list = [], []
    search_result = search_index.search_suggest(query_string)
    for i, movie_id in enumerate(search_result[0]):
        movie = search_index.data_in_memory['movie_dict'].get(movie_id)
        movie_list.append({'movieid': movie.movieid, 'poster': movie.poster, 'title': movie.title})
        if i == 2:
            break
    for i, actor_id in enumerate(search_result[1]):
        actor = search_index.data_in_memory['actor_dict'].get(actor_id)
        actor_list.append({'actorid': actor.actorid, 'photo': actor.photo, 'name': actor.name})
        if i == 2:
            break
    result = {'movie': movie_list, 'actor': actor_list, 'text': query_string}
    search_cache.set(query_string, result)
    return HttpResponse(json.dumps(result, ensure_ascii=False))


@csrf_protect
def seen(request, movie_id):
    if request.POST:
        try:
            d = Seen.objects.get(username=request.user.get_username(), movieid_id=movie_id)
            d.delete()
        except:
            return render(request, '404.html')
    records = Seen.objects.filter(username=request.user.get_username())
    movies = []
    for record in records:
        movie_id = str(record).split('|')[1]
        movies.append(Movie.objects.get(movieid=movie_id))
    return render(request, 'seen.html', {'items': movies, 'number': len(movies)})


def expect(request, movie_id):
    if request.POST:
        try:
            d = Expect.objects.get(username=request.user.get_username(), movieid_id=movie_id)
            d.delete()
        except:
            return render(request, '404.html')
    records = Expect.objects.filter(username=request.user.get_username())
    movies = []
    for record in records:
        movie_id = str(record).split('|')[1]
        movies.append(Movie.objects.get(movieid=movie_id))
    return render(request, 'expect.html', {'items': movies, 'number': len(movies)})


@csrf_protect
def recommendation(request, movie_id):
    data = {}
    movie_dict = search_index.data_in_memory['movie_dict']
    if request.user.is_authenticated:
        data = {'username': request.user.get_username()}
    popular_movies = Popularity.objects.all().order_by('-weight')
    popular = []
    for movie in popular_movies[:5]:
        try:
            popular.append({'movieid': movie.movieid_id, 'poster': movie_dict[movie.movieid_id].poster})
        except:
            continue
    data['popular'] = popular
    popular_movie_list = [movie_dict[movie.movieid_id] for movie in popular_movies[:5]]
    data['recommendation'] = get_recommendation(request, popular_movie_list)
    return render(request, 'recommendation.html', data)


def get_recommendation(request, popular_movie_list):
    result = []
    movie_dict = search_index.data_in_memory['movie_dict']
    added_movie_list = []
    if request.user.is_authenticated:
        username = request.user.get_username()
        # block + ctrl + /
        # watched_movies = set([movie_dict[movie.movieid_id] for movie in Seen.objects.filter(username=username)] +
        #                      [movie_dict[movie.movieid_id] for movie in Expect.objects.filter(username=username)])
        
        # if Seen.objects.filter(username=username) is None:
        # #     Seen.object.filter(username=username) = None
        #     return render(request, 'base.html')
        
        # try:
        #     d = set([movie_dict[movie.movieid_id] for movie in Seen.objects.filter(username=username)])
        #     d.delete()
        # except:
        #     return render(request, '404.html')


        watched_movies = set([movie_dict[movie.movieid_id] for movie in Seen.objects.filter(username=username)])
        #if len(result) == 0:
        #    return render(request, '404.html')
        unwatched_movies = set(search_index.data_in_memory['movie_list']) - watched_movies - set(popular_movie_list)
        genre_stats = {}
        for movie in watched_movies:
            for genre in movie.genres.split('|'):
                genre_stats[genre] = genre_stats.get(genre, 0) + 1
        movie_score = {}
        for movie in unwatched_movies:
            movie_score[movie.movieid] = movie.rate
            for genre in movie.genres.split('|'):
                movie_score[movie.movieid] += genre_stats.get(genre, 0) / len(watched_movies)

        sorted_list = sorted(movie_score.items(), key=operator.itemgetter(1), reverse=True)
        for item in sorted_list:
            movie = movie_dict[item[0]]
            result.append({'movieid': movie.movieid, 'poster': movie.poster})
            added_movie_list.append(movie)
            if len(result) == 8:
                break
        sorted_list = sorted(search_index.data_in_memory['movie_rating'].items(), key=operator.itemgetter(1), reverse=True)
        for item in sorted_list:
            movie = movie_dict[item[0]]
            if movie not in popular_movie_list and movie not in added_movie_list:
                result.append({'movieid': movie.movieid, 'poster': movie.poster})
            if len(result) == 10:
                break
        return [result[i] for i in random.sample(range(len(result)), 5)]
    
def aboutus(request):
    return render(request, 'aboutus.html')

def genre_select(request):
    return render(request, 'genre_select.html')