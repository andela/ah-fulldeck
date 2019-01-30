from .base_test import TestBaseCase
from rest_framework import status


class CommentsHistoryTests(TestBaseCase):
    """
    Comments history test cases
    """

    def forbidden_403(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def ok_200(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def not_found_404(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_get_comment_history(self):
        """
        Test authenticated users can get edit history of their
        comments
        """
        self.authorize()
        slug = self.create_article()
        response = self.add_comment(slug)
        id = response.data['id']
        self.update_comment()
        response = self.client.get(self.edit_history_url(slug, id))
        self.ok_200(response)

    def test_unauthenticated_get_comment_history(self):
        """
        Test unauthenticated users cannot get edit history of their
        comments
        """
        slug = self.create_article()
        response = self.add_comment(slug)
        id = response.data['id']
        self.update_comment()
        response = self.client.get(self.edit_history_url(slug, id))
        self.forbidden_403(response)

    def test_get_history_non_existent_comment(self):
        """
        Test user cannot get history of non-existent comments
        """
        self.authorize()
        slug = self.create_article()
        response = self.add_comment(slug)
        self.update_comment()
        response = self.client.get(self.edit_history_url(slug, 9))
        self.not_found_404(response)
