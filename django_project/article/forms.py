from django import forms
from .models import *

class  FormArticle(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('pType',)

    def __init__(self, *args, **kwargs):
        super(FormArticle, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
