from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *
from . import pluscode
from hub.forms import apply_field_classes

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
        apply_field_classes(self)

    def clean(self):
        cleaned = super().clean()
        code = cleaned.get("plus_code")
        if code and cleaned.get("latitude") is None and cleaned.get("longitude") is None:
            try:
                cleaned["latitude"], cleaned["longitude"] = pluscode.decode(code)
            except ValueError:
                self.add_error("plus_code", _("Invalid Plus Code"))
        return cleaned
