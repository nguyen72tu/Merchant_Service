from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import AbstractManagement


class AbstractTaxonomy(AbstractManagement):
    
    class Meta:
        abstract = True


class Category(AbstractTaxonomy):

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Category")


class Hashtag(AbstractTaxonomy):

    class Meta:
        verbose_name = _("Hashtag")
        verbose_name_plural = _("Hashtag")


class Keyword(AbstractTaxonomy):

    class Meta:
        verbose_name = _("Keyword")
        verbose_name_plural = _("Keyword")
        

class AbstractTaxonomyGroup1(models.Model):
    categories = models.ManyToManyField(Category)
    hashtags = models.ManyToManyField(Hashtag)
    keywords = models.ManyToManyField(Keyword)
    
    class Meta:
        abstract = True
        verbose_name = _("Abstract Taxonomy Group 1")
        verbose_name_plural = _("Abstract Taxonomy Group 1")