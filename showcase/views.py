from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Film
from .serializers import FilmAllSerializer, FilmDetailSerializer
from rest_framework import filters, generics
import collections

# Create your views here.
class FilmList(APIView):
    def get(self, request):

        film = Film.objects.all()
        sort = request.GET.get("sort", None)
        
  
        if sort == 'likes':
            film = Film.objects.all().order_by("genre")
            # print(serializers.data)
        elif sort == 'dislikes':
            film = Film.objects.all().order_by("genre")
            film = Film.objects.all().order_by("-dislike")
        elif sort == "year_ascending":
            film = Film.objects.all().order_by("released_year")
            # print(serializers.data)
        elif sort == "year_descending":
            film = Film.objects.all().order_by("-released_year")

        serializers = FilmAllSerializer(film, many=True)

        if sort == 'likes' or sort == "dislikes":
            # grouping film in genre
            list_of_films = []
            top_films = []
            dict_top_films={}
            list_top_genre= []
            list_final= []
            result = collections.defaultdict(list)
            for new_dict in serializers.data:
                result[new_dict['genre']].append(new_dict)
            
            for genre,movie in result.items():
                if sort == "likes":
                    res = sorted(movie, key=lambda movie: movie["like"], reverse=True)
                elif sort == "dislikes":
                    res = sorted(movie, key=lambda movie: movie["dislike"], reverse=True)
                dict_top_films[genre]=res
                list_of_films.append(res)

            for grouped_sorted_film in list_of_films:
                top_films.append(grouped_sorted_film[0])
                
                if sort == "likes":
                    res_top_film = sorted(top_films, key=lambda top_films: top_films["like"], reverse=True)
                elif sort == "dislikes":
                    res_top_film = sorted(top_films, key=lambda top_films: top_films["dislike"], reverse=True)
            
            for sorted_film in res_top_film:
                list_top_genre.append(sorted_film['genre'])

            
            for genre in list_top_genre:
                list_final.extend(dict_top_films[genre])

        data=serializers.data
        if sort=="likes" or sort=="dislikes":
            data=list_final
        return Response({
            "status": 200,
            "message": "Success",
            "data": data
        })

    def post(self, request):

        film = Film.objects.all()
        serializers = FilmAllSerializer(film, many=True)
        film_exist = False
        for data in serializers.data:
            if request.data['title'] == data['title'] and request.data[
                    'released_year'] == data['released_year']:
                film_exist = True
                break
            else:
                film_exist = False

        if not film_exist:
            film = Film.objects.create(
                title=request.data['title'],
                imageUrl=request.data['imageUrl'],
                trailerUrl=request.data['trailerUrl'],
                genre=request.data['genre'],
                released_year=request.data['released_year'],
            )
            serializers = FilmDetailSerializer(film)
            return Response({
                "status": 201,
                "message": "Created",
                "data": serializers.data
            })

        else:
            return Response({
                "status": 204,
                "message": "Success no data, existed film"
            })
    

class FilmSearchFilter(generics.ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmAllSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class FilmLikeDislike(APIView):
    def put(self, request, id, action):
        try:
            film = Film.objects.get(id=id)
            if action == "like":
                film.like += 1
            elif action == "dislike":
                film.dislike += 1
            else:
                return Response({"error": "hanya bisa like atau dislike"})
            film.save()
        except Film.DoesNotExist:
            return Response({"error": "film tidak ditemukan"})

        serializers = FilmDetailSerializer(film)
        return Response({
            "status": 201,
            "message": "update successfull",
            "data": serializers.data
        })


class FilmDetail(APIView):
    def get(self, request, id):
        #TODO Implement get by title
        try:
            film = Film.objects.get(id=id)
            serializers = FilmDetailSerializer(film)
        except Film.DoesNotExist:
            return Response({"error": "film tidak ditemukan"})
        return Response({
            "status": 200,
            "message": "get film success",
            "data": serializers.data
        })

    def delete(self, request, id):
        try:

            film = Film.objects.get(id=id)
            film.delete()

            return Response({
                "status": 201,
                "message": "delete success",
            })
        except Film.DoesNotExist:
            return Response({"error": "film tidak ditemukan"})
