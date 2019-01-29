"""
This module tests comment like and dislike functionality of comments
"""
from django.urls import reverse
from .base_test import TestBaseCase
from rest_framework import status


class TestLikeDislikeComment(TestBaseCase):
    """
    Testcase for user to like and/or dislike a comment
    """

    def like_url(self, id):
        return reverse("articles:comment_like", kwargs={'id': id})

    def dislike_url(self, id):
        return reverse("articles:comment_dislike", kwargs={'id': id})

    def base_test(self):
        slug = self.create_article()
        response = self.add_comment(slug)
        comment_id = response.data['id']
        token = self.login_user()
        like_url = self.like_url(comment_id)
        response2 = self.client.post(
            like_url, HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response2.status_code, 201)
        return response2

    def http_403_forbidden(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def http_404_not_found(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def like_dislike(self, url):
        response = self.client.post(url)
        self.http_403_forbidden(response)

    def non_existing(self, url):
        token = self.login_user()
        response = self.client.post(url,
                                    HTTP_AUTHORIZATION='Token ' + token)
        self.http_404_not_found(response)

    def test_like_a_comment(self):
        """
        Test than an authenticated user can like an comment
        """
        self.base_test()

    def test_liking_non_existent_comment(self):
        """
        Test an authenticated user liking a non-existing comment
        """
        self.non_existing(self.like_url(3))

    def test_dislike_a_comment(self):
        """
        Test than an authenticated user can dislike a comment
        """
        self.base_test()

    def test_disliking_non_existent_comment(self):
        """
        Test an authenticated user disliking a non-existing comment
        """
        self.non_existing(self.dislike_url(4))

    def test_unauthenticated_user_liking(self):
        """
        Test liking a non-existing comment
        """
        self.like_dislike(self.dislike_url(5))

    def test_unauthenticated_user_disliking(self):
        """
        Test liking a non-existing comment
        """
        self.like_dislike(self.like_url(6))
