from django import forms
from .models import *

class Form_location(forms.ModelForm):
    class Meta:
        model = Location
        fields = (
            'name',
            'traditional_land', 
            'traditional_country',
            'traditional_city',
            'traditional_zipcode',
            'traditional_street',
            'traditional_street_number'
         )
        labels = {
            'name':("Name"),
            'traditional_land':("Land"), 
            'traditional_country':("Bundesland"),
            'traditional_city':("Stadt"),
            'traditional_zipcode':("Postleitzahl"),
            'traditional_street':("Straße"),
            'traditional_street_number':("Nr.")
        }

    def __init__(self, *args, **kwargs):
        super(Form_location, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
