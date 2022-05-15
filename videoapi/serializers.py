from rest_framework import serializers
from videoapi.models import Video, ApiKey, Query



class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"
        