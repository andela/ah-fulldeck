from .base_test import TestBaseCase

from rest_framework import status


class TestHighlight(TestBaseCase):
    """Class to test the highlight functionality"""

    def highlight(self):
        """Function to try all highlight possibilities"""
        self.authorize()
        slug = self.create_article()
        response1 = self.client.post(self.highlight_url(
            slug), self.highlight_data, format='json')
        response2 = self.client.post(self.highlight_url(
            slug), self.highlight_out_of_range, format='json')
        response3 = self.client.post(self.highlight_url(
            slug), self.start_index_greater_than_end_index, format='json')
        response4 = self.client.post(self.highlight_url(
            slug), self.highlight_index_not_integer, format='json')
        response5 = self.client.post(self.highlight_url(
            slug), self.missing_highlight_field, format='json')
        response6 = self.client.post(self.highlight_url(
            "invalid slug"), self.highlight_data, format='json')
        responses = [response1, response2, response3, response4,
                     response5, response6]
        return responses

    def base_error_messages(self, response, message):
        self.assertIn(message.encode(), response.content)

    def _400_bad_request(self, response, message=None):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        if message:
            self.base_error_messages(response, message)

    def test_highlight_and_comment(self):
        """Test successful comment on highlighted text"""
        response = self.highlight()[0]
        self.assertIn('highlighted_text', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_out_of_range_highlight(self):
        """Test user cannot highlight out of range index"""
        message = "Indices should be in the range 0 and 25"
        response = self.highlight()[1]
        self._400_bad_request(response, message)

    def test_start_index_larger_than_end_index(self):
        """Test start index cannot be larger than end index."""
        message = "Start index can't be greater than or equal to end index"
        response = self.highlight()[2]
        self._400_bad_request(response, message)

    def test_indices_not_integers(self):
        """Test index data type must be integer."""
        message = "Indices must be of integer format"
        response = self.highlight()[3]
        self._400_bad_request(response, message)

    def test_missing_required_field(self):
        """Test for missing field."""
        message = "start_index field cannot be empty"
        response = self.highlight()[4]
        self._400_bad_request(response, message)

    def test_highlight_non_existing_article(self):
        """Test highlighting non-existing article"""
        message = "No article found for the slug given"
        response = self.highlight()[5]
        self._400_bad_request(response, message)
