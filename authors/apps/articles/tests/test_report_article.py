from django.urls import reverse
from rest_framework import status
import json

from .base_test import TestBaseCase


class ReportArticleTest(TestBaseCase):
    def base_report(self, message, response):
        self.assertIn(message.encode(), response.content)

    def get_report_article_url(self):
        slug = self.create_article()
        url = reverse(
            'articles:report-article', args=[slug]
        )
        return url

    def reporting_user_token(self):
        return self.login_user2()

    def report_article(self):
        response = self.client.post(
            self.get_report_article_url(),
            data=self.report_message,
            HTTP_AUTHORIZATION='Token ' + self.reporting_user_token(),
            format='json')
        return response

    def report_multiple_times(self):
        url = self.get_report_article_url()
        i = 0
        while i < 7:
            response = self.client.post(
                url,
                data=self.report_message,
                HTTP_AUTHORIZATION='Token ' + self.reporting_user_token(),
                format='json')
            i += 1
        return response

    def test_a_user_can_report_an_article(self):
        """This method tests if a user can report an article"""
        response = self.report_article()
        message = 'An email has been sent to the admin with your request'
        self.base_report(message, response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_cannot_report_their_own_article(self):
        """This method tests is a user can report they own article"""
        response = self.client.post(
            self.get_report_article_url(),
            data=self.report_message,
            HTTP_AUTHORIZATION='Token ' + self.login_user(),
            format='json')
        message = 'You cannot report your own article'
        self.base_report(message, response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_cannot_report_multiple_times(self):
        """This method tests if a user cannot post multiple reports of the same article"""
        response = self.report_multiple_times()
        message = 'You cannot report this article multiple times'
        self.base_report(message, response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
