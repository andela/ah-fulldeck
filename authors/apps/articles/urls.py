from django.urls import path

from .models import Article, LikeDislike
from . import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ListCreateArticle.as_view(), name='articles'),
    path('articles/<slug>/', views.RetrieveUpdateDeleteArticle.as_view(),
         name='article-details'),
    path('articles/<slug>/comments/',
         views.CommentView.as_view(), name='comments'),
    path('articles/<slug>/comments/<int:id>/',
         views.CommentDetails.as_view(), name='comment-details'),
    path('articles/<slug>/like/',
         views.LikeDislikeView.as_view(
             model=Article, vote_type=LikeDislike.LIKE),
         name='article_like'),
    path('articles/<slug>/dislike/',
         views.LikeDislikeView.as_view(
             model=Article, vote_type=LikeDislike.DISLIKE),
         name='article_dislike'),
    path('articles/<slug>/rate/', views.RatingView.as_view(),
         name='rate-articles'),
    path('articles/<slug>/ratings/',
         views.RatingDetails.as_view(), name='article-ratings')
]
