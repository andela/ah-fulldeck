from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .exceptions import ProfileDoesNotExist
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer


class ProfileRetrieveAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def get(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, username):

        if request.user.username != username:
            error_message = {
                'error': 'You are not allowed to update the details for user {}'.format(username)
            }
            return Response(error_message, status=status.HTTP_403_FORBIDDEN)
        user_data = request.data.get('profile', {})

        serializer = ProfileSerializer(
            request.user.profile,
            data=user_data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            self.check_object_permissions(request, user_data)
            serializer.save()
            return Response(serializer.data)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
