from django.forms import model_to_dict
from django.db import IntegrityError
from django.db.models import F, CharField, Value
from django.db.models.functions import Concat

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import pagination

from app.custom import CustomPageNumberPagination
from app.common.decorator.queryset import additional_filters
from app.common.func import merge_list_inner_join, flatten_field_paths

from merchant.models import Merchant

from taxonomy.services import TaxonomyService

""" Service
    This layer will handle queryset of object and almost business condition of project
    Functions into return value as python data (dict|list,boolean,...)
    To reduce redundancy fields by request, should determine list fields as arguments
"""

class MerChantService:
    """ The Service return data of MerChant

    Returns:
        list|dict|boolean: depend on value of function
    """
    queryset = Merchant.objects.all()
    model = Merchant
    
    def _get_model_fields(self):
        """
            Get list fields of Model
        Returns:
            list<string>: fields list
        """
        return [field.name for field in self.model._meta.get_fields()]

    
    # @additional_filters({'is_active' : True}) # This could be use for some flow of system
    def _get_queryset(self, select_related, prefetch_related):
        queryset = self.model.objects.all()
        if select_related:
            queryset = queryset.select_related(*select_related)
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)
        return queryset

    def retrieve(self, pk, request_fields, request_user_fields, request_taxonomy_fields):
        """_summary_

        Args:
            pk (uuid): uuid of model
            fields (list): list of fields want to return

        Returns:
            dict: data of model
        """
        data = {}
        select_related = ['user'] if request_user_fields else []
        prefetch_related = ['categories', 'hashtags', 'keywords'] if request_taxonomy_fields else []
        if not pk:
            return None       
        
        queryset = self._get_queryset(select_related=select_related, prefetch_related=prefetch_related).filter(uuid=pk).first()
        
        if request_fields:
            data = {field: getattr(queryset, field, None) for field in request_fields}
            
        # Query realted User 
        if request_user_fields:
            data['user'] = {field: getattr(queryset.user, field, None) for field in request_user_fields}

            # user_data = {}
            # for field in request_user_fields:
            #     user_data[field] = getattr(m.user, field, None)
            # data['user'] = user_data
        # Query taxonomy
        if request_taxonomy_fields:
            data['categories'] = list(queryset.categories.all().values(*request_taxonomy_fields))
            data['hashtags'] = list(queryset.hashtags.all().values(*request_taxonomy_fields))
            data['keywords'] = list(queryset.keywords.all().values(*request_taxonomy_fields))

        return data


    def create(self, data: dict, categories: list, hashtags: list, keywords: list):
        """
            Create MerChant
        Returns:
            dict: Data of MerChant as dictionary
        """
        try:
            merchant = self.model.objects.create(**data)
            
            #TODO: need optimize this ORM code and function
            if categories and isinstance(categories, list):
                category_service = TaxonomyService('category')
                # Verify and get item existed
                list_categories_id = category_service.list(id_list=categories, request_fields=['uuid'])
                if list_categories_id:
                    merchant.categories.set(list_categories_id)
            if hashtags and isinstance(hashtags, list):
                hashtag_service = TaxonomyService('hashtag')
                # Verify and get item existed
                list_hashtags_id = hashtag_service.list(id_list=hashtags, request_fields=['uuid'])
                if list_hashtags_id:
                    merchant.hashtags.set(list_hashtags_id)
            if keywords and isinstance(keywords, list):
                keyword_service = TaxonomyService('keyword')
                # Verify and get item existed
                list_keywords_id = keyword_service.list(id_list=keywords, request_fields=['uuid'])
                if list_keywords_id:
                    merchant.keywords.set(list_keywords_id)
            
            merchant.save()
            
            return merchant.uuid
        except IntegrityError as e:
            # Check if the error is related to a duplicate entry in the 'username' field
            if 'Duplicate entry' in str(e) and 'for key \'merchant_merchant.user_id\'' in str(e):
                return Exception({'error': 'Merchant already exists for this user. Please choose a different User.'})
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
                queryset=self._get_queryset().filter(**kwargs).values(*fields),
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
            uuids_list (list): list of id MerChants

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