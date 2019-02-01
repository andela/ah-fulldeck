from rest_framework.generics import (RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import FavoriteArticle
from ..serializers import FavoriteArticlesSerializer
from ..utils import get_article


class FavouriteArticleView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = FavoriteArticlesSerializer

    def put(self, request, slug):
        article = get_article(slug)

        # check if article has been favorited
        favorite_article = FavoriteArticle.objects.filter(
            user=request.user.id, article=article.id).exists()

        # if article is already a favorite, remove from favorites
        if favorite_article:
            instance = FavoriteArticle.objects.filter(
                user=request.user.id, article=article.id)

            self.perform_destroy(instance)
            return Response({'message': 'Article unfavorited'},
                            status.HTTP_200_OK)

        # if article is not a favorite, then make it favorite
        data = {"article": article.id, "user": request.user.id}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Article favorited'},
                        status.HTTP_200_OK)


class GetUserFavorites(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = FavoriteArticlesSerializer
    queryset = FavoriteArticle.objects.all()

    def get(self, request):
        fav_article = FavoriteArticle.objects.filter(user=request.user.id)
        if fav_article:
            serializer = FavoriteArticlesSerializer(fav_article, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'message': 'No favorites available'},
                            status=status.HTTP_404_NOT_FOUND)
