import os

import requests
import urllib
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import parsers, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Photo, PhotoNoBackground
from .serializers import PhotoSerializer, PhotoNoBackgroundSerializer


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
        photo_with_background = urllib.request.urlretrieve(photo_url, "photo.jpg")
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={
                'image_file': open(photo_with_background[0], 'rb')
            },
            data={'size': 'auto'},
            headers={'X-Api-Key': 'jwVycxCPbofMG4FDLTjdRZpD'}
        )

        photo_with_background_path = os.path.abspath(photo_with_background[0])

        os.remove(photo_with_background_path)
        print("Deleted local file with background")
        if response.status_code == requests.codes.ok:
            photo_with_no_background = 'no-bg.png'
            with open(photo_with_no_background, 'wb') as out:
                out.write(response.content)
                out.close()
            # return photo_with_no_background

            photo_with_no_background_path = os.path.abspath(photo_with_no_background)

            photo_with_no_background_obj = open(photo_with_no_background_path, 'rb')

            instance_file = SimpleUploadedFile(photo_with_no_background_path, photo_with_no_background_obj.read())

            photo = PhotoNoBackground.objects.create(
                file=instance_file
            )

            os.remove(photo_with_no_background_path)
            print("Deleted local file with no background")

            serializer = PhotoNoBackgroundSerializer(photo, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # Delete the photo if no object cannot be identified from the it
            photo.delete()
            return Response({"details": response.text}, status=response.status_code)
