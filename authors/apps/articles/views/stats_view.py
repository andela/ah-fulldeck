from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from ..models import Article
from ..serializers import ArticleStatSerializer
from ..renderers import ArticleJsonRenderer


class ArticlesStatsView(ListAPIView):
    serializer_class = ArticleStatSerializer
    renderer_classes = (ArticleJsonRenderer,)
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)
