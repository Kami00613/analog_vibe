from rest_framework import serializers

from .models import Camera, CameraBrand, CameraReview


class CameraBrandSerializer(serializers.ModelSerializer):
    cameras_count = serializers.SerializerMethodField()

    class Meta:
        model = CameraBrand
        fields = [
            'id',
            'name',
            'country',
            'cameras_count',
        ]

    def get_cameras_count(self, obj):
        return obj.cameras.count()


class CameraSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand_country = serializers.CharField(source='brand.country', read_only=True)
    owner_username = serializers.SerializerMethodField()
    image_url = serializers.CharField(source='image_src', read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = [
            'id',
            'owner',
            'owner_username',
            'brand',
            'brand_name',
            'brand_country',
            'name',
            'year',
            'description',
            'image_path',
            'image_url',
            'is_working',
            'is_rare',
            'reviews_count',
        ]

    def get_owner_username(self, obj):
        if obj.owner:
            return obj.owner.username

        return None

    def get_reviews_count(self, obj):
        return obj.reviews.filter(is_visible=True).count()


class CameraReviewSerializer(serializers.ModelSerializer):
    camera_name = serializers.CharField(source='camera.name', read_only=True)
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = CameraReview
        fields = [
            'id',
            'camera',
            'camera_name',
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