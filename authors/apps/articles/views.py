from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import os
from rest_framework.pagination import PageNumberPagination
from .permissions import IsOwnerOrReadonly
from authors.apps.authentication.models import User
from rest_framework.views import APIView
from collections import Counter
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from django.template.loader import render_to_string
from urllib.parse import quote
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView,
    RetrieveAPIView, ListAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, AllowAny)

from collections import Counter
from django.shortcuts import get_object_or_404
from .renderers import ArticleJsonRenderer, RatingJSONRenderer
from collections import Counter
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Avg
from authors.apps.core.pagination import StandardPagination
from authors.apps.authentication.models import User
from .permissions import IsOwnerOrReadonly
from .models import (Article, Comment, LikeDislike, ArticleRatings,
                     FavoriteArticle, Tag, ReportArticle)
from .serializers import (ArticleSerializers,
                          CommentsSerializers,
                          LikeDislikeSerializer,
                          RatingSerializer,
                          FavoriteArticlesSerializer,
                          CommentHistorySerializer,
                          TagSerializer, ReportArticlesSerializer, EmailCheckSerializer, ArticleStatSerializer,)
from authors.apps.helpers.send_email import send_email
                          

def article_not_found():
    raise ValidationError(
        detail={'error': 'No article found for the slug given'})


def get_article(slug):
    try:
        article = Article.objects.get(slug=slug)
        return article
    except Exception:
        article_not_found()


