from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .mixins import MerchantMixins

@authentication_classes([])
@permission_classes([permissions.AllowAny])
class MerchantDetailView(APIView, MerchantMixins):
    """
    API endpoint that allows users to be viewed or edited.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='uuid', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Id of Merchant'),
        ],
        responses={
            200: MerchantMixins.serializer_retrieve,
        }
    )
    def get(self, request):
        params = request.GET
        serializer = self.retrieve(id=params['uuid'])
        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    @swagger_auto_schema(
        request_body=MerchantMixins.serializer_create,
        responses={status.HTTP_201_CREATED: 'OKE'}
    )
    def post(self, request):
        """
        Create a new Merchant.
        """
        serializer = self.create(request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)