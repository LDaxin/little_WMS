from django import forms
from .models import *

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
