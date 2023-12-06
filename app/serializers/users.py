from rest_framework import serializers

from app.serializers.pagination import PagingSerializer


def raise_errors(exception: Exception):
    raise serializers.ValidationError(str(exception))
    
class UserRetrieveSerializer(serializers.Serializer):
    """
        This Serializer for request GET User
    """
    
    id = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    
    #full_name = serializers.CharField(max_length=100)
    

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    
    # Some validate below is sample, they should only validate the format and dont touch to queryset
    def validate_username(self, value):
        # Add custom validation for username
        if not value.isalnum():
            raise serializers.ValidationError("Username should contain only alphanumeric characters.")
        return value

    def validate_first_name(self, value):
        # Add custom validation for first_name
        if not value.isalpha():
            raise serializers.ValidationError("First name should contain only alphabetical characters.")
        return value

    def validate_last_name(self, value):
        # Add custom validation for last_name
        if not value.isalpha():
            raise serializers.ValidationError("Last name should contain only alphabetical characters.")
        return value

    def validate_email(self, value):
        # Add custom validation for email
        if not value.endswith('@example.com'):
            raise serializers.ValidationError("Email should end with '@example.com'.")
        return value
    
    def raise_errors(self, exception: Exception):
        raise serializers.ValidationError(str(exception))
    
class UsersListSerializer(serializers.Serializer):
    paging = PagingSerializer()
    result = UserRetrieveSerializer(many=True)
    

class UserIdsSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())