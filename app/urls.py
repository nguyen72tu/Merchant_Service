"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.routers import DefaultRouter

from app.custom import SwaggerSchemaView
from app.views import UserView, TestAPI, UserListView, SignUpAPIView, SignInAPIView

from merchant.views import MerchantDetailView
from taxonomy.views import CategoryViewSet, HashtagViewSet, KeywordViewSet

router = DefaultRouter()
router.register(r'taxonomy/category', CategoryViewSet, basename='category')
router.register(r'taxonomy/hashtag', HashtagViewSet, basename='hashtag')
router.register(r'taxonomy/keyword', KeywordViewSet, basename='keyword')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/testapi/', TestAPI.as_view(), name='test_api'),
    path('api/user/', UserView.as_view(), name='user_api'),
    path('api/users/', UserListView.as_view(), name='users_api'),
    path('api/merchant/', MerchantDetailView.as_view(), name='merchant_api'),
    # path('api/taxonomy/category/', CategoryViewSet.as_view(), name='category_api'),
    path('api/sign/up/', SignUpAPIView.as_view(), name='sign_up'),
    path('api/sign/in/', SignInAPIView.as_view(), name='sign_in'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', SwaggerSchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SwaggerSchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
