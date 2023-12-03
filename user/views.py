import os
import base64
from django.core.files.base import ContentFile
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from django.http import Http404
from .serializers import AuthorizedUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from passlib.apps import django_context


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
        try:
            id = self.get_id(request)
            user = self.get_object(id)
            serializer = AuthorizedUserSerializer(user)
            return Response(serializer.data)
        except:
            return Response({"Error": "given token is not valid"},
                            status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=None):
        id = self.get_id(request)
        user = self.get_object(id)
        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')
        if old_password != '' and new_password != '':
            hashed_password = user.password
            is_validated = django_context.verify(
                old_password, hashed_password)
            if not is_validated:
                return Response({'error': 'Password is not valid'},
                                status=status.HTTP_401_UNAUTHORIZED)
            user.set_password(new_password)
        user_data = {'fullName': request.data.get('fullName'),
                     'email': request.data.get('email')}
        try:
            format, imgstr = request.data.get('avatar').split(';base64,')
            ext = format.split('/')[-1]

            decoded_avatar_image = ContentFile(base64.b64decode(imgstr),
                                               name='temp.' + ext)
            user_data['avatar'] = decoded_avatar_image
        except ValueError:
            pass
        serializer = AuthorizedUserSerializer(user, data=user_data,
                                              context={
                                                  'fullName': request.data.get(
                                                      'fullName')})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        id = self.get_id(request)
        user = self.get_object(id)
        user_email = user.email
        user.delete()
        return Response(user_email, status=status.HTTP_204_NO_CONTENT)
