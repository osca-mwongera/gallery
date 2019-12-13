from rest_framework import serializers
from .models import Photo, PhotoNoBackground


class PhotoSerializer(serializers.ModelSerializer):
    # file = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'file']

    def get_file(self, obj):
        request = self.context.get('request')
        file = obj.file.url
        return request.build_absolute_uri(file)


class PhotoNoBackgroundSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoNoBackground
        fields = ['id', 'file']

    def get_file(self, obj):
        request = self.context.get('request')
        file = obj.file.url
        return request.build_absolute_uri(file)
