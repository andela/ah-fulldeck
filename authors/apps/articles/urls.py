from django.urls import path

from .models import Article, LikeDislike, Comment
from . import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ListCreateArticle.as_view(), name='articles'),
    path('articles/bookmarks/',
         views.BookMarkDetails.as_view(), name='article-bookmarks'),
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
         name='all_favourites'),
    path('articles/<slug>/bookmark/',
         views.BookMark.as_view(), name='article-bookmark'),
    path('articles/<slug>/report/',
         views.ReportArticlesView.as_view(), name='report-article'),
    path('<slug>/comments/<int:id>/history/',
         views.CommentHistory.as_view(),
         name='comment-history'),
    path('articles/<slug>/highlight/',
         views.HighlightAPIView.as_view(), name='highlighttext'),
    path('<slug>/share/email/', views.ShareArticleViaEmail.as_view(),
         name="email_share_article"),
    path('<slug>/share/facebook/', views.ShareArticleViaFacebook.as_view(),
         name="facebook-share-article"),
    path('<slug>/share/twitter/', views.ShareArticleViaTwitter.as_view(),
         name="twitter-share-article"),
    path('statistics/',
         views.ArticlesStatsView.as_view(), name='article-stats')
]
