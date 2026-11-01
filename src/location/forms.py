from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *
from . import pluscode

class FormLocation(forms.ModelForm):
    class Meta:
        model = Location
        fields = (
            'line1',
            'line2',
            'postal_code',
            'city',
            'state',
            'country',
            'latitude',
            'longitude',
            'plus_code',
        )

    def __init__(self, *args, **kwargs):
        super(FormLocation, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

    def clean(self):
        cleaned = super().clean()
        code = cleaned.get("plus_code")
        if code and cleaned.get("latitude") is None and cleaned.get("longitude") is None:
            try:
                cleaned["latitude"], cleaned["longitude"] = pluscode.decode(code)
            except ValueError:
                self.add_error("plus_code", _("Invalid Plus Code"))
        return cleaned
