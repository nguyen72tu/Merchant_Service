import uuid

from rest_framework import serializers

from app.serializers.pagination import PagingSerializer

from taxonomy.serializers.taxonomy import TaxonomySerializer


class MerchantDetailSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    user_id = serializers.IntegerField()
    name = serializers.CharField()
    
    categories = TaxonomySerializer(many=True)
    hashtags = TaxonomySerializer(many=True)
    keywords = TaxonomySerializer(many=True)


class MerchantCreateSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, read_only=True)
    user_id = serializers.IntegerField()
    name = serializers.CharField()
    
    categories = serializers.ListField(child=serializers.UUIDField())
    hashtags = serializers.ListField(child=serializers.UUIDField())
    keywords = serializers.ListField(child=serializers.UUIDField())