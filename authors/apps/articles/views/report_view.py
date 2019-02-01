import os
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..renderers import ArticleJsonRenderer
from ..models import ReportArticle
from ..serializers import ReportArticlesSerializer
from ..utils import get_article


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
