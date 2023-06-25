from django import forms
from .models import *

#TODO change the styele to the style from the tags from odoo Lager

def getArticleTypeFields(typ, table, fieldsForDel=[]):
    for field in ArticleType._meta.get_fields():
        if field.name.startswith(table + "_toggle_"):
            if not getattr(typ, field.name) or (table == "article" and field.name == "article_toggle_ref"):
                fieldsForDel.append(field.name.replace(table+"_toggle_", ""))

    return fieldsForDel



class FormTag(forms.ModelForm):
    class Meta:
        model = Tag
        fields = (
            'name',
            'parent'
         )
        labels = {
                'name':("Name"),
                'parent':("Herachie")
        }
    def __init__(self, *args, **kwargs):
        super(FormTag, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

class FormTemplateArticle(forms.ModelForm):

    class Meta:
        model = ArticleTemplate
        fields = '__all__'
        exclude = ("pType",)

    def __init__(self, *args,typ= None, **kwargs):
        super(FormTemplateArticle, self).__init__(*args, **kwargs)
        if not typ == None:
            for delField in getArticleTypeFields(typ, 'template', []):
                del self.fields[delField]

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

class  FormArticleBase(forms.ModelForm):

    class Meta:
        model = Article
        fields ='__all__' 
    def __init__(self, *args, typ= None, **kwargs):
        super(FormArticleBase, self).__init__(*args, **kwargs)

        if typ != None:
            for delField in getArticleTypeFields(typ, 'article', []):
                del self.fields[delField]

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
