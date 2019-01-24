from rest_framework import serializers

from .models import Article, Comment, LikeDislike, ArticleRatings
from django.db.models import Avg
from collections import Counter
from rest_framework.validators import UniqueValidator
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
    avg_rating = serializers.SerializerMethodField(
        method_name='average_rating')
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
            'avg_rating',
            'image_url',
            'author',
            'created_at',
            'updated_at'
        )

    def average_rating(self, instance):
        avg_rating = ArticleRatings.objects.filter(article=instance).aggregate(
            average_rating=Avg('rating'))['average_rating'] or 0
        avg_rating = round(avg_rating)
        total_user_rates = ArticleRatings.objects.filter(
            article=instance).count()
        each_rating = Counter(ArticleRatings.objects.filter(
            article=instance).values_list('rating', flat=True))

        return {
            'avg_rating': avg_rating,
            'total_user_rates': total_user_rates,
            'each_rating': each_rating
        }


class CommentsSerializers(serializers.ModelSerializer):
    body = serializers.CharField(
        max_length=200,
        required=True,
        error_messages={
            'required': 'Comments field cannot be blank'
        }
    )

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_at', 'updated_at',
                  'author', 'article', 'parent')

    def format_date(self, date):
        return date.strftime('%d %b %Y %H:%M:%S')

    def to_representation(self, instance):
        """
        overide representation for custom output
        """
        threads = [
            {

                'id': thread.id,
                'body': thread.body,
                'author': thread.author.username,
                'created_at': self.format_date(thread.created_at),
                'replies': thread.threads.count(),
                'updated_at': self.format_date(thread.updated_at)
            } for thread in instance.threads.all()
        ]

        representation = super(CommentsSerializers,
                               self).to_representation(instance)
        representation['created_at'] = self.format_date(instance.created_at)
        representation['updated_at'] = self.format_date(instance.updated_at)
        representation['author'] = instance.author.username
        representation['article'] = instance.article.title
        representation['reply_count'] = instance.threads.count()
        representation['threads'] = threads
        del representation['parent']

        return representation


class RatingSerializer(serializers.ModelSerializer):
    """
    create and update existing ratings for our articles
    """
    rating = serializers.IntegerField(required=True)

    class Meta:
        model = ArticleRatings
        fields = ['rating', 'rated_by']
        read_only_fields = ['rated_by']
        

class LikeDislikeSerializer(serializers.Serializer):
    """
    serializer class for the Like Dislike model
    """
    class Meta:
        model = LikeDislike

    def create(self, validated_data):
        rating = ArticleRatings.objects.create(**validated_data)

        return rating

    def validate(self, data):
        """
        ensure the ratings are between 1 and 5
        """
        rating = data.get('rating')

        if rating:
            if rating < 1 or rating > 5:
                raise serializers.ValidationError(
                    "Rating should be a number between 1 and 5")
        return {'rating': rating}
