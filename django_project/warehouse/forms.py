from django import forms
from .models import *

class FormStorage(forms.ModelForm):
    class Meta:
        model = Storage
        fields = (
            "name",
        )
        labels = {
                "name":("Name"),
        }

    def __init__(self, *args, **kwargs):
        super(FormStorage, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"



