from django import forms
from .models import *

#TODO change the styele to the style from the tags from odoo Lager

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

    def __init__(self, *args, **kwargs):
        super(FormTemplateArticle, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

class  FormArticleBase(forms.ModelForm):

    class Meta:
        model = Article
        fields ='__all__' 
    def __init__(self, *args, **kwargs):
        super(FormArticleBase, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
