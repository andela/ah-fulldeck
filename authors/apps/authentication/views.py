import os
import jwt
from rest_framework import status, generics
from rest_framework.generics import (
    RetrieveUpdateAPIView, CreateAPIView, ListAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from authors import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    SocialAuthSerializer, PasswordResetSerializer)
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from authors.settings import SECRET_KEY
from .send_email import send_email
from .models import User


class HomeView(ListAPIView):
    """class to access the home route"""

    def get(self, request):
        return Response("Welcome to fulldeck Authors Haven API")


class RegistrationAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        email = serializer.data['email']
        username = serializer.data['username']
        token = serializer.data['token']
        sender = os.getenv('EMAIL_SENDER')

        sender = "ahfulldeck@gmail.com"
        current_site = get_current_site(request)
        verification_link = "http://" + current_site.domain + \
            '/api/v1/verify/{}'.format(token)
        subject = "Authors Haven: Verification email"
        message_content = "Please verify that you requested to use this email address, \
            if you did not request this update, please ignore this \
            message."
        button_content = "VERIFY EMAIL ADDRESS"
        message = render_to_string('email_template.html', {
            'verification_link': verification_link,
            'message_content': message_content,
            'button_content': button_content,
            'title': subject,
            'username': username,
        })
        body_content = strip_tags(message)
        msg = EmailMultiAlternatives(subject, body_content, sender, to=[email])
        msg.attach_alternative(message, "text/html")
        msg.send()

        response_message = {
            "message": "User registered successfully. Check your mail for verification",
            "user_info": serializer.data
        }

        return Response(response_message, status=status.HTTP_201_CREATED)


class VerifyAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def get(self, request, token):
        email = jwt.decode(token, SECRET_KEY)['email']
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()

        return Response({"message": "Email has been verified successfully, thank you!"})


class LoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = PasswordResetSerializer

    def post(self, request):
        recipient = request.data.get('email', {})  # user enters email
        if not recipient:
            return Response({"message": "Enter your email"}, status=status.HTTP_400_BAD_REQUEST)
        # generate a new token for each email entered
        token = jwt.encode({"email": recipient},
                           settings.SECRET_KEY, algorithm='HS256')
        # confirm user exists
        user_exists = User.objects.filter(email=recipient).exists()
        if user_exists:
            result = send_email(recipient, token, request)
            return Response(result, status=status.HTTP_200_OK)
        else:  # If user does not exist
            result = {
                'message': 'Ooopps, no user found with that email'
            }
            return Response(result, status=status.HTTP_404_NOT_FOUND)


class PasswordUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def update(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:
            return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        password = {
            "password": password
        }
        serializer = self.serializer_class(data=password)
        serializer.is_valid(raise_exception=True)

        try:
            decode_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=decode_token['email'])
            user.set_password(request.data.get('password'))
            user.save()
            result = {'message': 'Your password has been reset'}
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)


class SocialAuthView(CreateAPIView):
    """Login via social sites (Google, Twitter, Facebook)"""
    permission_classes = (AllowAny,)
    serializer_class = SocialAuthSerializer
    renderer_classes = (UserJSONRenderer,)

    def create(self, request):
        """Takes in provider and access_token to authenticate user"""
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get("provider")
        authenticated_user = request.user if not request.user.is_anonymous else None
        strategy = load_strategy(request)

        # Load backend associated with the provider
        try:
            
            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None)
            if isinstance(backend, BaseOAuth1):
                if "access_token_secret" in request.data:
                    access_token={
                        'oauth_token': request.data['access_token'],
                        'oauth_token_secret': request.data['access_token_secret']
                    }
                else:
                    return Response(
                        {"error": "Access token secret is required"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            elif isinstance(backend, BaseOAuth2):
                
                access_token = serializer.data.get("access_token")

        except MissingBackend:
            return Response({"error": "The Provider is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Go through the pipeline to create user if they don't exist
        try:
            user = backend.do_auth(access_token, user=authenticated_user)
        
        except BaseException:
            return Response({"error": "Invalid token"},
                            status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:

            email = user.email
            username = user.username
            token = user.token
            user_data = {
                "username": username,
                "email": email,
                "token": token
            }
            return Response(user_data, status=status.HTTP_200_OK)
