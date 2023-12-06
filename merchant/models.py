from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from app.models import AbstractManagement
from taxonomy.models import AbstractTaxonomyGroup1

class Merchant(AbstractManagement, AbstractTaxonomyGroup1):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
    )
    
    class Meta:
        verbose_name = _("Merchant")
        verbose_name_plural = _("Merchant")