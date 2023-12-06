from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import AbstractManagement
from merchant.models import Merchant
from taxonomy.models import AbstractTaxonomyGroup1


class Product(AbstractManagement, AbstractTaxonomyGroup1):
    merchant = models.ForeignKey(
        Merchant, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='product',
    )
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Product")