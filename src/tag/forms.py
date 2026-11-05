from django import forms
from .models import *
from hub.forms import apply_field_classes

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
        apply_field_classes(self)

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
        apply_field_classes(self)
        self.fields['parent'].widget.attrs['id'] = 'id_parent_change'
