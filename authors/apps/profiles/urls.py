from django.urls import path

from .views import ProfileRetrieveAPIView

app_name = 'profiles'

urlpatterns = [
    path('users/<str:username>', ProfileRetrieveAPIView.as_view(), name='user_profile')
]

