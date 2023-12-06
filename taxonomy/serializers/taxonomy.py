import uuid 

from rest_framework import serializers

from app.serializers.pagination import PagingSerializer

from ..models import Category, Hashtag, Keyword

class TaxonomySerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    name = serializers.CharField()
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['uuid', 'name']
        
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['uuid', 'name']

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['uuid', 'name']