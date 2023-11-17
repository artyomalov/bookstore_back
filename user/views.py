from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from django.http import Http404
from .serializers import AuthorizedUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from passlib.apps import django_context
import os


class AuthUserDetail(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_id(self, request):
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            return response[1]['id']
        else:
            raise Exception('Token is not valid')

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        id = self.get_id(request)
        user = self.get_object(id)
        serializer = AuthorizedUserSerializer(user,
                                              context={'request': request})
        path_to_user_avatar = os.path.join(
            os.path.abspath('.'),
            'media',
            str(user.avatar).replace('/', '\\')
        )
        if not os.path.exists(path_to_user_avatar) and not os.path.isfile(
                path_to_user_avatar):
            domain = request.build_absolute_uri('/')[:-1]
        return Response(serializer.data)

    def put(self, request, format=None):
        print(request.data['avatar'].file)
        id = self.get_id(request)
        user = self.get_object(id)
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if bool(old_password) and bool(new_password):

            hash = user.password
            is_validated = django_context.verify(
                old_password, hash)
            if not is_validated:
                return Response({'error': 'Password is not valid'},
                                status=status.HTTP_401_UNAUTHORIZED)
            user.set_password(new_password)
        user_data = {
            'email': request.data.get('email'),
            'full_name': request.data.get('full_name'),
            'avatar': request.data.get('avatar')
        }
        if request.data['avatar'] == 'null':
            user_data = {
                'email': request.data.get('email'),
                'full_name': request.data.get('full_name'),
            }
        else:
            user_avatar = user.avatar
            path_to_old_avatar = os.path.join(
                os.path.abspath('.'),
                'user',
                'media',
                str(user_avatar).replace('/', '\\')
            )
            if path_to_old_avatar is not None:
                if os.path.exists(path=path_to_old_avatar):
                    os.remove(path_to_old_avatar)

        serializer = AuthorizedUserSerializer(user, data=user_data,
                                              partial=True)
        if serializer.is_valid():
            serializer.save()
            domain = request.build_absolute_uri('/')[:-1]

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        id = self.get_id(request)
        user = self.get_object(id)
        user_email = user.email
        user.delete()
        return Response(user_email, status=status.HTTP_204_NO_CONTENT)
