from django import forms
from .models import *
from codeSystem.models import *
from hub.forms import apply_field_classes


class FormStorage(forms.ModelForm):
    code = forms.CharField(max_length=34, required=False)
    class Meta:
        model = Storage
        fields = ('name', 'parent')

    def __init__(self, *args, **kwargs):
        super(FormStorage, self).__init__(*args, **kwargs)
        apply_field_classes(self)
        self.fields['code'].queryset = UuidCode.objects.filter(prefix="s0", used=False)

class FormChangeStorage(forms.ModelForm):
    class Meta:
        model = Storage
        exclude = ('organisation', 'typ', 'space', 'code', 'tags')

    def __init__(self, *args, **kwargs):
        super(FormChangeStorage, self).__init__(*args, **kwargs)
        apply_field_classes(self)
        self.fields['parent'].widget.attrs['id'] = 'id_parent_change'


