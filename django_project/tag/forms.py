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
