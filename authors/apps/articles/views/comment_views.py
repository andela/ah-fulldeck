from rest_framework.generics import (
    ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from ..permissions import IsOwnerOrReadonly
from ..models import Comment
from ..serializers import (ArticleSerializers,
                           CommentsSerializers,
                           CommentHistorySerializer,ProfileSerializer)
from ..utils import get_article


class CommentView(ListCreateAPIView):
    """
    Class for creating and listing all comments
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


class HighlightAPIView(CreateAPIView):
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
        comment = request.data["body"]
        author = request.user
        context = {
            "request": comment,
            "author": author,
            "article": article
        }
        highlighted_text = article_body[start_index:end_index]
        fetch_comment = article.comments.filter(body=comment).first()
        fetch_author = article.comments.filter(author=author).first()
        fetch_hightlight = article.comments.filter(
            highlighted_text=highlighted_text).first()
        if fetch_comment and fetch_author and fetch_hightlight:
            message1 = "You have posted same comment on this highlight before."
            message2 = "Consider editting the comment or highlight"
            message = message1+message2
            return Response({"error": message},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentsSerializers(data=request.data,
                                         context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, article_id=article.id,
                        highlighted_text=highlighted_text)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
