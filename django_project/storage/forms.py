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

    def __init__(self, *args, typ = None,  **kwargs):
        super(FormStorage, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"



