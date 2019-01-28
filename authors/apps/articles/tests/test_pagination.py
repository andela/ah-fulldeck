from .base_test import TestBaseCase


class PaginationTestCase(TestBaseCase):
    def create_multiple_articles(self):
        for i in range(21):
            self.create_article()

    def is_present(self, value):
        response = self.client.get(self.create_list_article_url)
        self.assertIn(value, response.data)

    def test_article_pagination(self):
        self.is_present('count')
        self.is_present('next')
        self.is_present('previous')

    def test_pagination_more_than_ten_articles(self):
        self.create_multiple_articles()
        response = self.client.get(self.create_list_article_url)
        self.assertEqual(21, response.data['count'])
        self.assertNotEqual(None, response.data['next'])
