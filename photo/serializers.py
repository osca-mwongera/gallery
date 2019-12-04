from rest_framework import serializers
from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    # file = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'name', 'file']

    def get_file(self, obj):
        request = self.context.get('request')
        file = obj.file.url
        return request.build_absolute_uri(file)
