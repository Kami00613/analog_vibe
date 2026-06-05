from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    cameras_count = serializers.SerializerMethodField()
    presets_count = serializers.SerializerMethodField()
    exhibitions_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'email',
            'nickname',
            'bio',
            'favorite_style',
            'phone',
            'cameras_count',
            'presets_count',
            'exhibitions_count',
        ]

    def get_cameras_count(self, obj):
        return obj.user.cameras.count()

    def get_presets_count(self, obj):
        return obj.user.presets.count()

    def get_exhibitions_count(self, obj):
        return obj.user.exhibitions.count()