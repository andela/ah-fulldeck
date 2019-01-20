from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Article
from .serializers import ArticleSerializers
from .renderers import ArticleJsonRenderer
from .permissions import IsOwnerOrReadonly


def article_not_found():
    raise ValidationError(
        detail={'error': 'No article found for the slug given'})


class ListCreateArticle(ListCreateAPIView):
    queryset = Article.objects.all()
    renderer_classes = (ArticleJsonRenderer,)
    serializer_class = ArticleSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        article = request.data.get('article', {})
        serializer = self.serializer_class(
            data=article, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDeleteArticle(RetrieveUpdateDestroyAPIView):
    """
    This class retrieves, updates, and deletes a single article
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
    renderer_classes = (ArticleJsonRenderer,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)
    lookup_field = 'slug'

    def get_single_article(self, slug):
        """
        This method returns an article with the slug provided
        """
        article = Article.objects.filter(slug=slug).first()
        return article

    def get(self, request, slug):
        article = self.get_single_article(slug)
        if not article:
            article_not_found()
        return super().get(request, slug)

    def update(self, request, slug):
        """
        This method updates an article
        """
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            article_not_found()
            return Response(status=status.HTTP_404_NOT_FOUND)
        article_data = request.data.get('article', {})
        serializer = self.serializer_class(
            article, data=article_data, partial=True)
        if serializer.is_valid():
            self.check_object_permissions(request, article)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        """
        Overide the default django error message after deleting an article
        """
        if not self.get_single_article(slug):
            article_not_found()
        super().delete(self, request, slug)
        return Response({"message": "Article Deleted Successfully"})
