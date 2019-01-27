import json

from rest_framework.renderers import JSONRenderer, BaseRenderer


class ProfileJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'profile'

    def render(self, data, media_type=None, renderer_context=None):
        # If the view throws an error (such as the user can't be authenticated)
        # `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        errors = data.get('errors', None)

        if errors is not None:
            # As mentioned above, we will let the default JSONRenderer handle
            # rendering errors.
            return super().render(data)

        return json.dumps({
            self.object_label: data
        })


class FollowUnfollowJsonRenderer(BaseRenderer):
    """
    This class determines the display format
    for following/unfollowing and any errors
    """
    media_type = 'application/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        follow = data.get('follow-detail')
        if follow:
            return json.dumps({'You are now following {}'.format(data['user']): data})
        unfollow = data.get('unfollow-detail')
        if unfollow:
            return json.dumps({'You have successfuly unfollowed {}'.format(data['user']): data})
        errors = data.get('errors', None)
        if errors:
            return json.dumps({'Details': data})
        else:
            return json.dumps({'Details': data})


class FollowingFollowrsJsonRenderer(BaseRenderer):
    """
    This class determines the display format
    for following
    """
    media_type = 'application/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        followers = data.get('followers-detail')
        if followers:
            return json.dumps({'Here is a list of followers for {}'.format(data['user']): data})
        following = data.get('following-detail')
        if following:
            return json.dumps({'Here is a list users following {}'.format(data['user']): data})
        errors = data.get('detail', None)
        if errors:
            return json.dumps({'Message': data})
        if isinstance(data, dict):
            return json.dumps(
                {'Response': data})