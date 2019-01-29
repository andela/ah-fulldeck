from .base_test import TestBaseCase
from rest_framework import status


class TestBookmarking(TestBaseCase):
    """Class to test bookmarking functionality"""

    def base_error_messages(self, response, message):
        self.assertIn(message.encode(), response.content)

    def base_200_ok(self, response, message=None):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if message:
            self.base_error_messages(response, message)

    def base_403_forbidden(self, response, message=None):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        if message:
            self.base_error_messages(response, message)

    def base_article_not_found(self, response, message=None):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        if message:
            self.base_error_messages(response, message)

    def bookmark(self, slug):
        '''bookmark an article'''
        url = self.bookmark_article_url(slug)
        response = self.client.put(url)
        return response

    def test_get_bookmarks(self):
        '''test retrieving all bookmarks'''
        self.authorize()
        response = self.client.get(self.get_bookmarks_url())
        self.base_200_ok(response)

    def test_bookmark(self):
        '''test bookmarking an article'''
        self.authorize()
        message = "The article test-article has been bookmarked!"
        response = self.bookmark(self.create_article())
        self.base_200_ok(response, message)

    def test_remove_bookmark(self):
        """Test removing a bookmark"""
        self.authorize()
        message = "The article test-article has been removed from bookmarks!"
        self.bookmark(self.create_article())
        response = self.bookmark("test-article")
        self.base_200_ok(response, message)

    def test_bookmark_non_existent_article(self):
        """Test bookmarking non-existing article"""
        self.authorize()
        message = "No article found for the slug given"
        response = self.bookmark("This slug doesn't exist")
        self.base_article_not_found(response, message)

    def test_unauthorized_user(self):
        """Test unauthenticated user can't bookmark articles"""
        message = "Authentication credentials were not provided."
        response = self.bookmark(self.create_article())
        self.base_403_forbidden(response, message)
