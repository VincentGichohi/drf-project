from watchlist_app.models import WatchList, StreamPlatForm
from rest_framework.response import Response
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatFormSerializer
from rest_framework.views import APIView  
from rest_framework import status

class StreamPlatFormListAV(APIView):
    
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
    
    def get(self, request, pk):
        try:
            movie = StreamPlatForm.objects.get(pk=pk)
        except StreamPlatForm.DoesNotExist:
            return Response({"Error": 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatFormSerializer(movie)
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
    
    
class WatchListAV(APIView):
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchListDetailAV(APIView):
    
    def get(self, request, pk):
            try:
                movie = WatchList.objects.get(pk=pk)
            except WatchList.DoesNotExist:
                return Response({"Error": 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = WatchListSerializer(movie)
            return Response(serializer.data)

    def put(self, request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        


     