from rest_framework import serializers

from .models import Exhibition, ExhibitionPhoto, ExhibitionReview


class ExhibitionPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='image_src', read_only=True)

    class Meta:
        model = ExhibitionPhoto
        fields = [
            'id',
            'exhibition',
            'image_path',
            'image_url',
            'caption',
            'position',
        ]


class ExhibitionSerializer(serializers.ModelSerializer):
    curator_username = serializers.SerializerMethodField()
    photos_count = serializers.IntegerField(read_only=True)
    cover_photo_url = serializers.SerializerMethodField()
    photos = ExhibitionPhotoSerializer(many=True, read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Exhibition
        fields = [
            'id',
            'curator',
            'curator_username',
            'title',
            'description',
            'is_published',
            'photos_count',
            'cover_photo_url',
            'photos',
            'reviews_count',
        ]

    def get_curator_username(self, obj):
        if obj.curator:
            return obj.curator.username

        return None

    def get_cover_photo_url(self, obj):
        cover = obj.cover_photo

        if cover:
            return cover.image_src

        return None

    def get_reviews_count(self, obj):
        return obj.reviews.filter(is_visible=True).count()


class ExhibitionReviewSerializer(serializers.ModelSerializer):
    exhibition_title = serializers.CharField(source='exhibition.title', read_only=True)
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = ExhibitionReview
        fields = [
            'id',
            'exhibition',
            'exhibition_title',
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