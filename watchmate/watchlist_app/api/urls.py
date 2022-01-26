from django.contrib import admin
from django.urls import path
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import WatchListAV, WatchListDetailAV, StreamPlatFormListAV, StreamPlatFormDetailAV
# from . import views

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list,'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name='movie-detail'),
    path('stream/', StreamPlatFormListAV.as_view(), name='stream'),
    path('stream/<int:pk>/', StreamPlatFormDetailAV.as_view(), name='stream-detail')
]