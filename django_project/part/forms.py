from django import forms
from .models import *

class Form_part(forms.ModelForm):
    class Meta:
        model = Part
        fields = (
         )
        labels = {

        }
