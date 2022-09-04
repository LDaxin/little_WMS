from django import forms
from .models import *

class Form_warehouse(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = (
            "location",
            "name"
        )

    def __init__(self, *args, **kwargs):
        super(Form_warehouse, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

