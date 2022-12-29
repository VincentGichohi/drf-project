from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.throttling import (AnonRateThrottle, ScopedRateThrottle,
                                       UserRateThrottle)
from rest_framework.views import APIView
from watchlist_app.api import pagination
from watchlist_app.api import permissions
from watchlist_app.api import serializers
from watchlist_app.api import throttling
from watchlist_app.models import Review, StreamPlatForm
from watchlist_app.models import WatchList as WatchlistModel


# import django_filters.rest_framework

class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


# A view for creating reviews
class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]

    # A queryset to get all the reviews done to a specific movie
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchlistModel.objects.get(pk=pk)

        # A review queryset to filter whether a user has already reviewed a movie to prevent them from reviewing it
        # twice
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        # A queryset to raise a Validation Error if a user is reviewing a movie twice
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)
        # return super().perform_create(serializer)


# A class for listing the reviews made on a movie and the user
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    # To restrict Unauthenticated users from viewing the lists
    # permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class StreamPlatFormVS(viewsets.ModelViewSet):
    queryset = StreamPlatForm.objects.all()
    serializer_class = serializers.StreamPlatFormSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class WatchListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        platform = WatchlistModel.objects.all()
        serializer = serializers.WatchListSerializer(platform, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchListDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchlistModel.objects.get(pk=pk)
        except WatchlistModel.DoesNotExist:
            return Response({"Error": 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchlistModel.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchlistModel.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
