from django import forms
from .models import *
class FormWarehouse(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = (
            "name",
            "location"
        )
        labels = {
                "name":("Name"),
                "location":("Standort")
        }

    def __init__(self, *args, **kwargs):
        super(FormWarehouse, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

class FormStorage(forms.ModelForm):
    class Meta:
        model = Storage
        fields = (
            "name",
            "warehouse"
        )
        labels = {
                "name":("Name"),
                "warehouse":("Wahrenhaus")
        }

    def __init__(self, *args, **kwargs):
        super(FormStorage, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"


class FormShelf(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = (
            "storage",
            "rows",
            "columns",
        )
        labels = {
                "storage":("Lager"),
                "rows":("Reihen"),
            "columns":("Faecher pro Reihe"),
        }

    def __init__(self, *args, **kwargs):
        super(FormShelf, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

