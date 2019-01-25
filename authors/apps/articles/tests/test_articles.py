from .base_test import TestBaseCase

from rest_framework import status


class TestArticle(TestBaseCase):
    def base_articles(self, message, response):
        self.assertIn(message.encode(), response.content)

    def authorized_post_request(self, url):
        token = self.login_user()
        response = self.client.post(
            url, self.article, format='json',
            HTTP_AUTHORIZATION='Token ' + token)
        return response

    def http_200_ok(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def http_403_forbidden(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_article_authorized(self):
        """
        This method checks if an uthorized user can create an article
        """
        response = self.authorized_post_request(self.create_list_article_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_create_articles_unauthorized(self):
        """
        This method checks if an unauthorized user cannot create an article
        """
        response = self.client.post(self.create_list_article_url,
                                    self.article, format='json')
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided."
        self.base_articles(message, response)

    def test_anyone_can_view_articles(self):
        """
        This method tests if anyone can retrieve articles
        """
        self.create_article()
        response = self.client.get(self.create_list_article_url,
                                   format='json')
        self.http_200_ok(response)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_authorized_user_view_articles(self):
        """
        This method tests if a logged in user can access articles
        """
        token = self.login_user()
        slug = self.create_article()
        url = self.single_article_url(slug)
        response = self.client.get(
            url, format='json',
            HTTP_AUTHORIZATION='Token '+token)
        self.http_200_ok(response)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_user_cannot_create_without_title(self):
        """
        This method tests if a user can post without a title
        """
        self.article['article'].pop('title')
        response = self.authorized_post_request(self.create_list_article_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = "Title is required"
        self.base_articles(message, response)

    def test_get_an_article_that_does_not_exist(self):
        """
        This method checks that one cannot get an article
        that does not exist
        """
        response = self.authorized_post_request(self.create_list_article_url)
        slug = response.data['slug'] + "no-such-article"
        url = self.single_article_url(slug)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = "No article found for the slug given"
        self.base_articles(message, response)


    def test_user_can_update(self):
        """
        This method checks if a user can update an existing articles
        """
        response = self.authorized_post_request(self.create_list_article_url)
        slug = response.data['slug']
        url = self.single_article_url(slug)
        token = self.login_user()
        data = {"article": {
            "title": "Updated Title", "body": "Updated body"}}
        res = self.client.put(url, data, format='json',
                              HTTP_AUTHORIZATION="Token "+token)
        self.assertIn(b"Updated Title", res.content)
        self.http_200_ok(res)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_unauthorised_user_update(self):
        """
        This method tests if unauthorized user can update existing articles
        """
        slug = self.create_article()
        url = self.single_article_url(slug)
        data = {"article": {"title": "Updated Title", "body": "Updated body"}}
        response = self.client.put(url, data, format='json')
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided."
        self.base_articles(message, response)

    def test_user_can_delete(self):
        """
        This method tests if a user can delete articles
        """
        response = self.authorized_post_request(self.create_list_article_url)
        slug = response.data['slug']
        url = self.single_article_url(slug)
        response = self.client.delete(
            url, format='json', HTTP_AUTHORIZATION='Token ' +
            self.login_user())
        message = "Article Deleted Successfully"
        self.base_articles(message, response)
        self.http_200_ok(response)

    def test_unauthorised_user_delete(self):
        """
        This method tests if a non owner can delete an article
        """
        slug = self.create_article()
        url = self.single_article_url(slug)
        response = self.client.delete(url, format='json')
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided"
        self.base_articles(message, response)
