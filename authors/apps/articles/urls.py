from django.urls import path

from .models import Article, LikeDislike, Comment
from .views import (article_views, bookmark_view, comment_views,
                    favourite_view, likedislike_view, rating_view,
                    report_view, tag_view, share_view, stats_view)

app_name = "articles"

urlpatterns = [
    path('articles/', article_views.ListCreateArticle.as_view(), name='articles'),
    path('articles/bookmarks/',
         bookmark_view.BookMarkDetails.as_view(), name='article-bookmarks'),
    path('articles/<slug>/', article_views.RetrieveUpdateDeleteArticle.as_view(),
         name='article-details'),
    path('articles/<slug>/comments/',
         comment_views.CommentView.as_view(), name='comments'),
    path('articles/<slug>/comments/<int:id>/',
         comment_views.CommentDetails.as_view(), name='comment-details'),
    path('articles/<slug>/like/',
         likedislike_view.LikeDislikeView.as_view(
             model=Article, vote_type=LikeDislike.LIKE),
         name='article_like'),
    path('articles/<slug>/dislike/',
         likedislike_view.LikeDislikeView.as_view(
             model=Article, vote_type=LikeDislike.DISLIKE),
         name='article_dislike'),
    path('articles/<slug>/rate/', rating_view.RatingView.as_view(),
         name='rate-articles'),
    path('articles/<slug>/ratings/',
         rating_view.RatingDetails.as_view(), name='article-ratings'),
    path('comments/<int:id>/like/',
         likedislike_view.LikeDislikeView.as_view(model=Comment,
                                                  vote_type=LikeDislike.LIKE),
         name="comment_like"),
    path('comments/<int:id>/dislike/',
         likedislike_view.LikeDislikeView.as_view(model=Comment,
                                                  vote_type=LikeDislike.DISLIKE),
         name="comment_dislike"),
    path('tags/', tag_view.TagsView.as_view(), name="articles-tags"),
    path('articles/<slug>/favorite/',
         favourite_view.FavouriteArticleView.as_view(), name="article-favorite"),
    path('favorites/', favourite_view.GetUserFavorites.as_view(),
         name='all_favourites'),
    path('articles/<slug>/bookmark/',
         bookmark_view.BookMark.as_view(), name='article-bookmark'),
    path('articles/<slug>/report/',
         report_view.ReportArticlesView.as_view(), name='report-article'),
    path('<slug>/comments/<int:id>/history/',
         comment_views.CommentHistory.as_view(),
         name='comment-history'),
    path('articles/<slug>/highlight/',
         comment_views.HighlightAPIView.as_view(), name='highlighttext'),
    path('<slug>/share/email/', share_view.ShareArticleViaEmail.as_view(),
         name="email_share_article"),
    path('<slug>/share/facebook/', share_view.ShareArticleViaFacebook.as_view(),
         name="facebook-share-article"),
    path('statistics/',
         stats_view.ArticlesStatsView.as_view(), name='article-stats'),
    path('<slug>/share/twitter/', share_view.ShareArticleViaTwitter.as_view(),
         name="twitter-share-article")

]
