# views.py
from rest_framework import viewsets
from .models import AbstractTaxonomy, Category, Hashtag, Keyword
from .serializers.taxonomy import CategorySerializer, HashtagSerializer, KeywordSerializer

# class TaxonomyAbstractViewSet(viewsets.ModelViewSet):
#     queryset = AbstractTaxonomy.objects.all()
#     serializer_class = TaxonomyAbstractSerializer
#     class Meta:
#         abstract = True
        
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = HashtagSerializer
    
class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = KeywordSerializer
    
