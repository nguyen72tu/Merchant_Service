from .services import MerChantService
from .serializers import MerchantDetailSerializer, MerchantCreateSerializer


service = MerChantService()

class MerchantMixins:
    serializer_retrieve = MerchantDetailSerializer
    serializer_create = MerchantCreateSerializer
    
    # Define manual
    serializer_merchant_retrieve_fields = ['uuid', 'name', 'user_id']
    serializer_taxonomy_retrieve_fields = ['uuid', 'name']
    serializer_user_fields = ['id', 'email']
    
    def retrieve(self, id):
        data = service.retrieve(
            pk=id,
            request_fields=self.serializer_merchant_retrieve_fields,
            request_user_fields=self.serializer_user_fields,
            request_taxonomy_fields=self.serializer_taxonomy_retrieve_fields,
        )
        serializer = self.serializer_retrieve(data=data)
        return serializer
    
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
        categories = []
        hashtags = []
        keywords = []
        if 'categories' in request_data:
            categories = request_data['categories']
            request_data.pop('categories')
        if 'hashtags' in request_data:
            hashtags = request_data['hashtags']
            request_data.pop('hashtags')
        if 'keywords' in request_data:
            keywords = request_data['keywords']
            request_data.pop('keywords')
        data = service.create(request_data, categories=categories, hashtags=hashtags, keywords=keywords)
        # Meeting error when create data
        if isinstance(data, Exception):
            raise_errors(str(data))
        # Return to retrieve
        if data:
            return self.retrieve(data)
        
        
    
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
