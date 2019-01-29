from rest_framework import renderers
import json


class ArticleJsonRenderer(renderers.BaseRenderer):
    """
    This class determines the display format
    for the articles and any errors
    """
    media_type = 'application/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # checks if the data received is a list
        # Used to display the articles
        if isinstance(data, list):
            return json.dumps(
                {
                    'articles': data,
                    'article_count': len(data)
                })
        else:
            # checks if the data received is an error message
            error = data.get('detail')
            if error:
                return json.dumps({'message': data})
            # if not an error then it must be a single article dictionary
            return json.dumps({'article': data})


class RatingJSONRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    media_type = 'application/json'
    format = 'json'
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):
            return json.dumps(
                {'ratings': data})
        else:
            # checks if the data received is an error message
            error = data.get('detail')
            if error:
                return json.dumps({'message': data})
            # if not an error then it must be a single article dictionary
            return json.dumps({'rating': data})
