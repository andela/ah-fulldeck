from .base_test import TestBaseCase
from rest_framework import status


class CommentsTests(TestBaseCase):
    """
    Comments test cases
    """

    def forbidden_403(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def ok_200(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def created_201(self, response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_comment(self):
        """
        Test if authenticated users can create comments
        """
        slug = self.create_article()
        response = self.add_comment(slug)
        self.created_201(response)

    def test_unauthenticated_user_cannot_comment(self):
        """
        Test if authenticated users can create comments
        """
        slug = self.create_article()
        response = self.client.post(
            self.create_comment(slug),
            self.comment,
            format="json"
        )
        self.forbidden_403(response)

    def test_unauthenticated_users_can_view_comments(self):
        """
        Test unauthenticated users can view all comments
        """
        slug = self.create_article()
        response = self.client.get(self.create_comment(slug))
        self.ok_200(response)

    def test_authenticate_users_can_view_comments(self):
        """
        Test authenticated users can view all comments
        """
        token = self.login_user()
        slug = self.create_article()
        response = self.client.get(self.create_comment(slug),
                                   HTTP_AUTHORIZATION="Token " + token)
        self.ok_200(response)

    def test_can_view_single_comment(self):
        """
        Test users can view a single comment
        """
        slug = self.create_article()
        response = self.add_comment(slug)
        id = response.data['id']
        response = self.client.get(self.specific_comment(slug, id))
        self.ok_200(response)

    def test_delete_comment(self):
        """
        Test users can view a single comment
        """
        token = self.login_user()
        slug = self.create_article()
        response = self.add_comment(slug)
        id = response.data['id']
        response = self.client.delete(
            (self.specific_comment(slug, id)),
            HTTP_AUTHORIZATION="Token " + token)
        self.ok_200(response)

    def test_update_comment(self):
        """
        Test authenticated users can update their comments
        """
        token = self.login_user()
        slug = self.create_article()
        response = self.add_comment(slug)
        id = response.data['id']
        response = self.client.put(
            (self.specific_comment(slug, id)),
            data={'comment': {'body': 'New comment'}},
            format='json',
            HTTP_AUTHORIZATION="Token " + token)
        self.ok_200(response)

    def test_can_thread_a_comment(self):
        """
        Test users can thread a comment
        """
        token = self.login_user()
        slug = self.create_article()
        response = self.add_comment(slug)
        id = response.data['id']
        response = self.client.post((self.specific_comment(slug, id)),
                                    data={'comment':
                                          {'body': 'child comment'}},
                                    format='json',
                                    HTTP_AUTHORIZATION="Token " + token)
        self.created_201(response)
        self.assertIn(b'child comment', response.content)

    def test_unauthenticated_user_cannot_delete_comment(self):
        """
        Test users can view a single comment
        """

        slug = self.create_article()
        response = self.add_comment(slug)
        id = response.data['id']
        response = self.client.delete(self.specific_comment(slug, id))
        self.forbidden_403(response)

    def test_unauthenticated_user_cannot_update_comment(self):
        """
        Test authenticated users can update their comments
        """
        slug = self.create_article()
        response = self.add_comment(slug)
        id = response.data['id']
        response = self.client.put(
            (self.specific_comment(slug, id)),
            data={'comment': {'body': 'New comment'}},
            format='json')
        self.forbidden_403(response)
