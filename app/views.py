from rest_framework import permissions
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app.mixins.users import UserMixin


@authentication_classes([])
@permission_classes([permissions.AllowAny])
class TestAPI(APIView):
    
    def get(self, request, format=None):
        """
        """
        some_text = ''
        return Response({'where' : 'here'})
    
    def post(self, request, format=None):
        """
        """
        return Response({'where' : 'here POST'})


class UserView(APIView, UserMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Id of User'),
        ],
        responses={
            200: UserMixin.serializer_retrieve,
        }
    )
    def get(self, request):
        params = request.GET
        serializer = self.retrieve(id=params['id'])
        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        request_body=UserMixin.serializer_create,
        responses={status.HTTP_201_CREATED: UserMixin.serializer_retrieve}
    )
    def post(self, request):
        """
        Create a new user.
        """
        serializer = self.create(request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView, UserMixin):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page_number', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: UserMixin.serializer_list,
        }
    )
    def get(self, request):
        page_number = request.GET.get('page_number', 1)
        page_size = request.GET.get('page_size', 2)
        serializer = self.list(request.GET.dict())
        if not serializer:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=UserMixin.serialzer_user_ids,
        responses={status.HTTP_200_OK : UserMixin.serializer_msg}
    )
    def delete(self, request, format=None):
        serializer = self.remove(request.data)
        
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@authentication_classes([])
@permission_classes([permissions.AllowAny])
class SignUpAPIView(APIView, UserMixin):
    @swagger_auto_schema(
        request_body=UserMixin.serializer_create,
        responses={status.HTTP_201_CREATED: UserMixin.serializer_retrieve}
    )
    def post(self, request):
        """
        Create a new user.
        """
        serializer = self.create(request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([])
@permission_classes([permissions.AllowAny])
class SignInAPIView(TokenObtainPairView, UserMixin):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token_string = response.data['access']
        access_token = AccessToken(access_token_string)
        serializer_user = self.retrieve(access_token['user_id'])
        # Customize the response format or add additional data
        if serializer_user.is_valid():
            response.data['user'] = serializer_user.data
            return response
        else:
            return Response(serializer_user.errors,status=status.HTTP_404_NOT_FOUND)
        