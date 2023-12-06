from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

class CustomPageNumberPagination(PageNumberPagination):
    
    def paginate_queryset(self, queryset, page_size, page_number, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = page_size
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(page_number, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        return list(self.page)
    
    def get_page_number(self, page_number, paginator):
        page_number = page_number
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        return page_number


class SwaggerSchemaView(get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="...",
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=(),
)):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        # Customize Swagger UI settings to include JWT token authorization
        response.data['securityDefinitions'] = {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
            },
        }
        response.data['security'] = [{'Bearer': []}]

        return response