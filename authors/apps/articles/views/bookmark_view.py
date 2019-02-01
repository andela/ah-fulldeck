from rest_framework.generics import (RetrieveAPIView,
                                     ListAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authors.apps.authentication.models import User
from ..serializers import ArticleSerializers
from ..utils import get_article


class BookMark(ListAPIView):
    """Implements bookmarking for an article"""
    permission_classes = IsAuthenticated,

    def put(self, request, slug):
        """"Method to bookmark or remove bookmark on article"""
        article = get_article(slug)
        user = User.objects.get(email=request.user)
        bookmarked = user.profile.bookmarks.filter(slug=slug).first()
        if bookmarked:
            user.profile.bookmarks.remove(bookmarked)
            msg = "The article {} has been removed from bookmarks!".format(
                slug)
            return Response(dict(message=msg),
                            status=status.HTTP_200_OK)
        user.profile.bookmarks.add(article)
        msg = "The article {} has been bookmarked!".format(slug)
        return Response(dict(message=msg),
                        status=status.HTTP_200_OK)


class BookMarkDetails(RetrieveAPIView):
    """Retrieve all bookmarked articles"""
    permission_classes = IsAuthenticated,
    serializer_class = ArticleSerializers

    def get(self, request):
        """fetch articles bookmarked by user"""
        user = User.objects.get(email=request.user)
        bookmarked_articles = user.profile.bookmarks.all()
        serializer = self.serializer_class(
            bookmarked_articles, context={"request": request}, many=True)
        data = {
            "User": user.username,
            "Bookmarked articles": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
