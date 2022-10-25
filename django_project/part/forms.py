from django import forms
from .models import *

#TODO change the styele to the style from the tags from odoo Lager
class Form_part(forms.ModelForm):
    class Meta:
        model = Part
        fields = (
            'name',
            'tag'
         )
        labels = {
                'name':("Name"),
                'tag':("Tags")
        }
    def __init__(self, *args, **kwargs):
        super(Form_part, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"



class Form_tag(forms.ModelForm):
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
        super(Form_tag, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"



class Form_container(forms.ModelForm):
    class Meta:
        model = Container
        fields = (
            'innerWidth',
            'innerDepth',
            'innerHeight'
         )
        labels = {
                'innerWidth':("Innen Breite"),
                'innerDepth':("Innen Tiefe"),
                'innerHeight':("Innen Höhe")
        }
    def __init__(self, *args, **kwargs):
        super(Form_container, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
