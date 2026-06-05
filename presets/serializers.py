from rest_framework import serializers

from .models import Preset, PresetReview


class PresetSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    image_url = serializers.CharField(source='image_src', read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Preset
        fields = [
            'id',
            'author',
            'author_username',
            'title',
            'tone',
            'description',
            'intensity',
            'image_path',
            'image_url',
            'is_public',
            'reviews_count',
        ]

    def get_author_username(self, obj):
        if obj.author:
            return obj.author.username

        return None

    def get_reviews_count(self, obj):
        return obj.reviews.filter(is_visible=True).count()


class PresetReviewSerializer(serializers.ModelSerializer):
    preset_title = serializers.CharField(source='preset.title', read_only=True)
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = PresetReview
        fields = [
            'id',
            'preset',
            'preset_title',
            'author',
            'author_username',
            'author_name',
            'text',
            'rating',
            'created_at',
            'is_visible',
        ]

    def get_author_username(self, obj):
        if obj.author:
            return obj.author.username

        return obj.author_name