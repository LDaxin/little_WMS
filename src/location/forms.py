from django import forms
from .models import *

class FormLocation(forms.ModelForm):
    class Meta:
        model = Location
        fields = (
            'traditionalLand', 
            'traditionalCountry',
            'traditionalCity',
            'traditionalZipcode',
            'traditionalStreet',
            'traditionalStreetNumber'
         )
        labels = {
            'traditionalLand':("Land"), 
            'traditionalCountry':("Bundesland"),
            'traditionalCity':("Stadt"),
            'traditionalZipcode':("Postleitzahl"),
            'traditionalStreet':("Straße"),
            'traditionalStreetNumber':("Nr.")
        }

    def __init__(self, *args, **kwargs):
        super(FormLocation, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
