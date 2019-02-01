from rest_framework.decorators import renderer_classes, api_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import coreapi
from rest_framework import response


# noinspection PyArgumentList
@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    # noinspection PyArgumentList
    schema = coreapi.Document(
        title='Authors Haven API',
        url='localhost:8000',
        content={
            'Authentication': {
                'create_user': coreapi.Link(
                    url='/api/v1/users/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='form',
                            description='The name of the User.'
                        ),
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='The email of the User.'
                        ),
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='The intended password of the User.'
                        )
                    ],
                    description='Create a User Account.'
                ),
                'login_user': coreapi.Link(
                    url='/api/v1/users/login/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='form',
                            description='The name of the User.'
                        ),
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='The password of User.'
                        )
                    ],
                    description='Login a User.'
                ),
                'social auth': coreapi.Link(
                    url='/api/v1/users/social/login/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='provider',
                            required=True,
                            location='form',
                            description='The name of the provider.'
                        ),
                        coreapi.Field(
                            name='access_token',
                            required=True,
                            location='form',
                            description='The acess token of the User.'
                        ),
                        coreapi.Field(
                            name='access_token_secret',
                            required=False,
                            location='form',
                            description='The acess token secret of the User.'
                        )
                    ],
                    description='Login via social sites (Google, Twitter, Facebook).'
                ),
                'password_reset': coreapi.Link(
                    url='/api/v1/users/password_reset/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='The email of the User.'
                        ),
                    ],
                    description='Reset password of a User.'
                ),
                'password_update': coreapi.Link(
                    url='/api/v1/users/password_update/{token}',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='password',
                            required=True,
                            location='form',
                            description='The password of the User.'
                        ),
                        coreapi.Field(
                            name='confirm_password',
                            required=True,
                            location='form',
                            description='The password of User.'
                        )
                    ],
                    description='Update password of a User.'
                ),
            },
            'Profile': {
                'get user profile': coreapi.Link(
                    url='/api/v1/users/{username}/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the User.'
                        )

                    ],
                    description='Get profile of a single user.'

                ),
                'update user_profile': coreapi.Link(
                    url='/api/v1/users/{username}/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the User.'
                        ),
                        coreapi.Field(
                            name='bio',
                            required=False,
                            location='form',
                            description='The bio of the User.'
                        ),
                        coreapi.Field(
                            name='image url',
                            required=False,
                            location='path',
                            description='The image of User.'
                        )
                    ],
                    description='Update user bio'
                ),
                'get all profiles': coreapi.Link(
                    url='/api/v1/profiles/',
                    action='GET',
                    description='Get all profiles'
                ),
                'follow a user': coreapi.Link(
                    url='/api/v1/users/username/follow/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the User.'
                        )

                    ],
                    description='Follow a user'
                ),
                'unfollow a user': coreapi.Link(
                    url='/api/v1/users/username/follow/',
                    action='DELETE',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the User.'
                        ),

                    ],
                    description='Unfollow a single user.'

                ),
                'get all followers': coreapi.Link(
                    url='/api/v1/users/username/followers/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the User.'
                        ),

                    ],
                    description='Get all followers a single user.'

                ),
                'get all following': coreapi.Link(
                    url='/api/v1/users/username/following/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='username',
                            required=True,
                            location='path',
                            description='Username of the User.'
                        ),

                    ],
                    description='Get all following a single user.'

                ),
            },
            'Articles': {
                'create_article': coreapi.Link(
                    url='/api/v1/articles/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='title',
                            required=True,
                            location='form',
                            description='The title of the article.'
                        ),
                        coreapi.Field(
                            name='description',
                            required=True,
                            location='form',
                            description='The article description.'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='The article body'
                        )
                    ],
                    description='Create Article'
                ),
                'get_articles': coreapi.Link(
                    url='/api/v1/articles/',
                    action='GET',
                    description='Display all the articles.',
                ),
                'get_tags': coreapi.Link(
                    url='/api/v1/tags/',
                    action='GET',
                    description='Display all the tags.',
                ),
                'get_single_article': coreapi.Link(
                    url='/api/v1/articles/{slug}/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        )],
                    description='Display a single article',
                ),
                'update_single_article': coreapi.Link(
                    url='/api/v1/articles/{slug}/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                        coreapi.Field(
                            name='title',
                            location='form',
                            description='New title to be updated'
                        ),
                        coreapi.Field(
                            name='description',
                            location='form',
                            description='New description'
                        ),
                    ],
                    description='Update an article',
                ),
                'delete_single_article': coreapi.Link(
                    url='/api/v1/articles/{slug}/',
                    action='DELETE',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        )
                    ],
                    description='Delete an article',
                ),
                'comments': coreapi.Link(
                    url='/api/v1/articles/{slug}/comments/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='Body of the comemnt'
                        ),
                    ],
                    description='Coment on an article',
                ),
                'get all comments': coreapi.Link(
                    url='/api/v1/articles/{slug}/comments/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                    ],
                    description='Get all coments on an article',
                ),
                'get a specific comment': coreapi.Link(
                    url='/api/v1/articles/{slug}/comments/{id}/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='The id of the comment.'
                        ),
                    ],
                    description='Get a specific comment',
                ),
                'Like an article': coreapi.Link(
                    url='/api/v1/articles/{slug}/like/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        )],
                    description='Like an article',
                ),
                'Dislike an article': coreapi.Link(
                    url='/api/v1/articles/{slug}/dislike/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        )],
                    description='Dislike an article',
                ),
                'update_single_comment': coreapi.Link(
                    url='/api/v1/articles/{slug}/comments/{id}/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='The id of the comment.'
                        ),

                        coreapi.Field(
                            name='body',
                            location='form',
                            description='New body on the comment'
                        ),
                    ],
                    description='Update a comment',
                ),
                'delete_single_comment': coreapi.Link(
                    url='/api/v1/articles/{slug}/comments/{id}/',
                    action='DELETE',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        ),
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='The id of the comment.'
                        ),
                    ],
                    description='Delete a comment',
                ),
                'thread': coreapi.Link(
                    url='/api/v1/articles/{slug}/comments/{id}/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        ),
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='Id of the comment'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='Body of a single thread'
                        ),
                    ],
                    description='Comment on a comment',
                ),
                'Like_a_comment': coreapi.Link(
                    url='/api/v1/comments/{id}/like/',
                    action='POST',
                    fields=[

                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='Id of the comment'
                        )
                    ],
                    description='Like a comment',
                ),
                'Dislike_a_comment': coreapi.Link(
                    url='/api/v1/comments/{id}/dislike/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='Id of the comment'
                        )
                    ],
                    description='Dislike a comment',
                ),
                'rate_an_article': coreapi.Link(
                    url='/api/v1/articles/{slug}/rate/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        ),
                        coreapi.Field(
                            name='rating',
                            required=True,
                            location='form',
                            description='Rating of the article'
                        ),
                    ],
                    description='Rate an article',
                ),
                'get_rating_for an_article': coreapi.Link(
                    url='/api/v1/articles/{slug}/ratings/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='The slug of the article.'
                        )],
                    description='Display rating of an article',
                ),
                'Report_an_article': coreapi.Link(
                    url='/api/v1/articles/{slug}/report/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        ),
                        coreapi.Field(
                            name='body',
                            required=True,
                            location='form',
                            description='Rating of the article'
                        ), ],
                    description='Report an article',
                ),
                'Favourite_article': coreapi.Link(
                    url='/api/v1/articles/{slug}/favorite/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        )],
                    description='Favourite an article',
                ),
                'get_bookmarks': coreapi.Link(
                    url='/api/v1/articles/bookmarks/',
                    action='GET',
                    description='Display all bookmarks'
                ),

                'Bookmark_articles': coreapi.Link(
                    url='/api/v1/articles/{slug}/bookmark/',
                    action='PUT',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        )],
                    description='Bookmark an article',
                ),
                'share an article on facebook': coreapi.Link(
                    url='/api/v1/{slug}/share/facebook/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='Slug of article.'
                        ),

                    ],
                    description='Share an article on facebook.'

                ),

                'share an article on twitter': coreapi.Link(
                    url='/api/v1/{slug}/share/twitter/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='Slug of article.'
                        ),

                    ],
                    description='Share an article on twitter.'

                ),

                'share an article on email': coreapi.Link(
                    url='/api/v1/{slug}/share/email/',
                    action='POST',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='Slug of article.'
                        ),
                        coreapi.Field(
                            name='email',
                            required=True,
                            location='form',
                            description='Slug of article.'
                        ),

                    ],
                    description='Share an article via email.'

                ),
                'commment edit history': coreapi.Link(
                    url='/api/v1/{slug}/comments/{id}/history/',
                    action='GET',
                    fields=[
                        coreapi.Field(
                            name='slug',
                            required=True,
                            location='path',
                            description='slug of the article'
                        ),
                        coreapi.Field(
                            name='id',
                            required=True,
                            location='path',
                            description='slug of the article'
                        )],
                    description='Track edit history of a comment',
                ),
                'get_statistics': coreapi.Link(
                    url='/api/v1/statistics/',
                    action='GET',
                    description='Get all articles statistics'
                ),
            }
        }
    )

    return response.Response(schema)
