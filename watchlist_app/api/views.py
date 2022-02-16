from django.forms import ValidationError
from watchlist_app.models import WatchList as WatchlistModel, StreamPlatForm, Review
from rest_framework.response import Response
from watchlist_app.api.serializers import ReviewSerializer, WatchListSerializer, StreamPlatFormSerializer
from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination
from django_filters.rest_framework import DjangoFilterBackend
# import django_filters.rest_framework

class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #To restrict Unauthenticated users from viewing the lists
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]


    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
        #The __username is to avoid the error Field 'id' expected a number but got 'demo'. due to the foreign key'review-user'

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


# A view for creating reviews
class ReviewCreate(generics.CreateAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    #A queryset to get all the reviews done to a specific movie
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchlistModel.objects.get(pk=pk)

        #A review queryset to filter whether a user has already reviewed a movie to prevent them from reviewing it twice
        review_user = self.request.user
        review_queryset  = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        # A queryset to raise a Validation Error if a user is reviewing a movie twice
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist, review_user=review_user)
        # return super().perform_create(serializer)

#A class for listing the reviews made on a movie and the user 
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #To restrict Unauthenticated users from viewing the lists
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 generics.GenericAPIView):

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatFormVS(viewsets.ModelViewSet):

    queryset = StreamPlatForm.objects.all()
    serializer_class = StreamPlatFormSerializer
    permission_classes = [IsAdminOrReadOnly]

# class StreamPlatFormVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatForm.objects.all()
#         serializer = StreamPlatFormSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatForm.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatFormSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatFormSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors) 

class StreamPlatFormListAV(APIView):
    #A class restricting normal users from editing contents
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        platform = StreamPlatForm.objects.all()
        serializer = StreamPlatFormSerializer(platform, many=True)
        return Response(serializer.data)
    
    def post(self, request): 
        serializer = StreamPlatFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class StreamPlatFormDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatForm.objects.get(pk=pk)
        except StreamPlatForm.DoesNotExist:
            return Response({"Error": 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatFormSerializer(platform)
        return Response(serializer.data)

    def put(self, request,pk):
        movie = StreamPlatForm.objects.get(pk=pk)
        serializer = StreamPlatFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
        
    def delete(self, request, pk):
        movie = StreamPlatForm.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class WatchListGV(generics.ListAPIView):
    queryset = WatchlistModel.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination
    #To restrict Unauthenticated users from viewing the lists
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    # search_fields = ['title', 'platform__name']
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']

class WatchListAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platform = WatchlistModel.objects.all()
        serializer = WatchListSerializer(platform, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchListDetailAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
            try:
                movie = WatchlistModel.objects.get(pk=pk)
            except WatchlistModel.DoesNotExist:
                return Response({"Error": 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = WatchListSerializer(movie)
            return Response(serializer.data)

    def put(self, request,pk):
        movie = WatchlistModel.objects.get(pk=pk)
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
        
    def delete(self, request, pk):
        movie = WatchlistModel.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
    
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({"Error": 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        


     