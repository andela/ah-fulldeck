from rest_framework import serializers

from .models import Article
from authors.apps.profiles.serializers import ProfileSerializer
from authors.apps.profiles.models import Profile


class ArticleSerializers(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        max_length=140,
        error_messages={
            'required': 'Title is required',
            'max_length': 'Title cannot be more than 140'
        }
    )
    description = serializers.CharField(
        required=False,
        max_length=250,
        error_messages={
            'max_length': 'Description cannot be more than 250'
        }
    )
    image_url = serializers.URLField(
        required=False
    )
    body = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Body cannot be empty'
        }
    )

    author = serializers.SerializerMethodField(read_only=True)

    slug = serializers.CharField(read_only=True)

    def get_author(self, obj):
        """This method gets the profile object for the article"""
        serializer = ProfileSerializer(
            instance=Profile.objects.get(user=obj.author))
        return serializer.data

    class Meta:
        model = Article
        fields = (
            'title',
            'description',
            'body',
            'slug',
            'image_url',
            'author',
            'created_at',
            'updated_at'
        )
