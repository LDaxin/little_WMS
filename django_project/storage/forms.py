from django import forms
from .models import *

class FormStorage(forms.ModelForm):
    class Meta:
        model = Storage
        fields = (
            "name",
            "parent",
        )
        labels = {
                "name":("Name"),
                "parent":("Ort"),
        }

    def __init__(self, *args, **kwargs):
        super(FormStorage, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

class FormChangeStorage(forms.ModelForm):
    class Meta:
        model = Storage
        fields = (
            "name",
            "parent",
        )
        labels = {
                "name":("Name"),
                "parent":("Ort"),
        }

    def __init__(self, *args, **kwargs):
        super(FormChangeStorage, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
        self.fields['parent'].widget.attrs['id'] = 'id_parent_change'


