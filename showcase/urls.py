from django.urls import path

from . import views
urlpatterns = [
  path('', views.FilmList.as_view()),
  path('<int:id>', views.FilmDetail.as_view()),
  path('<str:sort>', views.FilmSort.as_view()),
  
  path('<int:id>/<str:action>',views.FilmLikeDislike.as_view())
]