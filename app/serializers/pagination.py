from rest_framework import serializers

class PagingSerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=1, required=False, default=1)
    number_pages = serializers.IntegerField(min_value=1, required=False, default=10)