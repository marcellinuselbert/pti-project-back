from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Film
from .serializers import FilmAllSerializer
from rest_framework import filters,generics
from rest_framework import generics
from rest_framework import status

# Create your views here.

class FilmSearchFilter(generics.ListAPIView):

    serializer_class = FilmAllSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    

    def get_queryset(self):
        return Film.objects.all()

class FilmList(APIView):
    
    def get(self,request):
        if self.request.GET.get('sortby') == 'likes':
            Films = Film.objects.all().order_by("-like")
        elif self.request.GET.get('sortby') == 'dislikes':
            Films = Film.objects.all().order_by("-dislike")
        elif self.request.GET.get('sortby') == "year_ascending":
            Films = Film.objects.all().order_by("-released_year")
        elif self.request.GET.get('sortby') == "year_descending":
            Films = Film.objects.all().order_by("released_year")
        else :
            Films = Film.objects.all()
        
        serializers = FilmAllSerializer(Films, many=True)
        return Response({"status" : 200,
            "message" : "Success",
            "data":serializers.data})
            
    def post(self,request):

        film = Film.objects.all()      
        serializers = FilmAllSerializer(film, many=True)
        film_exist = False
        for data in serializers.data:
            if request.data['title'] == data['title'] and request.data['released_year'] == data['released_year']:
                film_exist=True
                break
            else:
                film_exist=False
            
        if not film_exist:
            film = Film.objects.create(
                title = request.data['title'],
                imageUrl = request.data['imageUrl'],
                trailerUrl = request.data['trailerUrl'],
                genre = request.data['genre'],
                released_year = request.data['released_year'],
            )
            serializers = FilmAllSerializer(film)
            return Response({"status" : 201,
        "message" : "Created",
        "data":serializers.data})

        else:
            return Response({
                "status" : 204,
        "message" : "Success no data, existed film"})
        

        
class FilmLikeDislike(APIView):

    # Like dengan method put/Update
    def put(self, request, pk, action):
        try :
            film = Film.objects.get(id=pk)

            if action == 'likes' :
                film.like += 1
        
            elif action == "dislikes":
                film.dislike += 1

            else:
                return Response({
                    "error": "hanya bisa like atau dislike"
                })
            film.save()

        except Film.DoesNotExist:
             return Response({
                "error" : "data film tidak ditemukan"
            })

        serializers = FilmAllSerializer(film)
        return Response({
            "status" : 201,
            "message" : "update successfull",
            "data" : serializers.data
        })

class FilmDetail(APIView):

    def get_object(self, pk):
        try:
            return Film.objects.get(pk=pk)
        except Film.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    # Like dengan method get
    def get(self, request, id):
        try :
            film = Film.objects.get(id=id)
    
            if self.request.GET.get('action') == 'likes' :
                film.like += 1

            elif self.request.GET.get('action') == 'dislikes':
                film.dislike += 1
                
            film.save()
            
            serializers = FilmAllSerializer(film)

        except Film.DoesNotExist :
            return Response({
                "error" : "data film tidak ditemukan"
            })
        return Response({
            "status" : 200,
            "message" : "GET Method film success",
            "data" : serializers.data
        })

    def delete(self, request, id) :
        try: 
            film = Film.objects.get(id=id)
            film.delete()

            return Response({
                "status" : 201,
                "message" : "delete success",
            })
        except Film.DoesNotExist:
            return Response({
                "error" : "film tidak ditemukan"
            })
#