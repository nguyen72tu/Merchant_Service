from .models import Category, Hashtag, Keyword, AbstractTaxonomy

class TaxonomyService():
    _list_model = {
        'category': Category,
        'hashtag': Hashtag,
        'keyword': Keyword
    }
    
    model = AbstractTaxonomy
    
    def __init__(self, model_name: str):
        self.model = self._list_model[model_name]
    
    def _get_queryset(self):
        return self.model.objects.all()
        
    def list(self, id_list: list, request_fields: list):
        """
            Return list of Taxnomy
        Args:
            id_list (list): list uuid of taxnomy
            request_fields (list): list of fields want to get

        Returns:
            list: list of taxonomies information
        """
        data = self._get_queryset().values_list(*request_fields, flat=True).filter(uuid__in=id_list)
        
        return data