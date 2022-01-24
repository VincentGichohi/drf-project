from django.contrib import admin
from django.urls import path
from watchlist_app.api.views import movie_list, movie_details
# from . import views
urlpatterns = [
    path('list/', movie_list, name='movie-list,'),
    path('<int:pk>/', movie_details, name='movie-detail')
]