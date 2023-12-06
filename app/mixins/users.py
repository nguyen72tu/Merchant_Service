from app.services import UserService
from app.serializers.users import UserRetrieveSerializer, UserCreateSerializer, UsersListSerializer, UserIdsSerializer, raise_errors
from app.serializers.pagination import PagingSerializer
from app.serializers.message import MessageSerializer

service = UserService()

class UserMixin:
    """
    Retrieve a model instance.
    """
    serializer_retrieve = UserRetrieveSerializer
    serializer_create = UserCreateSerializer
    serialzer_user_ids = UserIdsSerializer
    serializer_list = UsersListSerializer
    serializer_msg = MessageSerializer
    
    def retrieve(self, id):
        """
            Retrieve data of User
            Mix User's information as Python data and parse to Serialzer
        Args:
            id (int): id of User
        Returns:
            UserRetrieveSerializer: Serializer
        """
        if not id:
            return None
        # Get list fields of Serializer
        request_fields = self._get_serializer_retrieve_fields(action='retrieve')
        # Ask service to return data
        data = service.retrieve(
            pk=id, 
            request_fields=request_fields
        )
        # Check data & parse, return
        return self.serializer_retrieve(data=data)


    def create(self, request_data):
        """
            Create User
        Args:
            request_data (dict): data
        Raises:
            Exception: error

        Returns:
            UserRetrieveSerializer: Serializer
        """
        data = {}
        if not request_data:
            return None
        # Validate data request
        serializer = self.serializer_create(data=request_data)
        if not serializer.is_valid():
            return serializer
        # Send data to service to create
        data = service.create(request_data)
        # Meeting error when create data
        if isinstance(data, Exception):
            raise_errors(str(data))
        # Return to retrieve
        if data:
            return self.retrieve(data['id'])
    
    
    def list(self, kwargs):
        """
            Get list of Users's information with paging
        Args:
            kwargs (dict): _description_

        Raises:
            raise_errors: _description_

        Returns:
            UsersListSerializer: Serializer
        """
        # Get and remove paging variables
        page_number = kwargs.get('page_number', 1)
        page_size = kwargs.get('page_size', 2)
        
        kwargs.pop('page_number', None)
        kwargs.pop('page_size', None)
        
        # Get fields the serialzer needed
        request_fields = self._get_serializer_retrieve_fields(action='retrieve')
        
        # Start request data from service
        data = service.list(
            page_number=page_number, 
            page_size=page_size, 
            fields=request_fields, 
            **kwargs
        )
        
        # Return error if meet
        if isinstance(data, Exception):
            raise raise_errors(str(data))
        
        # Generate data serializer for return
        # Paging Serializer
        paging_serializer = PagingSerializer({
            'count' : data['paging']['count'],
            'number_pages' : data['paging']['num_pages'],
        })

        # User List Serializer
        result_serializer = self.serializer_list({
            'paging': paging_serializer.data,
            'result': self.serializer_retrieve(data['result'], many=True).data,
        })
        
        return result_serializer
    
    def remove(self, request_data):
        """
            Remove/Delete list of Users by ID
        Args:
            request_data (UserIdsSerializer): _description_

        Raises:
            raise_errors: _description_

        Returns:
            MessageSerializer: _description_
        """
        serializer = self.serialzer_user_ids(data=request_data)
    
        if not serializer.is_valid():
            return serializer
        
        ids_list = request_data['user_ids']
        total_ids = len(ids_list)
        
        data = service.delete(ids_list=ids_list)
        # Return error if meet
        if isinstance(data, Exception):
            raise raise_errors(str(data))
        
        msg = "Deleted {deleted} on {total_ids} items".format(deleted=data, total_ids=total_ids)
        serialzer_response = self.serializer_msg(data={'msg': msg})
        
        
        return serialzer_response
        
    def _get_serializer_retrieve_fields(self, action):
        """
            Get list fields of serializer class
        Args:
            action (string): retrieve or create

        Returns:
            list: list fields
        """
        if action == 'retrieve':
            return list(self.serializer_retrieve().get_fields().keys())
        elif action == 'create':
            return list(self.serializer_create().get_fields().keys())