class ListCreateArticle(ListCreateAPIView):
    queryset = Article.objects.all()
    renderer_classes = (ArticleJsonRenderer,)
    serializer_class = ArticleSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        paginator = StandardPagination()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = ArticleSerializers(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

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

    def get(self, request, slug):
        article = get_article(slug)
        if not article:
            article_not_found()
        if request.user and not isinstance(request.user, AnonymousUser) and article.author != request.user:
            article.views += 1
            article.save()
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
        if not get_article(slug):
            article_not_found()
        super().delete(self, request, slug)
        return Response({"message": "Article Deleted Successfully"})


class CommentView(ListCreateAPIView):
    """
    Class for creating and email_data all comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, slug, *args, **kwargs):
        """
        Method for creating article
        """
        article = get_article(slug)
        serializer_context = {
            'request': request.data["comment"]["body"],
            'author': request.user,
            'article': article
        }
        serializer = self.serializer_class(
            data=request.data["comment"], context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, article_id=article.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, slug):
        """
        Method for getting all comments
        """
        article = get_article(slug)
        comments = article.comments.filter()
        serializer = self.serializer_class(comments.all(), many=True)
        data = {
            'count': comments.count(),
            'comments': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class CommentDetails(RetrieveUpdateDestroyAPIView,
                     ListCreateAPIView):
    """
    Class for retrieving, updating and deleting a comment
    """
    queryset = Comment.objects.all()
    lookup_field = 'id'
    serializer_class = CommentsSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)

    def get(self, request, slug, id):
        article = get_article(slug)
        try:
            article.comments.filter(id=id).first()
            return super().get(request, id)
        except:
            raise ValidationError(
                detail={'error': 'No comment found for the ID given'})

    def create(self, request, slug, id):
        """Method for creating a child comment on parent comment."""
        context = super(CommentDetails,
                        self).get_serializer_context()
        article = get_article(slug)
        try:
            parent_comment = article.comments.filter(id=id).first().pk
        except:
            message = {'detail': 'Comment not found.'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        body = request.data.get('comment', {})['body']
        data = {
            'body': body,
            'parent': parent_comment,
            'article': article.pk
        }

        serializer = self.serializer_class(
            data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, article_id=article.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, slug, id):
        """
        Method for deleting a comment
        """
        article = get_article(slug)
        comment = article.comments.filter(id=id)
        if not comment:
            message = {'detail': 'Comment not found.'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        comment[0].delete()
        message = {'detail': 'Comment Deleted Successfully'}
        return Response(message, status=status.HTTP_200_OK)

    def update(self, request, slug, id):
        """
        Method for editing a comment
        """
        article = get_article(slug)

        comment = article.comments.filter(id=id).first()
        if not comment:
            message = {'detail': 'Comment not found.'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        new_comment = request.data.get('comment', {})['body']
        data = {
            'body': new_comment,
            'article': article.pk,
            'author': request.user.id
        }
        serializer = self.serializer_class(comment, data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LikeDislikeView(CreateAPIView):
    """
    this class defines the endpoint for like and dislike
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = LikeDislikeSerializer
    model = None  # Data Model - Articles or Comments
    vote_type = None  # Vote type Like/Dislike

    def post(self, request, slug=None, id=None):
        """
        This view enables a user to like or dislike an article or specific
        comment
        """
        # check an article is existing
        if self.model.__name__ is 'Article':
            obj = get_object_or_404(Article, slug=slug)
        else:  # model is comment
            obj = get_object_or_404(Comment, id=id)

        try:
            # if user has ever voted
            like_dislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                user=request.user)
            # check if the user has liked or disliked the article or comment already
            if like_dislike.vote is not self.vote_type:
                like_dislike.vote = self.vote_type
                like_dislike.save(update_fields=['vote'])
                result = True
            else:
                # delete the existing record if the user is submitting a similar vote
                like_dislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            # user has never voted for the article or comment, create new record.
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return Response({
            "status": result,
            "likes": obj.votes.likes().count(),
            "dislikes": obj.votes.dislikes().count(),
            "Total": obj.votes.sum_rating()
        },
            content_type="application/json",
            status=status.HTTP_201_CREATED
        )


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
            avg_rating = ArticleRatings.objects.filter(article=article).aggregate(
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


class TagsView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        data = self.get_queryset()
        serializer = self.serializer_class(data, many=True)
        return Response({'tags': serializer.data}, status=status.HTTP_200_OK)


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
            return Response({'message': 'No favorites available'}, status=status.HTTP_404_NOT_FOUND)


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


class CommentHistory(ListCreateAPIView):
    """
    Retrieve comments history with
    comment id
    """
    serializer_class = CommentHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, slug, **kwargs):

        article = get_article(slug)
        comment = article.comments.filter(id=id).first()
        if not comment:
            message = {'error': 'Comment not found'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        id = self.kwargs['id']
        edited_comment = Comment.history.filter(id=id)
        if not edited_comment:
            message = {'error': 'No edit history for this comment'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(edited_comment, many=True)
        data = {
            'Comment Edit History': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class HighlightAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = ArticleSerializers

    def post(self, request, slug):
        article = get_article(slug)
        data_fields = ["start_index", "end_index", "body"]
        for field in data_fields:
            if field not in request.data:
                msg = "{} field cannot be empty".format(field)
                return Response({"error": msg},
                                status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(article)
        start_index = request.data['start_index']
        end_index = request.data['end_index']
        article_body = serializer.data['body']
        indices = [start_index, end_index]
        for index in indices:
            if not isinstance(index, int):
                return Response({"error": "Indices must be of integer format"},
                                status=status.HTTP_400_BAD_REQUEST)

        if (start_index >= end_index):
            msg = "Start index can't be greater than or equal to end index"
            return Response({
                "error": msg
            }, status=status.HTTP_400_BAD_REQUEST)

        if (end_index > len(article_body)):
            msg = "Indices should be in the range 0 and {}".format(
                len(article_body))
            return Response({
                "error": msg
            }, status=status.HTTP_400_BAD_REQUEST)
        context = {
            "request": request.data["body"],
            "author": request.user,
            "article": article
        }
        highlighted_text = article_body[start_index:end_index]

        serializer = CommentsSerializers(data=request.data,
                                         context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, article_id=article.id,
                        highlighted_text=highlighted_text)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportArticlesView(ListCreateAPIView):
    queryset = ReportArticle.objects.all()
    serializer_class = ReportArticlesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJsonRenderer,)

    def post(self, request, slug):
        # Checks if there is an article with that slug
        article = get_article(slug=slug)
        # checks if the author is trying to report the article
        if article.author == request.user:
            return Response(
                {"errors": "You cannot report your own article"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # gets the article, user and report_msg
        article_report = article
        user_report = request.user
        report_msg = request.data.get(
            'report', {})['report_msg']
        no_of_reports = ReportArticle.objects.filter(
            article=article_report, user=user_report
        ).count()
        # checks how many times users has reported and returns an error
        if no_of_reports > 5:
            return Response(
                {"errors": "You cannot report this article multiple times"},
                status=status.HTTP_400_BAD_REQUEST
            )
        report = {
            'article': article.slug,
            'user': request.user,
            'report_msg': report_msg
        }
        # creates an instance of the report
        serializer = self.serializer_class(data=report)
        serializer.is_valid(raise_exception=True)
        # Send mail to Admin before saving the serialized object
        recipient = os.getenv('EMAIL_RECIPIENT')
        subject = "Authors Haven: Reported article"
        sender = '{}'.format(request.user,)
        host_url = get_current_site(request)
        url = "http://" + host_url.domain + \
            '/api/v1/articles/'+str(article.slug)+'/'
        button_content = 'View reported article'
        email_message = render_to_string('report_article_template.html', {
            'link': url,
            'article_title': article.title,
            'article_author': article.author.username,
            'name': request.user.username,
            'report': report_msg,
            'button_content': button_content,
            'title': subject
        })
        email_content = strip_tags(email_message)
        msg = EmailMultiAlternatives(
            subject, email_content, sender, to=[recipient])
        msg.attach_alternative(email_message, "text/html")
        msg.send()
        content = "An email has been sent to the admin with your request"
        message = {"message": content}
        serializer.save()
        return Response(message, status=status.HTTP_200_OK)


class ShareArticleViaEmail(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailCheckSerializer

    def post(self, request, slug):
        article = get_article(slug)

        user_data = request.data.get('email', {})
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)

        recipient = user_data['email']
        if not recipient:
            return Response({"error": "Email address is required"}, status=status.HTTP_404_NOT_FOUND)
        message_content = request.user.username + ' has shared an article with you '
        article_link = 'http://' + request.get_host() + '/api/v1/articles/'+slug
        message_body = article.body[0:200] + ' ...'
        email_data = [message_content, 'READ MORE', article_link, '', article.title, message_body]
        send_email("Authors Haven: Article Shared", request.user.email, recipient, email_data)
        message = {"message": "Article successfully shared"}
        return Response(message, status.HTTP_200_OK)


class ShareArticleViaFacebook(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):
        get_article(slug)

        facebook_url = "https://www.facebook.com/sharer/sharer.php?u="
        article_link = "http://{}/api/v1/articles/{}".format(
            request.get_host(), slug)
        url_link = facebook_url + article_link
        shared_post_url = {'link': url_link}
        return Response(shared_post_url, status.HTTP_200_OK)


class ShareArticleViaTwitter(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):

        article = get_article(slug)

        twitter_url = "https://twitter.com/home?status="
        title = article.title
        author = article.author.username
        associated_text = quote(title + ' by ' + author + ' ')
        article_link = "{}http://{}/api/v1/articles/{}".format(
            associated_text, request.get_host(), slug)
        url_link = twitter_url + article_link
        shared_post_url = {'link': url_link}
        return Response(shared_post_url, status=status.HTTP_200_OK)


class ArticlesStatsView(ListAPIView):
    serializer_class = ArticleStatSerializer
    renderer_classes = (ArticleJsonRenderer,)
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)
