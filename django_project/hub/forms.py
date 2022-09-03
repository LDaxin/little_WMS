from cProfile import label
from tokenize import blank_re
from django import forms

class Form_location(forms.Form):
    land = forms.CharField(max_length=50, label="Land")
    country = forms.CharField(max_length=50, label="Bundesland")
    city = forms.CharField(max_length=50, label="Stadt")
    zipcode = forms.CharField(max_length=15, label="Postleitzahl")
    street = forms.CharField(max_length=200, label="Straße")
    street_number = forms.CharField(max_length=4, label="Nr.")
    longitude = forms.FloatField(label="Längengrad", required=False)
    latitude = forms.FloatField(label="Breitengrad", required=False)
    what3words = forms.CharField(max_length=100, label="what3words ///", required=False)
    what3words_lang = forms.CharField(max_length=50,label="what3words /// Sprache", required=False)

    def __init__(self, *args, **kwargs):
        super(Form_location, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
