from removebg import RemoveBg
from rest_framework import viewsets, parsers, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Photo
from .serializers import PhotoSerializer
import requests


# Create your views here.

class PhotoUploadView(generics.CreateAPIView):
    model = Photo
    serializer_class = PhotoSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoListView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (parsers.FileUploadParser,)


class PhotoDetail(APIView):

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            return Response({"details": "Photo does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo, context={'request': request})
        return Response(serializer.data)


class DeletePhoto(APIView):

    def get_object(self, pk):
        try:
            photo = Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            return Response({"details": "Photo does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        photo = self.get_object(pk)
        photo.delete()
        return Response({"detail": "Photo deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PhotoRemoveBG(APIView):

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            return Response({"details": "Photo does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo, context={'request': request})
        photo_url = (serializer.data['file'])
        rmbg = RemoveBg("jwVycxCPbofMG4FDLTjdRZpD", "error.log")
        response = rmbg.remove_background_from_img_url(img_url=photo_url, size="regular", new_file_name="empty_bg.png")
        print(response)
        return Response(serializer.data, status=status.HTTP_200_OK)
