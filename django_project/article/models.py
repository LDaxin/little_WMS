from django.db import models
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey
from tag.models import Tag
from space.models import Space

# Create your models here.

"""
The Article model holds all articles and information about the Articles.

In der class Article is the unice Data is space 
"""

#---------------------------------------------------------------------------
# The Article model is were the unice value is space

class ArticleType(SoftDeleteObject, models.Model):

    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)

    article_toggle_space = models.BooleanField(default=False)

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

class Article(SoftDeleteObject, models.Model):
    #name of the article
    name = models.CharField(max_length=20)
    #Article Type
    pType = models.ForeignKey(ArticleType, on_delete=models.PROTECT, blank=True)
    #The place where the article is stored
    stored = models.ForeignKey(Space, related_name= "space", on_delete = models.SET_NULL, null=True, blank=True)
    #the storage space where other articles can be stored in the Article
    space = models.OneToOneField(Space, on_delete = models.CASCADE, related_name = "itemArticle", null=True, blank=True)
    #the unique code for the article
    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, blank = True, null = True)

    # here the code gets the prefix for the article
    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "a0" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)


    def __str__(self, *args, **kwargs):
        return self.name + " " + self.code.code
    
