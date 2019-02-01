from django.db.models import Avg
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, CreateAPIView,
    RetrieveAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from collections import Counter
from ..renderers import RatingJSONRenderer
from ..models import ArticleRatings
from ..serializers import RatingSerializer
from ..utils import get_article


class RatingView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = RatingSerializer
    renderer_classes = (RatingJSONRenderer,)
    queryset = ArticleRatings.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'

    def get_article(self, slug):
        article = get_article(slug=slug)

        return article

    def post(self, request, slug):
        serializer_data = request.data.get('rating', {})
        article = self.get_article(slug)

        if article is not None:
            rating = ArticleRatings.objects.filter(
                article=article, rated_by=request.user).first()
            rating_author = article.author
            rating_user = request.user
            if rating_author == rating_user:
                data = {'errors': 'You cannot rate your own article'}
                return Response(data, status=status.HTTP_403_FORBIDDEN)

            else:
                serializer = self.serializer_class(
                    rating, data=serializer_data, partial=True)
                serializer.is_valid(raise_exception=True)

                serializer.save(rated_by=request.user, article=article)
                data = serializer_data
                data['message'] = "You have rated this article successfully"
                return Response(data, status=status.HTTP_201_CREATED)


class RatingDetails(RetrieveAPIView):
    queryset = ArticleRatings.objects.all()
    serializer_class = RatingSerializer
    renderer_classes = (RatingJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'

    def get(self, request, slug):
        article = get_article(slug)

        if article is not None:
            avg_rating = ArticleRatings.objects.filter(
                article=article).aggregate(
                average_rating=Avg('rating'))['average_rating'] or 0
            avg_rating = round(avg_rating)
            total_user_rates = ArticleRatings.objects.filter(
                article=article).count()
            each_rating = Counter(ArticleRatings.objects.filter(
                article=article).values_list('rating', flat=True))

            return Response({
                'avg_rating': avg_rating,
                'total_user_rates': total_user_rates,
                'each_rating': each_rating
            }, status=status.HTTP_200_OK)
