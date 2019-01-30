from rest_framework import status
import json

from authors.apps.articles.tests.base_test import TestBaseCase


class TagsTest(TestBaseCase):

    def base_articles(self, message, response):
        self.assertIn(message.encode(), response.content)

    def http_200_ok(self, response, message):
        self.base_articles(message, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def http_201_created(self, response, message):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.base_articles(message, response)

    def http_403_forbidden(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def create_articles(self):
        self.authorize()
        url = self.create_list_article_url
        response = self.client.post(
            url, self.article, format='json')
        return response

    def test_user_can_create_article_with_tags(self):
        """This method tests if a user can create tags"""
        response = self.create_articles()
        message = '"tags": ["test", "tags"]'
        self.http_201_created(response, message)

    def test_user_can_create_article_without_tag(self):
        """This method test is a user can create an article without tag"""
        del self.article['article']['tags']
        response = self.create_articles()
        message = '"tags": []'
        self.http_201_created(response, message)

    def test_user_can_get_article_with_tags(self):
        """This method tests if a user can get an article with tags"""
        url = self.single_article_details()
        response = self.client.get(url, format='json')
        message = '"tags": ["test", "tags"]'
        self.http_200_ok(response, message)

    def test_user_can_get_all_tags(self):
        """This method tests if a user can get all tags"""
        self.create_articles()
        url = self.get_tags_url
        response = self.client.get(url)
        message = 'tags":["test","tags"]'
        self.http_200_ok(response, message)

    def test_unauthorized_users_cannot_create_tags(self):
        """This method tests if unauthorized users can create tags"""
        url = self.create_list_article_url
        response = self.client.post(url, data=self.article, format='json')
        message = "Authentication credentials were not provided"
        self.base_articles(message, response)
        self.http_403_forbidden

    def test_tags_are_created_as_slugs(self):
        self.article['article']['tags'].extend(["NEW TAG"])
        response = self.create_articles()
        self.assertIn('new-tag', json.dumps(response.data))

    def test_user_cannot_post_special_characters_on_tags(self):
        self.article['article']['tags'].extend(["NEW TAG WITH Characters #$%"])
        response = self.create_articles()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = "Tag cannot have special characters"
        self.base_articles(message, response)
