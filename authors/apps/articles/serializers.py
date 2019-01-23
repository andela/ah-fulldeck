from rest_framework import serializers

from .models import Article, Comment
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


class CommentsSerializers(serializers.ModelSerializer):
    body = serializers.CharField(
        max_length=200,
        required=True,
        error_messages={
            'required': 'Comments field cannot be blank'
        }
    )

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

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_at', 'updated_at',
                  'author', 'article', 'parent')
