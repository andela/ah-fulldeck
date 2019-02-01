from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers import EmailCheckSerializer
from authors.apps.helpers.send_email import send_email
from ..utils import get_article
from urllib.parse import quote


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
        email_data = [message_content, 'READ MORE',
                      article_link, '', article.title, message_body]
        send_email("Authors Haven: Article Shared",
                   request.user.email, recipient, email_data)
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
