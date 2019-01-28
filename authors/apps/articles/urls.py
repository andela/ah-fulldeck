from django.urls import path

from .models import Article, LikeDislike, Comment
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
         views.RatingDetails.as_view(), name='article-ratings'),
    path('comments/<int:id>/like/',
         views.LikeDislikeView.as_view(model=Comment,
                                       vote_type=LikeDislike.LIKE),
         name="comment_like"),
    path('comments/<int:id>/dislike/',
         views.LikeDislikeView.as_view(model=Comment,
                                       vote_type=LikeDislike.DISLIKE),
         name="comment_dislike"),
    path('tags/', views.TagsView.as_view(), name="articles-tags"),
    path('articles/<slug>/favorite/',
         views.FavouriteArticleView.as_view(), name="article-favorite"),
    path('favorites/', views.GetUserFavorites.as_view(),
         name='all_favourites')
]
