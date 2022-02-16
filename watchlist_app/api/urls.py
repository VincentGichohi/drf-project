from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import movie_list, movie_details, 
from watchlist_app.api.views import ReviewList, WatchListGV, ReviewDetail,UserReview, ReviewCreate, WatchListAV, WatchListDetailAV, StreamPlatFormListAV, StreamPlatFormDetailAV, StreamPlatFormVS
# from . import views

router = DefaultRouter()
router.register('stream', StreamPlatFormVS, basename='streamplatform')


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list,'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name='movie-detail'),
    path('list2/', WatchListGV.as_view(), name='watch-list'),

    # path('stream/', StreamPlatFormListAV.as_view(), name='stream'),
    # path('stream/<int:pk>/', StreamPlatFormDetailAV.as_view(), name='stream-detail'),
    path('', include(router.urls)),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    # path('review/', ReviewList.as_view(), name='review-list')

    path('<int:pk>/review-create', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('review/', UserReview.as_view(), name='user-review-detail'),



]