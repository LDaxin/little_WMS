from django import forms
from .models import *

class  FormArticle(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('pType', 'ref')

    def __init__(self, *args, **kwargs):
        super(FormArticle, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"

class FormChangeArticle(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('pType', 'ref')

    def __init__(self, *args, **kwargs):
        super(FormChangeArticle, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
        self.fields['tag'].widget.attrs['id'] = 'id_tag_change'
        self.fields['stored'].widget.attrs['id'] = 'id_stored_change'
        self.fields['unit'].widget.attrs['id'] = 'id_unit_change'
