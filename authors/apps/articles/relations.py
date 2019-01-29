import re
from rest_framework import serializers
from django.utils.text import slugify

from authors.apps.articles.models import Tag


class TagRelation(serializers.RelatedField):
    """
    This class overwrites the serializer class for tags
    to enable tags to be saved on a separate table when
    creating an article
    """

    def get_queryset(self):
        return Tag.objects.all()

    def to_representation(self, value):
        return value.tag

    def to_internal_value(self, data):
        # Ensure tags with caps and spaces are saved as slugs
        # caps and lowercase are saved as one
        if not re.match(r'^[a-zA-Z0-9][ A-Za-z0-9_-]*$', data):
            raise serializers.ValidationError(
                'Tag cannot have special characters')
        new_tag = slugify(data)
        tag, created = Tag.objects.get_or_create(tag=new_tag)
        return tag
