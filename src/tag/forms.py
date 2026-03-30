from django import forms
from .models import *

class FormTag(forms.ModelForm):
    class Meta:
        model = Tag
        fields = (
            "name",
            "parent",
        )
        labels = {
                "name":("Name"),
                "parent":("Ort"),
        }

    def __init__(self, *args, **kwargs):
        super(FormTag, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

class FormChangeTag(forms.ModelForm):
    class Meta:
        model = Tag
        fields = (
            "name",
            "parent",
        )
        labels = {
                "name":("Name"),
                "parent":("Ort"),
        }

    def __init__(self, *args, **kwargs):
        super(FormChangeTag, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
        self.fields['parent'].widget.attrs['id'] = 'id_parent_change'
