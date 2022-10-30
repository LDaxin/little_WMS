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

class FormTemplatePart(forms.ModelForm):
    class Meta:
        model = Template
        fields = (
            'name',
            'tag'
         )
        labels = {
                'name':("Name"),
                'tag':("Tags")
        }
    def __init__(self, *args, **kwargs):
        super(FormTemplatePart, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

class FormTemplateContainer(forms.ModelForm):
    class Meta:
        model = Template
        fields = (
            'name',
            'tag',
            'innerWidth',
            'innerDepth',
            'innerHeight'
         )
        labels = {
                'name':("Name"),
                'tag':("Tags"),
                'innerWidth':("innere Breite"),
            'innerDepth':("innere Tiefe"),
            'innerHeight':("innere Höhe")
        }
    def __init__(self, *args, **kwargs):
        super(FormTemplateContainer, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
