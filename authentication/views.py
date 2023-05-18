from user.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import SingupSerializer


class SignupAPIView(APIView):
    '''
    User's registration view
    '''

    permission_classes = [AllowAny, ]

    def post(self, request):
        password = request.data.get('password', None)
        confirm_password = request.data.get('confirm_password', None)
        if password == confirm_password:
            serializer = SingupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ''
            raise ValidationError(
                {'password_mismatch': 'Password fields don\'t not match.'})
        return Response(data, status=response)
