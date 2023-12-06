from django.forms import model_to_dict
from django.db.models import F, CharField, Value
from django.db.models.functions import Concat

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import pagination

from app.custom import CustomPageNumberPagination

from app.common.decorator.queryset import additional_filters
from app.common.func import merge_list_inner_join
from django.db import IntegrityError

""" Service
    This layer will handle queryset of object and almost business condition of project
    Functions into return value as python data (dict|list,boolean,...)
    To reduce redundancy fields by request, should determine list fields as arguments
"""

class UserService:
    """ The Service return data of User

    Returns:
        list|dict|boolean: depend on value of function
    """
    queryset = User.objects.all()
    model = User
    
    def _get_model_fields(self):
        """
            Get list fields of Model
        Returns:
            list<string>: fields list
        """
        return [field.name for field in self.model._meta.get_fields()]

    
    @additional_filters({'is_active' : True}) # This could be use for some flow of system
    def _get_queryset(self):
        return self.model.objects.all()

    def retrieve(self, pk, request_fields):
        """_summary_

        Args:
            pk (int): id of model
            fields (list): list of fields want to return

        Returns:
            dict: data of model
        """
        data = {}
        if not pk:
            return None
        if request_fields:
            # Scan fields available in model
            fields = merge_list_inner_join(self._get_model_fields(), request_fields)
        
        queryset = self._get_queryset().filter(id=pk).values(*fields)

        # Handle additional fields based on specific business requirements, it should be detach new function
        additional_fields = set(request_fields) - set(fields)
        if additional_fields:
            if 'full_name' in additional_fields:
                queryset = queryset.annotate(
                    full_name=Concat(F('first_name'), Value(' '), F('last_name'), output_field=CharField())
                )
        
        data = queryset.first()
        return data


    def create(self, data):
        """
            Create User
        Returns:
            dict: Data of User as dictionary
        """
        try:
            if 'password' in data:
                data['password'] = make_password(data['password'])
            user = self.model.objects.create(**data)
            return model_to_dict(user)
        except IntegrityError as e:
            # Check if the error is related to a duplicate entry in the 'username' field
            if 'Duplicate entry' in str(e) and 'for key \'auth_user.username\'' in str(e):
                return Exception({'error': 'Username already exists. Please choose a different username.'})
            else:
                return Exception(str(e))
            
    def list(self, page_number, page_size, fields, **kwargs):
        """_summary_

        Args:
            page_number (int): page number
            page_size (int): page size
            fields (list): list of fields want to return

        Returns:
            _type_: _description_
        """
        # setup paging
        paginator = CustomPageNumberPagination()
        paginator.page = page_number
        paginator.page_size = page_size
        
        # Start queryset & return data
        try:
            result_page = paginator.paginate_queryset(
                queryset=self._get_queryset().filter(**kwargs).order_by('-id').values(*fields),
                page_size=page_size,
                page_number=page_number
            )
            
            data = {
                'paging' : {
                    'num_pages': paginator.page.paginator.num_pages,
                    'count' : paginator.page.paginator.count
                },
                'result' : result_page
            }
            return data
        except Exception as e:
            return e
    
    def delete(self, ids_list):
        """_summary_

        Args:
            ids_list (list): list of id Users

        Returns:
            int: numbers of items deleted
        """
        if not ids_list:
            return 0
        try:
            queryset = self._get_queryset().filter(id__in=ids_list)
            rows_deleted, _ = queryset.delete()
            return rows_deleted
        except Exception as e:
            return e