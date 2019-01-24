from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ListCreateArticle.as_view(), name='articles'),
    path('articles/<slug>/', views.RetrieveUpdateDeleteArticle.as_view(),
         name='article-details'),
    path('articles/<slug>/comments/',
         views.CommentView.as_view(), name='comments'),
    path('articles/<slug>/comments/<int:id>/',
         views.CommentDetails.as_view(), name='comment-details')
]
