from django import forms
from .models import *

types = (
    (1 , "Article"), 
    (2 , "Storage"),
)

class FormCode(forms.Form):

    types = forms.ChoiceField(choices=types)
    number = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(FormCode, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
