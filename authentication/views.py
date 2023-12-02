from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer
from user.models import User
from user.serializers import AuthorizedUserSerializer
from passlib.apps import django_context


class SignupAPIView(APIView):
    """
    User's registration view
    """

    permission_classes = [AllowAny, ]

    def post(self, request):
        try:
            password = request.data.get('password', None)
            confirm_password = request.data.get('confirm_password', None)
            if password == confirm_password and password is not None:
                serializer = SignupSerializer(data=request.data)
                if not serializer.is_valid():
                    raise ValidationError(
                        'This password is too common.',
                        'This password is entirely numeric.')
                serializer.save()

                data = {'email': serializer.data['email']}
                print(data)
                response_status = status.HTTP_201_CREATED
            else:
                data = ''
                raise ValidationError(
                    {
                        'password_mismatch': 'Password fields don\'t not match.'})
            return Response(data, status=response_status)
        except Exception as err:
            data = {'error': err}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny, ]

    def get_user(self, email):
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            return None

    def create_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    def post(self, request):
        # return Response({'error': 'User does not exist'},
        #                 status=status.HTTP_404_NOT_FOUND)
        password = request.data.get('password')
        email = request.data.get('email')
        user = self.get_user(email=email)
        if user == None:
            return Response({'error': 'User does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        hash = user.password
        is_validated = django_context.verify(password, hash)
        if not is_validated:
            return Response({'error': 'Password is not valid'},
                            status=status.HTTP_401_UNAUTHORIZED)

        token_data = self.create_token(user)
        serializer = AuthorizedUserSerializer(user)
        return Response(
            {'token_data': token_data, 'user_data': serializer.data},
            status=status.HTTP_200_OK)
