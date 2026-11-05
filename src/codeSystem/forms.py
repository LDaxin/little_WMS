from django import forms
from .models import *
from hub.forms import apply_field_classes

types = (
    (1 , "Article"), 
    (2 , "Storage"),
)

class FormCode(forms.Form):

    types = forms.ChoiceField(choices=types)
    number = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(FormCode, self).__init__(*args, **kwargs)
        apply_field_classes(self)
