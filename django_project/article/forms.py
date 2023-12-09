from django import forms
from .models import *
from codeSystem.models import *
from space.models import *

class  FormArticle(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('pType', 'space')

    def __init__(self, *args, **kwargs):
        super(FormArticle, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
        self.fields['code'].queryset = UuidCode.objects.filter(prefix="a0", used=False)
        self.fields['stored'].queryset = Space.objects.filter(active=True)



class FormChangeArticle(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('pType', 'space', 'code')

    def __init__(self, *args, **kwargs):
        super(FormChangeArticle, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
        self.fields['stored'].queryset = Space.objects.filter(active=True)
        #self.fields['Space'].widget.attrs['id'] = 'id_space_change'
