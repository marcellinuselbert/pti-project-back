from django.urls import path
from .views import *

app_name = 'showcase'

urlpatterns = [
  path('', FilmList.as_view()),
  path('<int:id>', FilmDetail.as_view(), name='detail'),
  path('<int:pk>/<str:action>',FilmLikeDislike.as_view()),
  path('search',FilmSearchFilter.as_view())
]