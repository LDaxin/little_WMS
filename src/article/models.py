from django.db import models
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey
from tag.models import Tag
from space.models import Space

# Create your models here.

ZUSTAND_CHOICES = [
    ("gut", "gut"),
    ("gebraucht", "gebraucht"),
    ("defekt", "defekt"),
    ("reparatur", "in Reparatur"),
]

SIZE_CLASS_CHOICES = [
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
]

"""
The Article model holds all articles and information about the Articles.

In der class Article is the unice Data is space 
"""

#---------------------------------------------------------------------------
# The Article model is were the unice value is space

class ArticleType(SoftDeleteObject, models.Model):

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)

    article_toggle_space = models.BooleanField(default=False)
    allow_merge_split = models.BooleanField(default=False)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "at" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.name

class ArticleBase(SoftDeleteObject, models.Model):

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=20)

    pType = models.ForeignKey(ArticleType, on_delete=models.CASCADE, blank=True , null = False)

    # Catalog properties (shared by all instances of this model)
    outer_length_mm = models.IntegerField(null=True, blank=True)
    outer_width_mm = models.IntegerField(null=True, blank=True)
    outer_height_mm = models.IntegerField(null=True, blank=True)
    size_class = models.CharField(max_length=2, choices=SIZE_CLASS_CHOICES, null=True, blank=True)
    attributes = models.JSONField(default=dict)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "ab" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.name

class Article(SoftDeleteObject, models.Model):

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=1)
    base = models.ForeignKey(ArticleBase, on_delete=models.CASCADE, blank=True, null=False)
    #The place where the article is stored
    stored = models.ForeignKey(Space, related_name= "space", on_delete = models.SET_NULL, null=True, blank=True)
    #the storage space where other articles can be stored in the Article
    space = models.OneToOneField(Space, on_delete = models.CASCADE, related_name = "itemArticle", null=True, blank=True)
    #the unique code for the article
    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, blank = True, null = True)

    amount = models.CharField(max_length=20, null = True, blank = True)

    # Global fields (every article has them)
    zustand = models.CharField(max_length=20, choices=ZUSTAND_CHOICES, default="gut")
    anschaffungswert = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    kaufdatum = models.DateField(null=True, blank=True)
    ablaufdatum = models.DateField(null=True, blank=True)
    gewicht_gramm = models.IntegerField(null=True, blank=True)
    mindestbestand = models.IntegerField(null=True, blank=True)
    notiz = models.TextField(blank=True)
    standard_lagerplatz = models.ForeignKey(Space, related_name="standard_for", on_delete=models.SET_NULL, null=True, blank=True)
    ist_verbrauchsartikel = models.BooleanField(default=False)
    menge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mengeneinheit = models.CharField(max_length=20, blank=True)

    # here the code gets the prefix for the article
    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "a0" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)


    def __str__(self, *args, **kwargs):
        return self.base.name + " " + self.code.code
    
